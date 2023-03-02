if __name__ == "__main__":
    import argparse
    from os import path, makedirs
    import subprocess
    from re import match
    from sys import stdout
    from time import time

    def run_benchmark(architecture, benchmark, icache_size, dcache_size, dcache_associativity, cacheline_size):
        if benchmark.lower() == "susan":
            susan_path = f"benchmarks/susan"
            binary = f"{susan_path}/susan"
            arguments = [
                f"{susan_path}/input_{args.benchmark_size}.pgm {susan_path}/output_{args.benchmark_size}.smoothing.pgm -s",
                f"{susan_path}/input_{args.benchmark_size}.pgm {susan_path}/output_{args.benchmark_size}.edges.pgm -e",
                f"{susan_path}/input_{args.benchmark_size}.pgm {susan_path}/output_{args.benchmark_size}.corners.pgm -c",
            ]
        elif benchmark.lower() == "crc":
            binary = "benchmarks/CRC32/crc"
            arguments = [f"benchmarks/adpcm/data/{args.benchmark_size}.pcm"]
        else:
            raise Exception(f"Invalid benchmark '{benchmark}'")

        if architecture.upper() == "ARM":
            binary = f"{binary}.arm"
        elif architecture.upper() != "X86":
            raise Exception(f"Invalid architecture '{architecture}'")

        cache_size_pattern = r"^\d+(k|M)?B$"
        if not match(cache_size_pattern, icache_size):
            raise Exception(f"Invalid icache size '{icache_size}'")
        elif not match(cache_size_pattern, dcache_size):
            raise Exception(f"Invalid dcache size '{dcache_size}'")
        
        i = size_string_to_int(icache_size)
        d = size_string_to_int(dcache_size)
        if not (i != 0 and ((i & (i - 1)) == 0)):
            raise Exception(f"Instruction cache size '{icache_size}' is not a power of 2")
        elif not (d != 0 and ((d & (d - 1)) == 0)):
            raise Exception(f"Data cache size '{dcache_size}' is not a power of 2")

        for argument in arguments:
            command = [
                f"gem5/build/{architecture.upper()}/gem5.opt",
                "--outdir=gem5/m5out",
                "gem5/configs/example/se.py",
                f"--cmd={binary}",
                f"--options={argument}",
                # Add arguments to se.py here
                "--cpu-type=TimingSimpleCPU",
                "--caches",
                f"--l1i_size={icache_size}",
                f"--l1d_size={dcache_size}",
                f"--l1d_assoc={dcache_associativity}",
                f"--cacheline_size={cacheline_size}",
            ]
            output = subprocess.PIPE if not args.verbose else None
            process = subprocess.Popen(command, stdout=output, stderr=output)
            try:
                process.wait()
            except subprocess.CalledProcessError as e:
                raise Exception(
                    f"Command failed with return code {e.returncode}: {e.cmd}"
                )
            except KeyboardInterrupt:
                process.terminate()
                exit()

    def cpi():
        with open("gem5/m5out/stats.txt", "r") as stats_file:
            line = stats_file.readline()
            if not line:
                raise Exception("Empty stats.txt, try using the --verbose flag to check simulation output")
            while line:
                if line.startswith("simInsts"):
                    instruction_count = int(line.split()[1])
                elif line.startswith("system.cpu.numCycles"):
                    cycle_count = int(line.split()[1])
                    return cycle_count / instruction_count
                line = stats_file.readline()
            if not instruction_count:
                raise Exception("Could not find instruction count in stats.txt")
            elif not cycle_count:
                raise Exception("Could not find cycle count in stats.txt")

    def size_string_to_int(size):
        if size[:-1].isdigit() and size.endswith("B"):
            return int(size[:-1])
        elif size[:-2].isdigit():
            if size.endswith("kB"):
                return int(size[:-2]) * 1024
            elif size.endswith("MB"):
                return int(size[:-2]) * 1024 * 1024
        else:
            raise ValueError(f"Invalid size: {size}")

    def format_time(time_in_seconds):
        if time_in_seconds < 1:
            return f"{time_in_seconds * 1000:.1f}ms"
        elif time_in_seconds < 60:
            return f"{time_in_seconds:.1f}s"
        elif time_in_seconds < 3600:
            if time_in_seconds % 60 < 1:
                return f"{int(time_in_seconds / 60)}m"
            else:
                return f"{int(time_in_seconds / 60)}m {int(time_in_seconds % 60)}s"
        else:
            if time_in_seconds % 3600 < 1:
                return f"{int(time_in_seconds / 3600)}h"
            else:
                return f"{int(time_in_seconds / 3600)}h {int((time_in_seconds % 3600) / 60)}m"

    parser = argparse.ArgumentParser(
        description="Run gem5 simulations for different architectures, benchmarks, and cache sizes.",
        epilog="If no arguments are provided, the script will run all benchmarks for all architectures and a range of cache sizes.",
    )

    parser.add_argument(
        "-a",
        "--architectures",
        help="Architectures to run the simulations for.",
        action="store",
        default=["X86", "ARM"],
        choices=["X86", "ARM"],
        type=str.upper,
        nargs="+",
    )
    parser.add_argument(
        "-b",
        "--benchmarks",
        help="Benchmarks to run the simulations for.",
        action="store",
        default=["crc", "susan"],
        choices=["crc", "susan"],
        type=str.lower,
        nargs="+",
    )
    parser.add_argument(
        "-is",
        "--icache_sizes",
        help="Instruction cache sizes to run the simulations for.",
        action="store",
        default=[f"{2**i}kB" for i in range(1, 6)],
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "-ds",
        "--dcache_sizes",
        help="Data cache sizes to run the simulations for.",
        default=[f"{2**i}kB" for i in range(1, 7)],
        action="store",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "-da",
        "--dcache_associativity",
        help="Associativity of the data cache to run the simulations for.",
        action="store",
        default=[2**i for i in range(5)],
        choices=[2**i for i in range(5)],
        type=int,
        nargs="+"
    )
    parser.add_argument(
        "-cs",
        "--cacheline_sizes",
        help="Cacheline sizes to run the simulations for.",
        action="store",
        default=[2**i for i in range(4, 8)],
        choices=[2**i for i in range(4, 8)],
        type=int,
    )
    parser.add_argument(
        "-bs",
        "--benchmark_size",
        help="Size of the input data for the benchmarks.",
        action="store",
        default="small",
        choices=["small", "large"],
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output_file",
        help="Output file for the results of the simulations.",
        action="store",
        default="results.csv",
        type=str,
    )
    parser.add_argument(
        "-ap",
        "--append",
        help="Append to the output file rather than overwriting.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Print the output of the simulations.",
        action="store_true",
    )

    args = parser.parse_args()

    print("Running with the following parameters:")
    print(f"  architectures: {args.architectures}")
    print(f"  benchmarks: {args.benchmarks}")
    print(f"  icache_sizes: {args.icache_sizes}")
    print(f"  dcache_sizes: {args.dcache_sizes}")
    print(f"  dcache_associativity: {args.dcache_associativity}")
    print(f"  cacheline_size: {args.cacheline_sizes}")
    print(f"  benchmark_size: {args.benchmark_size}")
    print(f"  output_file: {args.output_file}")
    print(f"  append: {args.append}")
    print(f"  verbose: {args.verbose}")

    if not path.exists("out"):
        makedirs("out")
    args.output_file = "out/" + args.output_file
    if not args.output_file.endswith(".csv"):
        args.output_file += ".csv"
    if not args.append and path.exists(args.output_file):
        if input(f"File '{args.output_file}' already exists. Overwrite? [y/N]: ") != "y":
            exit()
    elif args.append and not path.exists(args.output_file):
        print(f"File '{args.output_file}' does not exist. Creating it.")
        args.append = False

    with open(args.output_file, "a" if args.append else "w") as output_file:
        if not args.append:
            output_file.write(
                "Architecture,Benchmark,Instruction Cache Size [B],Data Cache Size [B],Data Cache Associativity,Cache Line Size [B],CPI\n"
            )
            output_file.flush()
        script_start = time()
        for architecture in args.architectures:
            for benchmark in args.benchmarks:
                for icache_size in args.icache_sizes:
                    for dcache_size in args.dcache_sizes:
                        for dcache_associativity in args.dcache_associativity:
                            for cacheline_size in args.cacheline_sizes:
                                print(
                                    f"Simulating {benchmark.lower()} on {architecture.upper()} with {icache_size} icache, {dcache_size} dcache, dcache associativity of {dcache_associativity}, and {cacheline_size} cachelines...",
                                    end=" ",
                                )
                                stdout.flush()
                                simulation_start = time()
                                run_benchmark(architecture, benchmark, icache_size, dcache_size, dcache_associativity, cacheline_size)
                                simulation_end = time()
                                print(f"Done. ({format_time(simulation_end - simulation_start)})")
                                output_file.write(
                                    f"{architecture.upper()},{benchmark.lower()},{size_string_to_int(icache_size)},{size_string_to_int(dcache_size)},{dcache_associativity},{cacheline_size},{cpi()}\n"
                                )
                                output_file.flush()
        script_end = time()
        print(f"Script complete. Total time taken: {format_time(script_end - script_start)}")

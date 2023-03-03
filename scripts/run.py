import argparse
from os import path, makedirs
from sys import stdout
from time import time
import subprocess
from re import match


def run_simulation(
    architecture,
    benchmark,
    benchmark_size,
    variables,
    verbose,
):
    if benchmark.lower() == "dummy":
        binary = "benchmarks/dummy/dummy"
        arguments = [""]
    elif benchmark.lower() == "susan":
        susan_path = f"benchmarks/susan"
        binary = f"{susan_path}/susan"
        arguments = [
            f"{susan_path}/input_{benchmark_size}.pgm {susan_path}/output_{benchmark_size}.smoothing.pgm -s",
            f"{susan_path}/input_{benchmark_size}.pgm {susan_path}/output_{benchmark_size}.edges.pgm -e",
            f"{susan_path}/input_{benchmark_size}.pgm {susan_path}/output_{benchmark_size}.corners.pgm -c",
        ]
    elif benchmark.lower() == "crc":
        binary = "benchmarks/CRC32/crc"
        arguments = [f"benchmarks/adpcm/data/{benchmark_size}.pcm"]
    else:
        raise Exception(f"Invalid benchmark '{benchmark}'")

    if architecture.upper() == "ARM":
        binary = f"{binary}.arm"
    elif architecture.upper() != "X86":
        raise Exception(f"Invalid architecture '{architecture}'")

    for variable in variables:
        if variable.units == "B":
            size_pattern = r"^\d+(k|M)?B$"
            if not match(size_pattern, variable.value):
                raise Exception(f"Invalid {variable.name} '{variable.value}'")
            variable_size = size_string_to_int(variable.value)
            if not (
                variable_size != 0 and ((variable_size & (variable_size - 1)) == 0)
            ):
                raise Exception(
                    f"{variable.name} '{variable.value}' is not a power of 2"
                )

    for argument in arguments:
        command = [
            f"gem5/build/{architecture.upper()}/gem5.opt",
            "--outdir=gem5/m5out",
            "gem5/configs/example/se.py",
            f"--cmd={binary}",
            f"--options={argument}",
            "--cpu-type=TimingSimpleCPU",
            "--caches",
        ]
        for variable in variables:
            command.append(f"--{variable.argument}={variable.value}")
        output = subprocess.PIPE if not verbose else None
        process = subprocess.Popen(command, stdout=output, stderr=output)
        try:
            process.wait()
        except KeyboardInterrupt:
            process.terminate()
            exit()


def get_statistic(statistic):
    with open("gem5/m5out/stats.txt", "r") as stats_file:
        line = stats_file.readline()
        if not line:
            raise Exception(
                "Empty stats.txt, try using the --verbose flag to check simulation output"
            )
        while line:
            if statistic == "cpi":
                if line.startswith("simInsts"):
                    instruction_count = int(line.split()[1])
                elif line.startswith("system.cpu.numCycles"):
                    cycle_count = int(line.split()[1])
                    return float(cycle_count / instruction_count)
            elif statistic == "overall_dcache_miss_rate":
                if line.startswith("system.cpu.dcache.overallMissRate::cpu.data"):
                    return float(line.split()[1])
            line = stats_file.readline()
        if statistic == "cpi":
            if not instruction_count:
                raise Exception("Could not find instruction count in stats.txt")
            elif not cycle_count:
                raise Exception("Could not find cycle count in stats.txt")
        elif statistic == "overall_dcache_miss_rate":
            raise Exception("Could not find overall dcache miss rate in stats.txt")


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
            return (
                f"{int(time_in_seconds / 3600)}h {int((time_in_seconds % 3600) / 60)}m"
            )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--test",
        help="Test script using a dummy binary.",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--parts",
        help="Parts of the assignment to run.",
        action="store",
        default=["a", "b"],
        choices=["a", "b", "1", "2"],
        type=str.lower,
        nargs="+",
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
        nargs="+",
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
        "--output_directory",
        help="Output directory for the results of the simulations.",
        action="store",
        default="results",
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

    if args.test:
        args.benchmarks = ["dummy"]

    args.parts = [part.replace("1", "a").replace("2", "b") for part in args.parts]

    print("Running with the following parameters:")
    print(f"  test: {args.test}")
    print(f"  parts: {args.parts}")
    print(f"  architectures: {args.architectures}")
    print(f"  benchmarks: {args.benchmarks}")
    if "a" in args.parts:
        print(f"  icache_sizes: {args.icache_sizes}")
        print(f"  dcache_sizes: {args.dcache_sizes}")
    if "b" in args.parts:
        print(f"  dcache_associativity: {args.dcache_associativity}")
        print(f"  cacheline_size: {args.cacheline_sizes}")
    print(f"  benchmark_size: {args.benchmark_size}")
    print(f"  output_directory: {args.output_directory}")
    print(f"  append: {args.append}")
    print(f"  verbose: {args.verbose}")
    input("Press enter to confirm and continue... ")

    args.output_directory = f"out/{args.output_directory}"
    if not path.exists(args.output_directory):
        makedirs(args.output_directory)
    elif not args.append and (
        input(f"Directory '{args.output_directory}' already exists. Overwrite? [y/N]: ")
        != "y"
    ):
        exit()

    class Part:
        def __init__(self, output_file, variables, statistic):
            self.output_file = output_file
            self.variables = variables
            self.statistic = statistic

    class Variable:
        def __init__(self, value, argument, name, units=None):
            self.value = value
            self.argument = argument
            self.name = name
            self.units = units

    parts = {}
    for part in args.parts:
        output_file = open(
            f"{args.output_directory}/part_{part}.csv", "a" if args.append else "w"
        )
        if part == "a":
            variables = [
                Variable(args.icache_sizes, "l1i_size", "ICache Size", "B"),
                Variable(args.dcache_sizes, "l1d_size", "DCache Size", "B"),
            ]
            statistic = "Cycles Per Instruction"
        elif part == "b":
            variables = [
                Variable(
                    args.dcache_associativity, "l1d_assoc", "DCache Associativity"
                ),
                Variable(args.cacheline_sizes, "cacheline_size", "Cacheline Size"),
            ]
            statistic = "Overall DCache Miss Rate"
        if not args.append:
            output_file.write(
                "Architecture,Benchmark,"
                + ",".join(
                    variable.name
                    + (
                        f"({variable.units})"
                        if variable.units
                        else ""
                    )
                    for variable in variables
                )
                + f",{statistic}\n"
            )
        parts[part] = Part(output_file, variables, statistic)

    script_start = time()
    for architecture in args.architectures:
        for benchmark in args.benchmarks:
            for part in parts.values():
                for variable_value_0 in part.variables[0].value:
                    for variable_value_1 in part.variables[1].value:
                        variables = (
                            Variable(
                                variable_value_0,
                                part.variables[0].argument,
                                part.variables[0].name,
                                part.variables[0].units,
                            ),
                            Variable(
                                variable_value_1,
                                part.variables[1].argument,
                                part.variables[1].name,
                                part.variables[1].units,
                            ),
                        )
                        print(
                            f"Architecture: {architecture}, Benchmark: {benchmark}, "
                            + ", ".join(
                                f"{variable.name}: {variable.value}"
                                for variable in variables
                            ),
                            end="... ",
                            flush=True,
                        )
                        simulation_start = time()
                        run_simulation(
                            architecture,
                            benchmark,
                            args.benchmark_size,
                            variables,
                            args.verbose,
                        )
                        simulation_end = time()
                        print(
                            f"done. ({format_time(simulation_end - simulation_start)})"
                        )
                        part.output_file.write(
                            f"{architecture},{benchmark},"
                            + ",".join(
                                str(size_string_to_int(variable.value))
                                if variable.units == "B"
                                else str(variable.value)
                                for variable in variables
                            )
                            + f",{get_statistic(part.statistic)}\n"
                        )
                        part.output_file.flush()
    script_end = time()
    print(
        f"Script complete! Total time taken: {format_time(script_end - script_start)}"
    )

    for part in parts.values():
        part.output_file.close()


if __name__ == "__main__":
    main()

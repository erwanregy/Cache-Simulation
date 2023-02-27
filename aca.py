#!/usr/bin/python -u

import subprocess, re, sys
from time import time

def run_benchmark(architecture, benchmark, icache_size, dcache_size, test_size, mute_output):
    if benchmark.lower() == "susan":
        susan_path = f"{benchmarks_path}/automotive/susan"
        binary = f"{susan_path}/susan"
        arguments = [
            f"{susan_path}/input_{test_size}.pgm {susan_path}/output_{test_size}.smoothing.pgm -s",
            f"{susan_path}/input_{test_size}.pgm {susan_path}/output_{test_size}.edges.pgm -e",
            f"{susan_path}/input_{test_size}.pgm {susan_path}/output_{test_size}.corners.pgm -c"
        ]
    elif benchmark.lower() == "crc":
        telecomm_path = f"{benchmarks_path}/telecomm"
        binary = f"{telecomm_path}/CRC32/crc"
        arguments = [f"{telecomm_path}/adpcm/data/{test_size}.pcm"]
    else:
        raise Exception(f"Invalid benchmark '{benchmark}'")

    if architecture.lower() == "arm":
        binary = f"{binary}.arm"
    elif architecture.lower() != "x86":
        raise Exception(f"Invalid architecture '{architecture}'")
    
    cache_size_pattern = r"^\d+(k|M|G)?B$"
    if not re.match(cache_size_pattern, icache_size):
        raise Exception(f"Invalid icache size '{icache_size}'")
    elif not re.match(cache_size_pattern, dcache_size):
        raise Exception(f"Invalid dcache size '{dcache_size}'")

    for argument in arguments:
        command = [
            f"{gem5_path}/build/{architecture.upper()}/gem5.opt",
            f"{gem5_path}/configs/example/se.py",
            f"--cmd={binary}",
            f"--options='{argument}'",
            f"--caches",
            f"--l1i_size={icache_size}",
            f"--l1d_size={dcache_size}",
            f"--cpu-type=TimingSimpleCPU",
        ]
        output = subprocess.PIPE if mute_output else None
        proc = subprocess.Popen(command, shell=True, stdout=output, stderr=output)
        try:
            proc.wait()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Command failed with return code {e.returncode}: {e.cmd}")
        except KeyboardInterrupt:
            proc.terminate()
            exit(1)

def cpi():
    with open("m5out/stats.txt", "r") as stats_file:
        while True:
            line = stats_file.readline()
            if line.startswith("simInsts"):
                instruction_count = int(line.split()[1])
                # print(f"Cycles: {cycle_count}")
            elif line.startswith("system.cpu.numCycles"):
                cycle_count = int(line.split()[1])
                # print(f"Instructions: {instruction_count}")
                return cycle_count / instruction_count

def write(string):
    if write_to_file:
        output_file.write(string)
        output_file.flush()
    else:
        print(string, end="")

if __name__ == "__main__":
    gem5_path = "/home/erwan/aca/gem5"
    benchmarks_path = "/home/erwan/aca/benchmarks"

    architectures = [
        "x86",
        # "arm",
    ]
    cache_sizes = [
        "128B",
        "256B",
        "512B",
        "1kB",
        "2kB",
        "4kB",
        "8kB",
        "16kB",
        "32kB",
        "64kB",
        "128kB",
        "256kB",
    ]
    benchmarks = [
        "crc",
        "susan",
    ]

    test_size = "small"
    mute_output = True
    time_executions = True
    write_to_file = True
    append = False
    output_file_name = "results.txt"

    if write_to_file:
        import os
        if os.path.exists(output_file_name):
            user_input = input(f"File '{output_file_name}' already exists. Overwrite? (y/N) ")
            if user_input != "y":
                exit(1)
        if append:
            output_file = open(output_file_name, "a")
        else:
            output_file = open(output_file_name, "w")

    for architecture in architectures:
        write(f"Architecture: {architecture.upper()}\n")
        for benchmark in benchmarks:
            write(f"\tBenchmark: {benchmark.lower()}\n")
            for icache_size in cache_sizes:
                write(f"\t\tIcache: {icache_size}\n")
                for dcache_size in cache_sizes:
                    write(f"\t\t\tDcache: {dcache_size}\n")
                    if time_executions == True:
                        start = time()
                    print(f"Running {benchmark.lower()} on {architecture.upper()} with {icache_size} icache and {dcache_size} dcache... ", end="")
                    sys.stdout.flush()
                    run_benchmark(architecture, benchmark, icache_size, dcache_size, test_size, mute_output)
                    print(f"Done.", end=" " if time_executions == True else None)
                    if time_executions == True:
                        end = time()
                        print(f"({end - start:.1f}s)")
                    write(f"\t\t\t\tCPI: {cpi()}\n")

    if write_to_file:
        output_file.close()
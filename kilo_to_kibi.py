if __name__ == "__main__":
    import csv
    import argparse

    def kilo_to_kibi(size: str) -> str:
        size = float(size)
        if size % 1000 == 0:
            return str(int(size / 1000 * 1024))
        else:
            return str(int(size))
    
    parser = argparse.ArgumentParser(
        description="Run gem5 simulations for different architectures, benchmarks, and cache sizes.",
        epilog="If no arguments are provided, the script will run all benchmarks for all architectures and a range of cache sizes.",
    )

    parser.add_argument(
        "input_file",
        action="store",
        default="./example/results.csv",
        type=str,
        nargs="?",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        action="store",
        default="./out/results_kibi.csv",
        type=str,
        nargs="?",
    )
    
    args = parser.parse_args()
    
    if not args.output_file.endswith(".csv"):
        args.output_file += ".csv"    
       
    with open(args.input_file, "r") as input_file:
        results = list(csv.reader(input_file))
    
    for row in results[1:]:
        row[2] = kilo_to_kibi(row[2])
        row[3] = kilo_to_kibi(row[3])
    
    with open(args.output_file, "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerows(results)

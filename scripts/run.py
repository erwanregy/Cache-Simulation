import sys
sys.path.append("source")
from aca import *

def main():
    arguments = parse_arguments()
    print_arguments(arguments)

    setup_output_directory(arguments)
    parts = setup_parts(arguments)

    run_simulations(arguments, parts)


if __name__ == "__main__":
    main()
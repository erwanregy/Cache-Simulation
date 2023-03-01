# Advanced Computer Architecture Coursework 1 - gem5 Simulation

## Introduction

This repository contains the code for the first coursework of the Advanced Computer Architecture course at the University of Southampton. The aim of the coursework is to simulate a simple x86 and ARM processor in gem5 and compare the performance of the two architectures in terms of CPI when running simple benchmarks (crc and susan) and varying the cache size.

## Repository Structure

The repository is structured as follows:

- `gem5`: gem5 simulator repository.

- `benchmarks`: Benchmarks used in the simulation.

- `scripts`: Scripts used to run simulations and plot results.

## Running the scripts

The simulations can be run by executing the following command:

```bash
python scripts/run_simulations.py
```

Likewise, the results can be plotted using the following command:

```bash
python scripts/plot_results.py
```

## Simulation Parameters

The following arguments can be added when running the `run_simulations` script:

- `architectures`: Architectures to simulate.

- `benchmarks`: Contains the benchmarks to be simulated.

- `icache_sizes`: Instruction cache sizes to simulate.

- `dcache_sizes`: Data cache sizes to simulate.

- `benchmark_size`: Size of the input data to the benchmarks.

- `output_file`: File where the results of the simulations will be written.

- `append`: Append the results to the output file, rather than overwriting.

- `verbose`: Show the output of each gem5 simulation.

- `time`: Time the execution of each simulation and the entire script. By default this is set to true, so adding this argument will instead disable timing.

## Dependencies

The following dependencies are required to run the simulations:

- Python 3.10+

- gem5

## License

The code in this repository is licensed under the MIT license. For more information, see the LICENSE file.

## Author

The code in this repository was developed by [Erwan Régy](https://www.linkedin.com/in/erwanregy/)

## TODO: Simulation Output

The script will run the simulations for the x86 and ARM architectures and will generate the following directories:

### Simulation Results

This directory contains the results of the simulations. The results are stored in the following files:

- `x86_crc.csv`: Contains the CPI for the x86 architecture when running the crc benchmark and varying the cache size.

- `x86_susan.csv`: Contains the CPI for the x86 architecture when running the susan benchmark and varying the cache size.

- `arm_crc.csv`: Contains the CPI for the ARM architecture when running the crc benchmark and varying the cache size.

- `arm_susan.csv`: Contains the CPI for the ARM architecture when running the susan benchmark and varying the cache size.

### Simulations Logs

This directory contains the logs of the simulations. The logs are stored in the following files:

- `x86_crc.log`: Contains the log of the simulation for the x86 architecture when running the crc benchmark and varying the cache size.

- `x86_susan.log`: Contains the log of the simulation for the x86 architecture when running the susan benchmark and varying the cache size.

- `arm_crc.log`: Contains the log of the simulation for the ARM architecture when running the crc benchmark and varying the cache size.

- `arm_susan.log`: Contains the log of the simulation for the ARM architecture when running the susan benchmark and varying the cache size.

### Simulation Plots

This directory contains the plots of the simulations. The plots are stored in the following files:

- `x86_crc.png`: Contains the plot of the CPI for the x86 architecture when running the crc benchmark and varying the cache size.

- `x86_susan.png`: Contains the plot of the CPI for the x86 architecture when running the susan benchmark and varying the cache size.

- `arm_crc.png`: Contains the plot of the CPI for the ARM architecture when running the crc benchmark and varying the cache size.

- `arm_susan.png`: Contains the plot of the CPI for the ARM architecture when running the susan benchmark and varying the cache size.


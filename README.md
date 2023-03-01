# Advanced Computer Architecture Coursework 1 - gem5 Simulation

## Introduction

This repository contains the code for the first coursework of the Advanced Computer Architecture course at the University of Southampton. The aim of the coursework is to simulate a simple x86 and ARM processor in gem5 and compare the performance of the two architectures in terms of CPI when running simple benchmarks (crc and susan) and varying the cache size.

## Repository Structure

The repository is structured as follows:

- `benchmarks`: Contains the source code for the benchmarks used in the simulation.

- `gem5`: Contains the source code for the gem5 simulator.

- `aca.py`: Contains the script used to run the simulations.

## Running the simulations

The simulations can be run by executing the following command:

```bash
python aca.py
```

## Simulation Parameters

The following parameters can be modified in the `aca.py` script:

- `architectures`: Contains the architectures to be simulated.

- `cache_sizes`: Contains the cache sizes to be used in the simulations.

- `benchmarks`: Contains the benchmarks to be simulated.

- `test_size`: Contains the size of the test to be run.

- `mute_output`: If set to `True`, the output of the simulations will be muted.

- `time_executions`: If set to `True`, the execution time of the simulations will be printed.

- `write_to_file`: If set to `True`, the results of the simulations will be written to a file. The file name can be specified using the `output_file_name` parameter. Else, the results will be printed to stdout.

- `append`: If set to `True`, the results of the simulations will be appended to the output file. Else, the file will be overwritten.

- `output_file_name`: Contains the name of the file where the results of the simulations will be written.

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


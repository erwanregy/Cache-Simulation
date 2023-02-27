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

The script will run the simulations for the x86 and ARM architectures and will generate the following directories:

### Simulation Results

This directory contains the results of the simulations. The results are stored in the following files:

- `x86_crc.csv`: Contains the CPI for the x86 architecture when running the crc benchmark and varying the cache size.

- `x86_susan.csv`: Contains the CPI for the x86 architecture when running the susan benchmark and varying the cache size.

- `arm_crc.csv`: Contains the CPI for the ARM architecture when running the crc benchmark and varying the cache size.

- `arm_susan.csv`: Contains the CPI for the ARM architecture when running the susan benchmark and varying the cache size.

### Simulation Logs

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

## Simulation Parameters

The following parameters can be modified in the `aca.py` script:

- `cache_sizes`: Contains the cache sizes to be used in the simulations.

- `num_cpus`: Contains the number of CPUs to be used in the simulations.

- 

## Dependencies

The following dependencies are required to run the simulations:

- Python 2.7

- gem5

- matplotlib

## License

The code in this repository is licensed under the MIT license. For more information, see the LICENSE file.

## Acknowledgements

The code in this repository was developed by:

- [Erwan Régy](https://www.linkedin.com/in/erwanregy/)
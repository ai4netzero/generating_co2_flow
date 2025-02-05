# Parallel Processing of RAW Files with Python

This repository contains a bash script that facilitates the parallel simulation of CO2 given `.raw` files of physical domains using a Python script. The script dynamically creates job-specific directories, copies necessary files, and runs multiple instances of the Python script in parallel using available CPU cores.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Usage](#usage)
- [Script Parameters](#script-parameters)

## Overview
The bash script (`run_jobs.sh`) is designed to process multiple `.raw` files concurrently by distributing the load across available CPU cores. Each `.raw` file is processed in a temporary directory, and the results are stored in a shared destination folder. The Python script that performs the file processing runs within each of these directories, ensuring isolation and preventing file conflicts.

## Requirements
- **Python** 
- **Bash** 
- **OpenFOAM**
- Ensure the following software and libraries are installed:
  - Python 3.11.9 (although it can work on earlier versions)
  - OpenFOAM
  - GeoChemFoam
  - numpy-stl
  - skimage
  - matplotlib

## Usage

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    ```

2. **Configure the Script:**
    - Edit the following parameters inside the `run_jobs.sh` script:
      - `input_directory`: Path to the directory containing the `.raw` input files.
      - `original_dir`: Path to the original directory containing the `script.py` file and other necessary resources.
      - `destination_folder`: Path where all output results will be stored.
      - `total_cores`: Total number of cores available on your machine (or use `$(nproc)` to fetch the core count dynamically). (Practically it should be less than the available cores)
      
3. **Run the Script:**
    Run the bash script to start processing the `.raw` files in parallel:
    ```bash
    ./run_jobs.sh
    ```

## Python Script Parameters

 These parameters are passed to `run_scripts.py`:
  - `--raw_file_path`: Path to the input `.raw` file.
  - `--destination_folder`: Path to the folder for saving results.
  - `--num_processors`: Number of processors (default: 16).
  - `--x_dim`, `--y_dim`, `--z_dim`: Dimensions of the image (default: 1000x1000x6).


## Cropping Parameters
  In the python script you can specify the cropping paramters of the image, for instance:
  
  `x_min,x_max,y_min,y_max= (488,1000,2,514)`


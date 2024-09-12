#!/bin/bash

# Directory containing input files
input_directory="raw_missed_files_Crop10"  # Replace with the actual input directory


# The original directory that contains script.py and other necessary files
original_dir="2D_micromodal"


# Shared destination folder for all results
destination_folder="/data/aa519/postdoc/output_results_all_crop10"  # Replace with the actual destination folder path



# Number of cores each Python script uses
cores_per_job=16

# Total number of cores available on the machine
total_cores=96 #$(nproc)  # Fetches the total number of cores on the machine

# Maximum number of concurrent jobs
max_concurrent_jobs=$((total_cores / cores_per_job))

# Default parameters for Python script
num_processors=$cores_per_job
x_dim=1000
y_dim=1000
z_dim=6

# Function to run a job
run_job() {
    local raw_file_path=$1
    local job_dir=$2
  

    # Copy the original directory into a new job-specific directory
    cp -r "$original_dir" "$job_dir"
    cp "$raw_file_path" "$job_dir"/$original_dir

    # Run the Python script in the new directory with specified parameters
    (
        cd "$job_dir"/$original_dir && \
        source /usr/lib/openfoam/openfoam2212/etc/bashrc
        source $HOME/works/GeoChemFoam-5.1/etc/bashrc
        python run_scripts.py \
            --raw_file_path "$raw_file_path" \
            --destination_folder "$destination_folder" \
            --num_processors "$num_processors" \
            --x_dim "$x_dim" \
            --y_dim "$y_dim" \
            --z_dim "$z_dim" 
                )
}

# Count of currently running jobs
job_count=0

# Iterate over each input file in the directory and run them in parallel
for raw_file_path in "$input_directory"/*; do

    # Create a unique directory for each job
    job_dir=$(mktemp -d -t job_dir_XXXXXX)
    echo -e "Running on " $raw_file_path "in folder" $job_dir

    # Run the job in the background and increment the job count
    run_job "$raw_file_path" "$job_dir" &
    ((job_count++))

    # Check if the maximum number of concurrent jobs is reached
    if ((job_count >= max_concurrent_jobs)); then
        # Wait for any job to finish before starting a new one
        wait -n
        ((job_count--))
    fi
done

# Wait for all remaining jobs to finish
wait

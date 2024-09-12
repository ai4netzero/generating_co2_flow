import argparse
import glob
import os
import shutil
import subprocess

def run_shell_script(script_path):
    """
    Run a shell script using subprocess and print its output.
    :param script_path: Path to the shell script to run.
    :return: None
    """
    try:
        result = subprocess.run(['bash', script_path], check=True, capture_output=True, text=True)
        print(f"Output of {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:\n{e.stderr}")
        exit(1)
        
def run_shell_script(script_path, *args):
    """
    Run a shell script using subprocess and print its output.
    :param script_path: Path to the shell script to run.
    :param args: Arguments to pass to the shell script.
    :return: None
    """
    try:
        # Prepare the command with arguments
        command = ['bash', script_path] + list(args)
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Output of {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:\n{e.stderr}")
        exit(1)

def run_python_script(script_path, *args):
    """
    Run a Python script using subprocess and print its output.
    :param script_path: Path to the Python script to run.
    :param args: Arguments to pass to the Python script.
    :return: None
    """
    try:
        # Prepare the command with arguments
        command = ['python', script_path] + list(args)
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"Output of {script_path}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_path}:\n{e.stderr}")
        exit(1)

if __name__ == "__main__":
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Preprocess images from a source folder and save them to a destination folder.")
    parser.add_argument('--raw_file_path', type=str, help='Path to the source folder containing raw images.')
    parser.add_argument('--destination_folder', type=str, help='Path to the destination folder where hdf5 images will be saved.')
    parser.add_argument('--num_processors', type=int, default=24)
    parser.add_argument('--x_dim', default=1004, type=int, help='dimension x of img')
    parser.add_argument('--y_dim', default=1004, type=int, help='dimension y of img')
    parser.add_argument('--z_dim', default=6, type=int, help='dimension z of img')

    opt = parser.parse_args()
    
   
    #cropping_combinations = [(2,514,2,514)]
    #cropping_combinations = [(488,1000,2,514)]

    # image dimension
    x_dim=opt.x_dim
    y_dim=opt.y_dim
    z_dim=opt.z_dim
    
    # Create the destination folder if it doesn't exist
    os.makedirs(opt.destination_folder, exist_ok=True)
    

    # Loop over all files in the source folder (these should be all raw files)
    
    # get image name 
    image_name = os.path.splitext(os.path.basename(opt.raw_file_path))[0]
    
    print(image_name)

    #x_min,x_max,y_min,y_max= (2,514,2,514)
    x_min,x_max,y_min,y_max= (488,1000,2,514)
    
    # List of shell scripts to run (script name, its arguments)
    shell_scripts = [('_1createMesh_unix.sh', image_name,str(x_dim),str(y_dim),str(z_dim),str(x_min),str(x_max),str(y_min),str(y_max),str(opt.num_processors)),
                        ('_2runSnappyHexMesh_unix.sh',) ,('_3initCaseSPFlow_unix.sh',),
                        ('_4runCaseSPFlow_unix.sh',), ('_5processSPFlow_unix.sh',),
                        ('_6initCaseTPFlow_unix.sh',),
                        ('_7runCaseTPFlow_unix.sh',),
                        ('_8processTPFlow_unix.sh',),
                        ('_9postprocess_unix.sh',)]
    
    #shell_scripts = [('_8processTPFlow_unix.sh',),
    #                 ('_9postprocess_unix.sh',)]
    
    #shell_scripts = []
    # Run each shell script

    for shell_script, *args in shell_scripts:
        run_shell_script(shell_script, *args)

    dest_path = os.path.join(opt.destination_folder,image_name+'.hdf5')

    # Run a Python script
    python_script = 'writeUPAlphaHdf5.py'
    python_args = ['--x_min', '0', '--x_max', '512', '--y_min', '0', '--y_max', '512',
            '--res', '0.000035','--output_filename',dest_path]
    
    run_python_script(python_script,*python_args)
    
    # new folder to store relperm.csv and poroPerm.csv
    folder_for_csv_files = os.path.join(opt.destination_folder, image_name+'_csv_files')
    os.makedirs(folder_for_csv_files, exist_ok=True)
    # Move all CSV files from source to destination
    [shutil.move(f, folder_for_csv_files) for f in glob.glob('*.csv')]


    # Run another shell script after the Python script
    final_shell_script = 'deleteAll.sh'
    run_shell_script(final_shell_script)

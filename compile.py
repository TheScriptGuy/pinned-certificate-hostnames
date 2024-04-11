import argparse
import os
import hashlib
from datetime import datetime
import pytz

def read_file_content(file_path: str) -> str:
    """Reads and returns the content of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def calculate_file_hash(file_path: str) -> str:
    """Calculates and returns the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def compile_directory_contents(dir_path: str, depth: int = 0, accumulated_path: str = "") -> list:
    """
    Recursively walks through directories, compiling contents of 'header' and 'hostnames' files,
    and includes the directory names in the output with appropriate depth indication.
    
    Args:
    - dir_path (str): The path to the directory to start the walk from.
    - depth (int): The current depth of the recursion.
    - accumulated_path (str): Accumulated path names formatted with depth.
    
    Returns:
    - list: A list of compiled contents, including directory names and file contents.
    """
    compiled_contents = []
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    # Only append directory names if not at the root
    if depth > 0:
        # Format directory name with appropriate depth
        dir_name = os.path.basename(dir_path)
        accumulated_path += f"{'#' * depth} {dir_name}\n"

    entries = sorted(os.listdir(dir_path), key=lambda x: x.lower())
    has_subdirectories = any(os.path.isdir(os.path.join(dir_path, entry)) for entry in entries)
    
    for entry in entries:
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            compiled_contents += compile_directory_contents(full_path, depth + 1, accumulated_path)
    
    # If at an "end directory", compile header and hostnames
    if not has_subdirectories:
        header_path = os.path.join(dir_path, 'header')
        hostnames_path = os.path.join(dir_path, 'hostnames')
        if os.path.isfile(header_path) and os.path.isfile(hostnames_path):
            header_content = read_file_content(header_path)
            header_content = f"{'#' * (depth + 1)} {header_content}"
            hostnames_content = read_file_content(hostnames_path)
            # Add directory structure and file contents
            compiled_contents.append(f"{accumulated_path}{header_content}{hostnames_content}\n")
    
    return compiled_contents if depth == 0 else compiled_contents

def write_compiled_list(dir_path: str):
    try:
        compiled_list = compile_directory_contents(dir_path)
        if not compiled_list:
            print("No valid header and hostnames files found in the directory tree.")
            return
        
        timestamp = datetime.now(pytz.timezone("UTC")).strftime("# List compiled on %Y-%m-%d %H:%M:%S %Z\n")
        
        with open('compiled-with-comments.txt', 'w') as file:
            file.write(timestamp)
            file.writelines(compiled_list)

        # Prepare list for compiled-excluding-comments.txt
        # Flatten the list, remove lines starting with '#', and sort
        flat_list = "\n".join(compiled_list).split("\n")
        filtered_list = [line for line in flat_list if not line.strip().startswith('#') and line.strip() != '']
        sorted_filtered_list = sorted(filtered_list, key=lambda x: x.lower())
        print(f"Number of hostnames found: {len(sorted_filtered_list)}")

        # Write to compiled-excluding-comments.txt excluding comments and sorted
        with open('compiled-without-comments.txt', 'w') as file:
            file.write(timestamp)
            for line in sorted_filtered_list:
                file.write(f"{line}\n")

        # Write a Palo Alto Networks specific exclude list.
        with open('panw-compiled-without-comments.txt', 'w') as panw_file:
            panw_file.write(timestamp)
            for line in sorted_filtered_list:
                panw_file.write(f"{line}/\n")

        # Calculate hashes and write to file-validation.hash
        hash_file = 'file-validation.hash'
        with open(hash_file, 'w') as hashfile:
            for filename in ['compiled-with-comments.txt', 'compiled-without-comments.txt', 'panw-compiled-without-comments.txt']:
                hash_val = calculate_file_hash(filename)
                hashfile.write(f"{hash_val}  {filename}\n")

    except FileNotFoundError as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description='Compile directory contents with structure representation.')
    parser.add_argument('directory', type=str, help='The path to the directory to start the compilation from.')
    
    args = parser.parse_args()
    
    write_compiled_list(args.directory)

if __name__ == '__main__':
    main()


import hashlib
import os
import pickle

# Displaying a custom banner
def display_banner():
    banner = """
    ______ _ _        _____      _                  _ _           _____ _               _             
    |  ___(_) |      |_   _|    | |                (_) |         /  __ \ |             | |            
    | |_   _| | ___    | | _ __ | |_ ___  __ _ _ __ _| |_ _   _  | /  \/ |__   ___  ___| | _____ _ __ 
    |  _| | | |/ _ \   | || '_ \| __/ _ \/ _` | '__| | __| | | | | |   | '_ \ / _ \/ __| |/ / _ \ '__|
    | |   | | |  __/  _| || | | | ||  __/ (_| | |  | | |_| |_| | | \__/\ | | |  __/ (__|   <  __/ |   
    \_|   |_|_|\___|  \___/_| |_|\__\___|\__, |_|  |_|\__|\__, |  \____/_| |_|\___|\___|_|\_\___|_|   
                                          __/ |            __/ |                                      
                                         |___/            |___/                                       
    """
    print(banner)

# Function to calculate the hash of a file
def calculate_file_hash(file_path):
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read the file in chunks to avoid memory overload
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

# Function to check the integrity of files
def check_file_integrity(files, hash_file):
    current_hashes = {}
    
    # Calculate the current hash for each file
    for file_path in files:
        if os.path.exists(file_path):
            current_hashes[file_path] = calculate_file_hash(file_path)
        else:
            print(f"File {file_path} does not exist.")
    
    # Load stored hashes and compare
    try:
        with open(hash_file, 'rb') as f:
            stored_hashes = pickle.load(f)
    except FileNotFoundError:
        stored_hashes = {}

    # Compare stored and current hashes
    for file_path, current_hash in current_hashes.items():
        if file_path not in stored_hashes:
            print(f"New file detected: {file_path}")
        elif stored_hashes[file_path] != current_hash:
            print(f"File modified: {file_path}")
        else:
            print(f"File unchanged: {file_path}")
    
    # Save the current hashes for future comparison
    with open(hash_file, 'wb') as f:
        pickle.dump(current_hashes, f)

# Main function
def main():
    # Display the banner
    display_banner()
    
    # Example file paths (can be a list of files or directory scanning)
    files_to_monitor = ["file1.txt", "file2.txt", "example.txt"]  # Add your file paths here
    hash_storage_file = "file_hashes.pkl"
    
    check_file_integrity(files_to_monitor, hash_storage_file)

if __name__ == "__main__":
    main()

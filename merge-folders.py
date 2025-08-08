import os
import shutil

def get_user_input():
    """Get user input for paths and merge type"""
    print("=== Folder Merge Script ===\n")
    
    # Get source path
    while True:
        source_path = input("Enter source path (containing folders to merge): ").strip()
        if not source_path:
            print("Please enter a valid path.")
            continue
        if not os.path.exists(source_path):
            print(f"Error: Path '{source_path}' does not exist!")
            continue
        if not os.path.isdir(source_path):
            print(f"Error: '{source_path}' is not a directory!")
            continue
        break
    
    # Get destination path
    while True:
        dest_path = input("Enter destination path (where merged files will go): ").strip()
        if not dest_path:
            print("Please enter a valid path.")
            continue
        break
    
    # Get merge type
    while True:
        print("\nMerge options:")
        print("1. Merge entire folder structures (preserves directory hierarchy)")
        print("2. Merge contents only (flattens all files into destination folder)")
        choice = input("Choose option (1 or 2): ").strip()
        
        if choice == "1":
            merge_type = "structure"
            break
        elif choice == "2":
            merge_type = "contents"
            break
        else:
            print("Please enter 1 or 2.")
    
    return source_path, dest_path, merge_type

def merge_with_structure(base_source_path, destination_path, destination_folder_name):
    """Merge folders preserving directory structure"""
    print(f"\n--- Merging with folder structure preserved ---")
    
    # Get all folders in the base path except the destination folder
    try:
        all_items = os.listdir(base_source_path)
        folders = [
            os.path.join(base_source_path, f)
            for f in all_items
            if os.path.isdir(os.path.join(base_source_path, f)) and f != destination_folder_name
        ]
    except Exception as e:
        print(f"Error listing directories: {e}")
        return 0, 0, 1
    
    total_copied = 0
    total_replaced = 0
    total_errors = 0
    
    for folder in folders:
        print(f"\nProcessing folder: {os.path.basename(folder)}")
        
        try:
            for root, dirs, files in os.walk(folder):
                for file_name in files:
                    try:
                        source_file_path = os.path.join(root, file_name)

                        # Get the relative path from base source to the file
                        relative_path = os.path.relpath(source_file_path, base_source_path)

                        # Construct destination path using that relative structure
                        destination_file_path = os.path.join(destination_path, relative_path)

                        # Create directory if it doesn't exist
                        dest_dir = os.path.dirname(destination_file_path)
                        os.makedirs(dest_dir, exist_ok=True)

                        # If destination file doesn't exist, copy it
                        if not os.path.exists(destination_file_path):
                            shutil.copy2(source_file_path, destination_file_path)
                            print(f"Copied: {relative_path}")
                            total_copied += 1
                        else:
                            # If the existing destination is not a file, replace it
                            if not os.path.isfile(destination_file_path):
                                shutil.copy2(source_file_path, destination_file_path)
                                print(f"Replaced: {relative_path}")
                                total_replaced += 1
                            else:
                                print(f"Skipped (already exists): {relative_path}")
                                
                    except PermissionError as e:
                        print(f"Permission error with file '{file_name}': {e}")
                        total_errors += 1
                    except Exception as e:
                        print(f"Error processing file '{file_name}': {e}")
                        total_errors += 1
                        
        except Exception as e:
            print(f"Error processing folder '{folder}': {e}")
            total_errors += 1
    
    return total_copied, total_replaced, total_errors

def merge_contents_only(base_source_path, destination_path, destination_folder_name):
    """Merge only file contents, flattening directory structure"""
    print(f"\n--- Merging contents only (flattened) ---")
    
    # Get all folders in the base path except the destination folder
    try:
        all_items = os.listdir(base_source_path)
        folders = [
            os.path.join(base_source_path, f)
            for f in all_items
            if os.path.isdir(os.path.join(base_source_path, f)) and f != destination_folder_name
        ]
    except Exception as e:
        print(f"Error listing directories: {e}")
        return 0, 0, 1
    
    total_copied = 0
    total_replaced = 0
    total_errors = 0
    
    for folder in folders:
        print(f"\nProcessing folder: {os.path.basename(folder)}")
        
        try:
            for root, dirs, files in os.walk(folder):
                for file_name in files:
                    try:
                        source_file_path = os.path.join(root, file_name)

                        # Just use the filename (flatten the directory structure)
                        destination_file_path = os.path.join(destination_path, file_name)

                        # If destination file doesn't exist, copy it
                        if not os.path.exists(destination_file_path):
                            shutil.copy2(source_file_path, destination_file_path)
                            print(f"Copied: {file_name}")
                            total_copied += 1
                        else:
                            # Handle filename conflicts
                            if os.path.isfile(destination_file_path):
                                # File exists, create a unique name
                                base_name, ext = os.path.splitext(file_name)
                                counter = 1
                                original_dest_path = destination_file_path
                                while os.path.exists(destination_file_path):
                                    new_name = f"{base_name}_{counter}{ext}"
                                    destination_file_path = os.path.join(destination_path, new_name)
                                    counter += 1
                                
                                shutil.copy2(source_file_path, destination_file_path)
                                print(f"Copied with new name: {file_name} → {os.path.basename(destination_file_path)}")
                                total_copied += 1
                            else:
                                print(f"Skipped (already exists): {file_name}")
                                
                    except PermissionError as e:
                        print(f"Permission error with file '{file_name}': {e}")
                        total_errors += 1
                    except Exception as e:
                        print(f"Error processing file '{file_name}': {e}")
                        total_errors += 1
                        
        except Exception as e:
            print(f"Error processing folder '{folder}': {e}")
            total_errors += 1
    
    return total_copied, total_replaced, total_errors

def merge_folders():
    """Main function to merge folders based on user input"""
    
    # Get user input
    base_source_path, destination_path, merge_type = get_user_input()
    
    # Extract destination folder name from path
    destination_folder_name = os.path.basename(destination_path.rstrip('/\\'))
    
    # Check if base source path exists
    if not os.path.exists(base_source_path):
        print(f"Error: Base source path '{base_source_path}' does not exist!")
        return
    
    # Create destination directory if it doesn't exist
    os.makedirs(destination_path, exist_ok=True)
    print(f"Destination path: {destination_path}")
    print(f"Destination folder name: {destination_folder_name}")
    
    # Get all folders in the base path except the destination folder
    try:
        all_items = os.listdir(base_source_path)
        folders = [
            os.path.join(base_source_path, f)
            for f in all_items
            if os.path.isdir(os.path.join(base_source_path, f)) and f != destination_folder_name
        ]
        
        print(f"Found {len(folders)} folders to process:")
        for folder in folders:
            print(f"  - {os.path.basename(folder)}")
        
        if not folders:
            print("No folders found to merge!")
            return
            
    except PermissionError as e:
        print(f"Permission error accessing '{base_source_path}': {e}")
        return
    except Exception as e:
        print(f"Error listing directories: {e}")
        return
    
    # Perform merge based on user choice
    if merge_type == "structure":
        total_copied, total_replaced, total_errors = merge_with_structure(
            base_source_path, destination_path, destination_folder_name
        )
    else:  # merge_type == "contents"
        total_copied, total_replaced, total_errors = merge_contents_only(
            base_source_path, destination_path, destination_folder_name
        )
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Files copied: {total_copied}")
    print(f"Files replaced: {total_replaced}")
    print(f"Errors encountered: {total_errors}")
    
    if total_errors == 0:
        print("✅ Merge completed successfully!")
    else:
        print("⚠️  Merge completed with some errors.")

if __name__ == "__main__":
    try:
        merge_folders()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    
    input("\nPress Enter to exit...")
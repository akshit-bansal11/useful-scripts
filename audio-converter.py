import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

def check_ffmpeg() -> bool:
    """Check if FFmpeg is available in the system."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_audio_files(source_path: str, mode: str) -> List[Path]:
    """Get audio files based on mode and automatically detect formats."""
    audio_extensions = {'.wav', '.mp3', '.flac', '.aac', '.ogg', '.m4a', '.wma'}
    
    audio_files = []
    source_path = Path(source_path).resolve()  # Normalize and resolve path
    
    if mode == "single":
        if source_path.is_file():
            if source_path.suffix.lower() in audio_extensions:
                audio_files.append(source_path)
            else:
                print(f"Warning: '{source_path.name}' may not be a supported audio file.")
                audio_files.append(source_path)  # Still try to convert it
        else:
            print(f"Error: '{source_path}' is not a file!")
    else:  # folder mode
        if not source_path.is_dir():
            print(f"Error: '{source_path}' is not a directory!")
            return []
        for file_path in source_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in audio_extensions:
                audio_files.append(file_path)
    
    return audio_files

def validate_output_format(fmt: str) -> bool:
    """Check if the output format is supported by FFmpeg."""
    supported_formats = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'}
    return fmt.lower() in supported_formats

def get_user_input() -> Tuple[str, str, str, str, str, bool, int, int]:
    """Get user input for paths and conversion settings."""
    print("=== Audio File Converter ===\n")
    
    # Choose conversion mode
    while True:
        print("Conversion mode:")
        print("1. Convert a single file")
        print("2. Convert all files in a folder")
        mode_choice = input("Choose mode (1 or 2): ").strip()
        if mode_choice in ("1", "2"):
            mode = "single" if mode_choice == "1" else "folder"
            break
        print("Please enter 1 or 2.")
    
    # Get source path based on mode
    while True:
        source_path = input("Enter path to audio file: " if mode == "single" else
                           "Enter source folder (containing audio files to convert): ").strip()
        if not source_path:
            print("Please enter a valid path.")
            continue
        source_path = str(Path(source_path).resolve())  # Normalize path
        if not os.path.exists(source_path):
            print(f"Error: Path '{source_path}' does not exist!")
            continue
        if mode == "single" and not os.path.isfile(source_path):
            print(f"Error: '{source_path}' is not a file!")
            continue
        if mode == "folder" and not os.path.isdir(source_path):
            print(f"Error: '{source_path}' is not a directory!")
            continue
        break
    
    # Get destination path
    default_dest = os.path.dirname(source_path) if mode == "single" else source_path
    while True:
        dest_path = input(f"Enter destination folder (default: {default_dest}): ").strip()
        dest_path = dest_path or default_dest
        dest_path = str(Path(dest_path).resolve())  # Normalize path
        try:
            os.makedirs(dest_path, exist_ok=True)
            test_file = os.path.join(dest_path, ".test_write")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            break
        except (OSError, PermissionError) as e:
            print(f"Error: Cannot write to '{dest_path}': {e}")
    
    # Get output format
    print("\nSupported output formats:")
    output_formats = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
    for i, fmt in enumerate(output_formats, 1):
        print(f"{i}. {fmt.upper()}")
    print("7. Custom format")
    
    while True:
        choice = input("Choose output format (1-7): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 6:
            output_format = output_formats[int(choice) - 1]
            break
        elif choice == "7":
            custom_format = input("Enter custom format (e.g., mp4): ").strip()
            if not custom_format.startswith('.'):
                custom_format = '.' + custom_format
            if validate_output_format(custom_format):
                output_format = custom_format.lower()
                break
            print(f"Error: '{custom_format}' is not a supported audio format.")
        else:
            print("Please enter a number between 1-7.")
    
    # Get quality setting
    quality_map = {'1': '0', '2': '2', '3': '4', '4': '6', '5': '9'}
    quality_param = "-q:a" if output_format in ('.mp3', '.aac', '.m4a') else "-compression_level"
    
    print("\nAudio quality options:")
    print("1. Highest quality (0)")
    print("2. High quality (2)")
    print("3. Medium quality (4)")
    print("4. Low quality (6)")
    print("5. Lowest quality (9)")
    print("6. Custom quality")
    
    while True:
        choice = input("Choose quality (1-6): ").strip()
        if choice in quality_map:
            quality = quality_map[choice]
            break
        elif choice == "6":
            while True:
                custom_quality = input("Enter quality (0-9, 0=highest, 9=lowest): ").strip()
                if custom_quality.isdigit() and 0 <= int(custom_quality) <= 9:
                    quality = custom_quality
                    break
                print("Please enter a number between 0-9.")
            break
        print("Please enter a number between 1-6.")
    
    # Get bitrate (optional)
    while True:
        bitrate = input("Enter bitrate (e.g., 192k, leave blank for default): ").strip()
        if not bitrate or bitrate.lower().endswith('k') and bitrate[:-1].isdigit():
            break
        print("Please enter a valid bitrate (e.g., 192k) or leave blank.")
    
    # Get sample rate (optional)
    while True:
        sample_rate = input("Enter sample rate (e.g., 44100, leave blank for default): ").strip()
        if not sample_rate or sample_rate.isdigit():
            break
        print("Please enter a valid sample rate (e.g., 44100) or leave blank.")
    
    # Ask about overwriting existing files
    while True:
        overwrite = input("Overwrite existing files? (y/n): ").strip().lower()
        if overwrite in ('y', 'yes', 'n', 'no'):
            overwrite = overwrite in ('y', 'yes')
            break
        print("Please enter 'y' or 'n'.")
    
    return source_path, dest_path, mode, output_format, quality, overwrite, bitrate, sample_rate

def convert_audio_files():
    """Main function to convert audio files based on user input."""
    if not check_ffmpeg():
        print("❌ FFmpeg is not installed or not available in PATH!")
        print("Please install FFmpeg from https://ffmpeg.org/download.html")
        return
    
    print("✅ FFmpeg found!")
    
    # Get user input
    source_path, dest_path, mode, output_format, quality, overwrite, bitrate, sample_rate = get_user_input()
    
    print(f"\nSource: {source_path}")
    print(f"Destination: {dest_path}")
    print(f"Mode: {'Single file' if mode == 'single' else 'Folder'}")
    print(f"Output format: {output_format.upper()}")
    print(f"Quality: {quality} (0=highest, 9=lowest)")
    print(f"Bitrate: {bitrate or 'Default'}")
    print(f"Sample rate: {sample_rate or 'Default'}")
    print(f"Overwrite existing: {'Yes' if overwrite else 'No'}")
    
    # Get all audio files
    try:
        audio_files = get_audio_files(source_path, mode)
        
        if mode == "single":
            print(f"\nFile to convert: {Path(source_path).name}")
            input_format = Path(source_path).suffix.lower()
            print(f"Detected input format: {input_format.upper()}")
        else:
            print(f"\nFound {len(audio_files)} audio files to convert:")
            formats_found = set(file_path.suffix.lower() for file_path in audio_files)
            print(f"Input formats detected: {', '.join(fmt.upper() for fmt in sorted(formats_found))}")
        
        if not audio_files:
            print("No audio files found to process!" if mode == "folder" else
                  "The selected file could not be processed!")
            return
    except Exception as e:
        print(f"Error accessing source path: {e}")
        return
    
    # Convert files
    total_converted = 0
    total_skipped = 0
    total_errors = 0
    
    print(f"\n--- Starting conversion ---")
    
    # Use tqdm for progress bar if available and in folder mode
    file_iter = tqdm(audio_files, desc="Converting", unit="file") if HAS_TQDM and mode == "folder" else audio_files
    
    for file_path in file_iter:
        try:
            # Create output file path
            output_filename = file_path.stem + output_format
            output_path = Path(dest_path) / output_filename
            
            # Skip if file exists and overwrite is disabled
            if output_path.exists() and not overwrite:
                print(f"Skipped (already exists): {file_path.name}")
                total_skipped += 1
                continue
            
            # Skip if input and output are the same
            if file_path.suffix.lower() == output_format.lower() and str(file_path.parent) == dest_path:
                print(f"Skipped (same format and location): {file_path.name}")
                total_skipped += 1
                continue
            
            # Check file size
            if file_path.stat().st_size == 0:
                print(f"Skipped (empty file): {file_path.name}")
                total_skipped += 1
                continue
            
            print(f"Converting: {file_path.name} → {output_filename}")
            
            # Build FFmpeg command
            cmd = ["ffmpeg", "-i", str(file_path), "-map_metadata", "0"]
            if overwrite:
                cmd.append("-y")
            
            # Add quality or compression level based on format
            if output_format in ('.mp3', '.aac', '.m4a'):
                cmd.extend(["-q:a", quality])
            elif output_format == '.flac':
                cmd.extend(["-compression_level", quality])
            
            # Add bitrate if specified
            if bitrate:
                cmd.extend(["-b:a", bitrate])
            
            # Add sample rate if specified
            if sample_rate:
                cmd.extend(["-ar", sample_rate])
            
            cmd.append(str(output_path))
            
            # Execute FFmpeg command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Successfully converted: {file_path.name}")
                total_converted += 1
            else:
                print(f"❌ Error converting {file_path.name}")
                error_lines = result.stderr.strip().split('\n')
                relevant_errors = [line for line in error_lines if 'error' in line.lower() or 'invalid' in line.lower()]
                if relevant_errors:
                    print(f"   Error: {relevant_errors[-1]}")
                total_errors += 1
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {e}")
            total_errors += 1
    
    # Print summary
    print(f"\n=== Conversion Summary ===")
    print(f"Files converted: {total_converted}")
    print(f"Files skipped: {total_skipped}")
    print(f"Errors encountered: {total_errors}")
    print(f"Total files processed: {len(audio_files)}")
    print("✅ Conversion completed successfully!" if total_errors == 0 else
            "⚠️  Conversion completed with some errors.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        convert_audio_files()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
# useful-scripts
A grand repository of useful scripts you can use to run insane tasks.

---

# Available Scripts

## Merge Folders
A script that allows you to merge two or more folders or their content into a new folder.  
(Yes, it can merge an infinite number of folders!)

### Steps
1. **Download the script:** `merge-folders.py`
2. **Make sure Python 3 is installed**
    ```bash
    python --version
    ```
    You should get something like this:
    ```bash
    Python 3.x.x
    ```
3. **Run the script** using cmd, PowerShell, bash, etc.
    ```bash
    python merge-folders.py
    ```
4. **Follow the steps in the output terminal** and provide these inputs:
    - **Source path** (where all the folders are located)
    - **Destination path** (where you want all the folders or content to be merged)
    - **Select the 2nd option** (merge contents), as the 1st option (merge folder structure) is less practical

> **Note:** The folder structure merge functionality might seem unnecessary since copying folders manually achieves the same result.  
It was included in the script's early design, but the content merge option is typically more useful.  
Let's just overlook the oversight!

---

## Audio Converter
A script that converts audio files to various formats using **FFmpeg**, supporting single files or entire folders with customizable quality, bitrate, and sample rate settings.

### Steps
1. **Download the script:** `audio_converter.py`
2. **Make sure Python 3 is installed**
    ```bash
    python --version
    ```
    You should get something like this:
    ```bash
    Python 3.x.x
    ```
3. **Install FFmpeg** and ensure it's available in your system's PATH:
    - Download FFmpeg from: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
    - Verify FFmpeg installation:
        ```bash
        ffmpeg -version
        ```
4. **(Optional)** Install `tqdm` for progress bar support in folder mode:
    ```bash
    pip install tqdm
    ```
5. **Run the script** using cmd, PowerShell, bash, etc.
    ```bash
    python audio_converter.py
    ```
6. **Follow the steps in the output terminal** and provide these inputs:
    - **Conversion mode** (1 for single file, 2 for all files in a folder)
    - **Source path** (path to the audio file or folder containing audio files)
    - **Destination path** (where converted files will be saved)
    - **Output format** (e.g., `.mp3`, `.wav`, `.flac`, or custom format)
    - **Quality setting** (0 for highest to 9 for lowest)
    - **Optional bitrate** (e.g., `192k`) and sample rate (e.g., `44100`)
    - **Overwrite option** (`y`/`n` to overwrite existing files)

> **Note:** The script supports common audio formats (`.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a`, `.wma`) and provides detailed feedback on conversion progress, including a summary of converted, skipped, and errored files.  
Ensure FFmpeg is installed, as it's required for audio conversion.

---

# Song Processor
A Python CLI tool designed to prepare custom tracks for [**Karaoke With Friends**](https://moun4u.itch.io/karaoke-with-friends). It uses **Demucs** for AI vocal/instrumental separation and **Whisper / Stable-Whisper** for automated timestamped lyric transcription or forced alignment.

## Prerequisites

Before running the tool, make sure you have the following installed on your system:
1. **Python** (version 3.8 or higher)
2. **FFmpeg** (Must be installed and added to your system's Environment PATH, as Demucs and Whisper require it to process audio).

### Install FFmpeg
* **Mac (via Homebrew):**
```
brew install ffmpeg
```

* **Linux (Ubuntu/Debian):**
```
sudo apt update && sudo apt install ffmpeg

sudo dnf install ffmpeg
```

* **Windows (via Conda):**
```bash
choco install ffmpeg
```

## Installation
1. Clone or download this repository to your local machine.
2. Open a terminal inside the project directory and install the required Python packages using the provided requirements file:
```
pip install -r requirements.txt
```
## How to Use the Program
You can run this tool in two different ways:

### Method A: The 1-Click Batch Script (Recommended)
You can use the provided run.bat script to process files easily without typing paths manually.

**Drag-and-Drop Mode:** Highlight your song file (.mp3 or .wav) and optional custom lyrics file (.txt), then drag and drop them both directly onto run.bat.

**Interactive Mode:** Simply double-click run.bat to launch the command prompt, and it will prompt you step-by-step for your inputs.

  
### Method B: Direct Command Line
Run the script directly from your terminal:

```
python song_processor_cli.py path/to/song.mp3 path/to/lyrics.txt
```

## Script Options & Prompts
When running the script interactively, you will be asked for the following parameters:

**Transcription Strength / Model Size: (base, small, medium, large)**
Controls the accuracy and resource weight of the Whisper AI model.

**Default:** large

**Song File Path:** Path to your audio file (.mp3, .wav, .flac, .m4a, .mp4).

**Custom Lyrics File Path (Optional):**
Path to a .txt file containing your song lyrics for forced alignment via stable-whisper. Press Enter to skip if you want Whisper to auto-transcribe the vocals from scratch.

**Language Code:** Main language of the track (e.g., 'en' for English, 'ko' for Korean).
Default: en

## Output Structure
Once processing completes, a folder named output_songs/{song_name}/ will be created containing the exact 3 files required by Karaoke With Friends:

**{song_name}.txt** – The timestamped and color-coded lyric chart.

**{song_name}_vocals.wav** – The isolated vocal track.

**{song_name}_instrumental.wav** – The background instrumental track.

## Customizing Lyrics & Formatting
If the automatically generated .txt output isn't satisfactory, you can feed a custom lyrics .txt file into the processor.

### Custom Input Format (.txt)
Use # at the beginning of a line to add comments or ignore lines.

Use bracketed singer names (e.g., [bob], [tim]) to assign different colors per singer for the game UI.

**Example custom lyrics text file:**

```
# title of the song
lyrics sentence
lyrics sentence
[bob]
lyrics sentence
[tim]
lyrics sentence
lyrics sentence
lyrics sentence
[bob]
lyrics sentence
```
(Note: Lines before any singer tag remain white/default, while subsequent lines automatically cycle through assigned team colors like blue, red, yellow, green, and pink).

### Final Output File Structure
If you prefer to manually tweak the output text file directly, it follows this strict format:
``` 
time in seconds | lyrics sentence | color
``` 
**Example output lines:**
```
5 | lyrics sentence | white
12 | lyrics sentence | white
30 | lyrics sentence | blue
40 | lyrics sentence | red
44 | lyrics sentence | red
50 | lyrics sentence | red
63 | lyrics sentence | blue
```

If the output of the .txt is not sactifactory for the user you can either rerun it with either adding a custom lyrics text file into the song processor 
for the .txt file structure is "#to ignore a line inside the .txt file", "[name of singer] if you want to separate the different person that sings which line" in the game connected to this song processor it will give the lyrics a different collor based on who's singing and the lyrics will be listed with each line and connected to the time sung in the .mp3 file, like this:

The first two lines will not get a color, but the lines after bob and tim will gain their own colors.


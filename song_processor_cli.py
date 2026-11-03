import os
import sys
import whisper
import stable_whisper
from demucs.api import Separator, save_audio
import shutil
import subprocess
import argparse

# Check for FFmpeg dependency
def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("\n[ERROR] FFmpeg was not found on your system!")
        print("Demucs and Whisper require FFmpeg to process audio files.")
        print("Please install FFmpeg and add it to your System PATH.")
        input("\nPress Enter to exit...")
        sys.exit(1)

def process_song(audio_path: str, lyrics_path: str = "", strength: str = "large", lang: str = "en", output_dir: str = "output_songs"):
    if not os.path.exists(audio_path):
        print(f"Error: File not found -> {audio_path}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    
    song_name = os.path.splitext(os.path.basename(audio_path))[0]
    song_output_dir = os.path.join(output_dir, song_name)
    os.makedirs(song_output_dir, exist_ok=True)
    has_custom_lyrics = os.path.exists(lyrics_path) if lyrics_path else False

    print("=" * 60)
    print(f" Processing  Song: {song_name}")
    print("=" * 60)

    print(f"\n[1/2] Separating vocals and instruments for {song_name}... ")
    separator = Separator(model="htdemucs", device="cpu", progress=True)
    origin, separated = separator.separate_audio_file(audio_path)

    instrumental = separated["drums"] + separated["bass"] + separated["other"]
    vocal = separated["vocals"]

    inst_dest = os.path.join(song_output_dir, f"{song_name}_instrumental.wav")
    save_audio(instrumental, inst_dest, separator.samplerate)
    vocal_dest = os.path.join(song_output_dir, f"{song_name}_vocals.wav")
    save_audio(vocal, vocal_dest, separator.samplerate)
    print(f"Saved instrumental track to: {inst_dest} and singer to: {vocal_dest}")

    valid_strenghts = ["base","small","medium","large"]
    if strength not in valid_strenghts:
        print(f"Warning: Invalid model size '{strength}'. Defaulting to 'large'.")
        strength = "large"
    
    txt_dest = os.path.join(song_output_dir, f"{song_name}.txt")
    
    if has_custom_lyrics:
        print(f"\n[2/2] Custom lyrics found! Performing forced alignment...")

        with open(lyrics_path, "r", encoding="utf-8") as f:
            custom_lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        align_model = stable_whisper.load_model(strength)

        text_prompt = "\n".join(custom_lines)
        aligned_res = align_model.align(vocal_dest, text_prompt, language=lang, original_split=True)

        assigned_color = {}
        color_palette = ["blue","red","yellow","green","pink"]
        current_color = "white"
        
        with open(txt_dest, "w", encoding="utf-8") as f:
            f.write(f"# Auto-aligned chart for {song_name}\n")
            for segment in aligned_res.segments:
                start_time = round(segment.start, 2)
                text_content = segment.text.strip()

                if not text_content:
                    continue
                    
                if text_content.startswith("[") and text_content.endswith("]"):
                    if text_content not in assigned_color:
                        color_index = len(assigned_color) % len(color_palette)
                        assigned_color[text_content] = color_palette[color_index]

                    current_color = assigned_color[text_content]
                    continue
                    
                f.write(f"{start_time} | {text_content} | {current_color}\n")
        
        print(f"Successfully aligned lyric chart: {txt_dest}")
        
    else:    
        print(f"\n[2/2] No custom lyrics found! Transcribing lyrics and generating timestamps with Whisper...")
        whisper_model = whisper.load_model(strength)
        res = whisper_model.transcribe(vocal_dest, language=lang, word_timestamps=False)

        with open(txt_dest, "w", encoding="utf-8") as f:
            f.write(f"# Auto-generated chart for {song_name}\n")
            
            for segment in res["segments"]:
                start_time = round(segment["start"], 2)
                text_content = segment["text"].strip()
                f.write(f"{start_time} | {text_content} | white\n")

        print(f"Successfully generated lyric chart: {txt_dest}")

if __name__ == "__main__":
    check_ffmpeg()
    
    # Support drag-and-drop via command line argument if provided, otherwise prompt user
    if len(sys.argv) > 1:
        target_mp3 = sys.argv[1]
        target_txt = sys.argv[2] if len(sys.argv) > 2 else ""
        strength = "large"
        language = "en"
        print(f"sent {target_mp3} and {target_txt}")
    else:
        strength = input("Choose transcription strength (base, small, medium, large) [default: large]: ").strip().lower()
        if not strength:
            strength = "large"
            
        target_mp3 = input("Enter path to your song file (.mp3/.wav): ").strip().strip('"')
        target_txt = input("Enter path to optional custom lyrics (.txt) [Press Enter to skip]: ").strip().strip('"')
        language = input("Enter main language code (e.g. 'en', 'ko') [default: en]: ").strip().lower()
        if not language:
            language = "en"

    process_song(target_mp3, target_txt, strength, language)
    input("\nProcessing complete! Press Enter to exit...")
@echo off
title Karaoke With Friends - Song Processor
cd /d "%~dp0"
python song_processor_cli.py %*
pause
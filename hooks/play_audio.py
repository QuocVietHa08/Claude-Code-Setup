#!/usr/bin/env python3
"""
Claude Code Stop Hook - Task Completion Announcer
Plays pre-generated audio clips when tasks are completed
"""

import sys
import subprocess
from pathlib import Path


def play_audio(audio_file):
    """Play audio file using system audio player"""
    try:
        # Use afplay on macOS
        subprocess.run(["afplay", str(audio_file)], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to play audio: {audio_file}")
    except FileNotFoundError:
        print(
            "Audio player not found. Install afplay or modify script for your system."
        )


def main():
    """Main function for Claude Code stop hook"""
    print("Stop hook triggered!")
    # Get audio directory
    audio_dir = Path(__file__).parent.parent / "audio"

    # Default to task_complete sound (try multiple formats)
    base_name = "task_complete"

    # Override with specific sound if provided as argument
    if len(sys.argv) > 1:
        base_name = sys.argv[1]

    # Try different audio formats
    audio_path = None
    for ext in [".mp3", ".aiff", ".wav", ".m4a"]:
        test_path = audio_dir / f"{base_name}{ext}"
        if test_path.exists():
            audio_path = test_path
            break

    # Check if audio file exists
    if not audio_path:
        print(f"Audio file not found in: {audio_dir}")
        print(f"Looking for: {base_name}.[mp3|aiff|wav|m4a]")
        print("Run generate_audio_clips.py first to create audio files.")
        sys.exit(1)

    # Play the audio
    play_audio(audio_path)


main()

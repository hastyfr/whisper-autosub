Auto Subtitle Generator
A Python application that automatically generates and embeds subtitles for video files using OpenAI's Whisper AI model. Built with a modern PyQt5 interface, this tool is perfect for creating accessible videos with minimal effort.
Features


Python 3.8+
FFmpeg: Required for audio extraction and subtitle embedding.
Windows: Download from gyan.dev, extract, and add the bin folder to your PATH.
Mac: Install with brew install ffmpeg (requires Homebrew).
Linux: Install with sudo apt-get install ffmpeg (Ubuntu) or equivalent for your distribution.



Installation

Clone the repository:git clone https://github.com/your-username/auto-subtitle-generator.git
cd auto-subtitle-generator


Create and activate a virtual environment:python -m venv venv


Mac/Linux: source venv/bin/activate
Windows: venv\Scripts\activate


Install dependencies:pip install -r requirements.txt


Verify FFmpeg:Run ffmpeg -version to ensure FFmpeg is installed and accessible in your PATH.

Usage

Run the application:python subtitle_generator.py


In the GUI:
Click Select Video File to choose a video (MP4, AVI, MKV).
Click Select Save Location to specify where to save the subtitled video.
Click Generate Subtitles to process the video and create a new video with embedded subtitles.


Monitor the progress bar and status messages. The output video will be saved at the specified location.

Project Structure

subtitle_generator.py: Main application code.
requirements.txt: Python dependencies.
screenshots/: Folder for demo images (add your own).

Future Improvements

Support for audio file inputs (e.g., MP3, WAV).
Option to select different Whisper models for accuracy vs. speed trade-offs.
Export subtitles in additional formats (e.g., VTT).
Bundle FFmpeg for easier setup (planned for v2).

License
This project is licensed under the MIT License. See LICENSE for details.
Note: FFmpeg is licensed under the LGPL/GPL. Ensure compliance when using FFmpeg binaries (see FFmpeg License).
Contact
Built by [Your Name]. Feel free to reach out via hastywrld@gmail.com or open an issue on GitHub for questions or suggestions!


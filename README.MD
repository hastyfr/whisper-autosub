🎥 Auto Subtitle Generator

A sleek, AI-powered desktop application that automatically generates and embeds subtitles for videos using OpenAI's Whisper. Built with a modern PyQt5 interface and integrated with FFmpeg, this tool makes video accessibility effortless. Perfect for showcasing skills in AI, GUI development, and video processing in a portfolio.

🚀 Features

AI-Powered Transcription: Leverages OpenAI's Whisper (base model) for accurate speech-to-text transcription.
Modern GUI: Clean, responsive PyQt5 interface with a gradient background, animated buttons, and a real-time progress bar.
Embedded Subtitles: Generates plain white subtitles (Arial, 24pt, no border) embedded as a toggleable mov_text track in the output video.
Separate SRT File: Saves a standalone .srt file for flexibility.
Real-Time Feedback: Displays FFmpeg progress in the console and smooth GUI progress updates, reaching "100%" on completion.
Cross-Platform: Runs on Windows, Mac, and Linux with proper FFmpeg setup.



🛠️ Installation
Prerequisites

Python 3.8+: Download Python.
FFmpeg: Required for audio extraction and subtitle embedding.
Windows: Download from gyan.dev, extract, and add the bin folder to your PATH.
Mac: Install with brew install ffmpeg (Homebrew).
Linux: Install with sudo apt-get install ffmpeg (Ubuntu) or equivalent.


Setup :-
Clone the repository:git clone https://github.com/hastyfr/auto-subtitle-generator.git
cd auto-subtitle-generator


Create and activate a virtual environment:python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

Install dependencies:pip install -r requirements.txt

Verify FFmpeg:ffmpeg -version

Ensure FFmpeg is in your PATH.

🎮 Usage

Run the app:python whisperui.py


In the GUI:
Click Select Video File to choose a video (MP4, AVI, MKV).
Click Select Save Location to specify the output path (e.g., test.mp4).
Click Generate Subtitles to process the video.


Monitor the progress bar (reaches "100%") and console for FFmpeg output.
Output:
test_subtitled.mp4: Video with embedded subtitles (toggleable in players like VLC).
test.srt: Separate subtitle file.




🌟 Why This Project?
This project demonstrates a blend of AI, GUI development, and video processing:

AI Skills: Implements OpenAI's Whisper for speech recognition, showcasing machine learning integration.
GUI Design: Features a modern PyQt5 interface with real-time progress and user-friendly design.
Video Processing: Uses FFmpeg for audio extraction and subtitle embedding, highlighting multimedia expertise.


Developed as part of my journey to explore AI-driven solutions, this project reflects my passion for creating accessible, user-focused tools.

📋 Project Structure
auto-subtitle-generator/
├── whisperui.py          # Main application code
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── .gitignore            # Excludes venv/, temp files
└── screenshots/          # Demo images

🔮 Future Improvements

Support for audio files (MP3, WAV).
Customizable subtitle fonts, colors, and sizes.
Completion sound notification.
Option for burnt-in subtitles.
Support for additional Whisper models (e.g., small, medium).

⚖️ License
This project is licensed under the MIT License. See LICENSE for details.
Note: FFmpeg is licensed under the LGPL/GPL. Ensure compliance when using FFmpeg binaries (see FFmpeg License).
📬 Contact - hastywrld@gmail.com


⭐️ If you find this project useful, give it a star on GitHub! Contributions and feedback are welcome.

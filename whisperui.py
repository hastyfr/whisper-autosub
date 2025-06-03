import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QProgressBar, QLabel, QDesktopWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import whisper
import ffmpeg
import srt
from datetime import timedelta

class SubtitleWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, video_path, save_path):
        super().__init__()
        self.video_path = video_path
        self.save_path = save_path
        self._is_running = True

    def run(self):
        try:
            # Load Whisper model
            model = whisper.load_model("base")
            self.progress.emit(5)

            # Extract audio from video
            audio_path = "temp_audio.wav"
            stream = ffmpeg.input(self.video_path)
            stream = ffmpeg.output(stream, audio_path, acodec="pcm_s16le", ar="16k", ac=1)
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
            self.progress.emit(20)

            # Transcribe audio with progress simulation
            start_time = time.time()
            result = model.transcribe(audio_path)
            duration = time.time() - start_time
            for i in range(21, 61):  # Simulate progress from 21% to 60%
                if not self._is_running:
                    return
                elapsed = time.time() - start_time
                if elapsed < duration:
                    progress = 21 + int((i - 21) * (elapsed / duration))
                    self.progress.emit(min(progress, 60))
                    time.sleep(0.1)
            self.progress.emit(61)

            # Generate SRT subtitles
            subtitles = []
            for i, segment in enumerate(result["segments"]):
                start = timedelta(seconds=segment["start"])
                end = timedelta(seconds=segment["end"])
                subtitles.append(srt.Subtitle(
                    index=i + 1,
                    start=start,
                    end=end,
                    content=segment["text"].strip()
                ))
                # Incremental progress from 61% to 80%
                self.progress.emit(61 + int((i + 1) / len(result["segments"]) * 19))
            
            srt_content = srt.compose(subtitles)
            srt_path = os.path.splitext(self.save_path)[0] + ".srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
            self.progress.emit(80)

            # Embed subtitles into video
            output_video = os.path.splitext(self.save_path)[0] + "_subtitled.mp4"
            stream = ffmpeg.input(self.video_path)
            escaped_srt_path = srt_path.replace('\\', '\\\\').replace(':', '\\:')
            stream = ffmpeg.output(
                stream, output_video,
                vf=f"subtitles='{escaped_srt_path}':force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,Outline=0,Shadow=0'",
                vcodec="libx264",
                acodec="copy",
                preset="fast",
                **{"c:s": "mov_text"}
            )
            start_time = time.time()
            process = ffmpeg.run_async(stream, overwrite_output=True, pipe_stdout=True, pipe_stderr=True)
            duration_estimate = os.path.getsize(self.video_path) / (1024 * 1024) / 2  # Rough estimate: 2 MB/s
            while process.poll() is None:
                if not self._is_running:
                    process.terminate()
                    return
                elapsed = time.time() - start_time
                progress = 81 + int((elapsed / duration_estimate) * 19)
                self.progress.emit(min(progress, 99))
                time.sleep(0.1)
                # Print FFmpeg output to console
                stderr = process.stderr.read(1024)
                if stderr:
                    sys.stderr.write(stderr.decode())
                    sys.stderr.flush()
            process.wait()
            if process.returncode != 0:
                raise RuntimeError("FFmpeg subtitle embedding failed")
            self.progress.emit(100)

            # Clean up temporary files
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            self.finished.emit(output_video)
        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        self._is_running = False

class SubtitleGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.video_path = None
        self.save_path = None
        self.worker = None

    def initUI(self):
        self.setWindowTitle("Auto Subtitle Generator")
        self.setFixedSize(600, 400)
        self.center()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        main_widget.setLayout(layout)

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e0e7ff, stop:1 #f0f2f5);
            }
            QPushButton {
                background-color: #1e90ff;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                transition: all 0.3s;
            }
            QPushButton:hover {
                background-color: #1565c0;
                transform: scale(1.05);
            }
            QPushButton:disabled {
                background-color: #b0c4de;
            }
            QProgressBar {
                border: 2px solid #4682b4;
                border-radius: 10px;
                text-align: center;
                height: 25px;
                background-color: #e6f0fa;
                font-size: 12px;
                color: #333;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #40c4ff, stop:1 #0288d1);
                border-radius: 8px;
            }
            QLabel {
                font-size: 16px;
                color: #2f4f4f;
            }
        """)

        title = QLabel("Video Subtitle Generator")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.select_video_btn = QPushButton("Select Video File")
        self.select_video_btn.clicked.connect(self.select_video)
        layout.addWidget(self.select_video_btn)

        self.select_save_btn = QPushButton("Select Save Location")
        self.select_save_btn.clicked.connect(self.select_save_location)
        layout.addWidget(self.select_save_btn)

        self.generate_btn = QPushButton("Generate Subtitles")
        self.generate_btn.clicked.connect(self.generate_subtitles)
        self.generate_btn.setEnabled(False)
        layout.addWidget(self.generate_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def select_video(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "",
            "Video Files (*.mp4 *.avi *.mkv)"
        )
        if file:
            self.video_path = file
            self.status_label.setText(f"Selected: {os.path.basename(file)}")
            self.check_generate_button()

    def select_save_location(self):
        file, _ = QFileDialog.getSaveFileName(
            self, "Select Save Location", "",
            "MP4 Files (*.mp4)"
        )
        if file:
            self.save_path = file
            self.status_label.setText(f"Save to: {os.path.basename(file)}")
            self.check_generate_button()

    def check_generate_button(self):
        if self.video_path and self.save_path:
            self.generate_btn.setEnabled(True)
        else:
            self.generate_btn.setEnabled(False)

    def generate_subtitles(self):
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.status_label.setText("Processing...")
        self.generate_btn.setEnabled(False)
        self.select_video_btn.setEnabled(False)
        self.select_save_btn.setEnabled(False)

        self.worker = SubtitleWorker(self.video_path, self.save_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_finished(self, output_path):
        self.status_label.setText(f"Completed! Saved to {os.path.basename(output_path)}")
        self.generate_btn.setEnabled(True)
        self.select_video_btn.setEnabled(True)
        self.select_save_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("100%")
        self.worker = None

    def on_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.generate_btn.setEnabled(True)
        self.select_video_btn.setEnabled(True)
        self.select_save_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.worker = None

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubtitleGenerator()
    window.show()
    sys.exit(app.exec_())
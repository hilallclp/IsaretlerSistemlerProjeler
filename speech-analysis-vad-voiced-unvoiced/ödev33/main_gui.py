import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
import audio_engine

class CyberAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cyber-Neon VAD & V/UV Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #0D0D0D; color: #00FF41;")

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout(self.widget)

        self.btn = QPushButton("RECORD & ANALYZE NEON AUDIO")
        self.btn.setStyleSheet("border: 2px solid #00FF41; padding: 15px; font-weight: bold; color: #00FF41;")
        self.btn.clicked.connect(self.start)
        self.layout.addWidget(self.btn)

        self.fig, self.axs = plt.subplots(3, 1, figsize=(10, 12))
        self.fig.patch.set_facecolor('#0D0D0D')
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

    def start(self):
        # 🎤 Mikrofon kaydı alıp, VAD ve V/UV analizini yap
        audio, fs, eng, zcr, labels, hop = audio_engine.analyze_audio(record=True, duration=15)

        times = np.linspace(0, len(audio)/fs, len(audio))
        frame_times = np.linspace(0, len(audio)/fs, len(labels))

        for ax in self.axs:
            ax.clear()
            ax.set_facecolor('#000000')
            ax.tick_params(colors='#00FF41')

        # 1️⃣ Sinyal + Maskeler
        self.axs[0].plot(times, audio, color='#00FF41', alpha=0.6)
        for i in range(len(labels)):
            start_t = frame_times[i]
            end_t   = frame_times[i+1] if i+1 < len(frame_times) else times[-1]
            if labels[i]==1:  # Voiced
                self.axs[0].axvspan(start_t, end_t, color='#39FF14', alpha=0.4)
            elif labels[i]==2: # Unvoiced
                self.axs[0].axvspan(start_t, end_t, color='#00FFFF', alpha=0.4)
        self.axs[0].set_title("VAD & V/UV MASKING (GREEN: VOICED | BLUE: UNVOICED)", color='#00FF41')

        # 2️⃣ Enerji (STE)
        self.axs[1].plot(frame_times, eng, color='#FF00FF')
        self.axs[1].set_title("SHORT-TIME ENERGY (STE)", color='#FF00FF')

        # 3️⃣ ZCR
        self.axs[2].plot(frame_times, zcr, color='#FFFF00')
        self.axs[2].set_title("ZERO-CROSSING RATE (ZCR)", color='#FFFF00')

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CyberAnalyzer()
    win.show()
    sys.exit(app.exec_())
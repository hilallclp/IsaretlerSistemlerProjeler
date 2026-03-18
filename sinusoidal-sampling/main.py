import sys
import numpy as np
import sounddevice as sd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# -------- PARAMETRELER --------
fs = 8000
sure = 0.4
t = np.linspace(0, sure, int(fs * sure), endpoint=False)

# DTMF frekans tablosu
tuslar = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477), 'A': (697, 1633),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477), 'B': (770, 1633),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477), 'C': (852, 1633),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477), 'D': (941, 1633)
}

class DTMFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DTMF Sinyal Sentezi - Mac Version")
        self.setMinimumSize(900, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("DTMF Sinyal Sentezi ve FFT Analizi")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)

        self.button_grid = QGridLayout()
        layout.addLayout(self.button_grid)
        self.create_buttons()

        self.figure = Figure(figsize=(8,4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def create_buttons(self):
        for i, tus in enumerate(tuslar.keys()):
            btn = QPushButton(tus)
            btn.setFixedSize(80, 60)
            btn.clicked.connect(lambda checked, t=tus: self.tus_basildi(t))
            self.button_grid.addWidget(btn, i//4, i%4)

    def tus_basildi(self, tus):
        flow, fhigh = tuslar[tus]
        sinyal = 0.5 * (np.sin(2*np.pi*flow*t) + np.sin(2*np.pi*fhigh*t))

        # --- SES ---
        try:
            sd.play(sinyal.astype(np.float32), fs)
            sd.wait()
        except Exception as e:
            print("Ses hatası:", e)

        # --- GRAFİK ---
        self.figure.clear()
        ax1, ax2 = self.figure.subplots(1,2)

        # Zaman domain
        ax1.plot(t[:200], sinyal[:200])
        ax1.set_title(f"{tus} - Zaman")
        ax1.set_xlabel("Zaman (s)")
        ax1.set_ylabel("Genlik")

        # FFT
        fft_sonuc = np.abs(np.fft.fft(sinyal))
        frekanslar = np.fft.fftfreq(len(sinyal), 1/fs)

        ax2.plot(frekanslar[:len(frekanslar)//2],
                 fft_sonuc[:len(fft_sonuc)//2])
        ax2.set_xlim(0, 2000)
        ax2.set_title("Frekans Spektrumu")
        ax2.set_xlabel("Frekans (Hz)")
        ax2.set_ylabel("Genlik")

        self.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DTMFApp()
    window.show()
    sys.exit(app.exec_())

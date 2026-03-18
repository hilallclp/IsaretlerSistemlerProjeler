import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTabWidget, QTextEdit, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from decoder import decode_audio, record_microphone

class DTMF_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DTMF Analiz")
        self.resize(900,600)
        layout = QVBoxLayout()

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Metin görüntüleme
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        # Butonlar
        self.btn_text_to_audio = QPushButton("Metin → Ses")
        self.btn_text_to_audio.clicked.connect(self.text_to_audio)
        layout.addWidget(self.btn_text_to_audio)

        self.btn_mic_to_text = QPushButton("Mikrofon → Metin")
        self.btn_mic_to_text.clicked.connect(self.mic_to_text)
        layout.addWidget(self.btn_mic_to_text)

        self.setLayout(layout)

    def add_tab_with_figures(self, figures, titles):
        self.tabs.clear()
        for fig, title in zip(figures, titles):
            canvas = FigureCanvas(fig)
            self.tabs.addTab(canvas, title)

    def text_to_audio(self):
        from encoder import encode_text
        # 🚀 Input Dialog ekledik
        text, ok = QInputDialog.getText(self, "Metin → Ses", "Metni gir:")
        if ok and text:
            encode_text(text, filename="output.wav")
            decoded_text, figs = decode_audio("output.wav", gui=True)
            self.text_output.setText(decoded_text)
            self.add_tab_with_figures(figs, ["Zaman Domaini","FFT","Goertzel"])

    def mic_to_text(self):
        wav_file = record_microphone("ses_input.wav")
        decoded_text, figs = decode_audio(wav_file, gui=True)
        self.text_output.setText(decoded_text)
        self.add_tab_with_figures(figs, ["Zaman Domaini","FFT","Goertzel"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DTMF_GUI()
    window.show()
    sys.exit(app.exec_())

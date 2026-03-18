import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from frequencies import char_map

fs = 44100
duration = 0.04      # karakter süresi (40 ms)
silence_duration = 0.01  # karakterler arası boşluk (10 ms)

def encode_text(text, filename="output.wav"):
    text = text.upper()
    signal = np.array([], dtype=np.float32)

    for char in text:
        if char not in char_map:
            continue

        f_low, f_high = char_map[char]

        # Zaman ekseni
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)

        # İki frekanslı DTMF benzeri sinyal
        s = np.sin(2 * np.pi * f_low * t) + np.sin(2 * np.pi * f_high * t)

        # 10 ms sessizlik
        silence = np.zeros(int(fs * silence_duration))

        # Harf + sessizlik ekle
        signal = np.concatenate((signal, s, silence))

    if len(signal) == 0:
        print("Geçerli karakter bulunamadı.")
        return

    # Normalize
    signal = signal / np.max(np.abs(signal))

    # Hoparlörden çal
    sd.play(signal, fs)
    sd.wait()

    # WAV olarak kaydet
    write(filename, fs, (signal * 32767).astype(np.int16))

    print(f"'{text}' için ses üretildi, {silence_duration*1000:.0f} ms boşluklu ve kaydedildi.")

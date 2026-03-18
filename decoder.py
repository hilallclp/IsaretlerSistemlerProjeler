# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from frequencies import reverse_map, low_freqs, high_freqs
import sounddevice as sd
from scipy.io.wavfile import write

# ===== Ayarlar =====
duration_char = 0.04  # 40 ms karakter süresi
threshold = 1e7
fs = 44100
mic_duration = 2 # mikrofon kaydı süresi

# ===== Mikrofon Kaydı =====
def record_microphone(filename="ses_input.wav"):
    print("🎤 Konuşmayı başlat, kayıt ediliyor...")
    recording = sd.rec(int(mic_duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    recording = recording.flatten()
    recording = recording / np.max(np.abs(recording))
    write(filename, fs, (recording * 32767).astype(np.int16))
    print(f"✅ Ses kaydedildi: {filename}")
    return filename

# ===== Goertzel Hesabı =====
def goertzel(segment, freq, fs):
    N = len(segment)
    k = int(0.5 + ((N * freq) / fs))
    omega = (2.0 * np.pi * k) / N
    coeff = 2.0 * np.cos(omega)
    s_prev = 0
    s_prev2 = 0
    for sample in segment:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    power = s_prev2**2 + s_prev**2 - coeff * s_prev*s_prev2
    return power

# ===== Ses Çözümleme =====
def decode_audio(filename="output.wav", gui=False):
    samplerate, data = read(filename)
    samples_per_char = int(samplerate * duration_char)
    decoded_text = ""
    last_char = None  # Debouncing

    # Grafik için eksen ve FFT
    time_axis = np.arange(len(data)) / samplerate
    fft_spectrum = np.fft.fft(data.astype(np.float32) * np.hamming(len(data)))
    freqs = np.fft.fftfreq(len(fft_spectrum), 1/samplerate)
    magnitude = np.abs(fft_spectrum)
    pos_mask = freqs > 0

    all_freqs = low_freqs + high_freqs
    total_powers = np.zeros(len(all_freqs))

    # Karakter segmentlerini çöz
    for i in range(0, len(data), samples_per_char):
        segment = data[i:i+samples_per_char]
        if len(segment) < samples_per_char:
            continue
        segment = segment * np.hamming(len(segment))
        low_powers = [goertzel(segment, f, samplerate) for f in low_freqs]
        high_powers = [goertzel(segment, f, samplerate) for f in high_freqs]
        max_low = max(low_powers)
        max_high = max(high_powers)
        char = None
        if max_low > threshold and max_high > threshold:
            detected_low = low_freqs[np.argmax(low_powers)]
            detected_high = high_freqs[np.argmax(high_powers)]
            char = reverse_map.get((detected_low, detected_high), None)
        # 🔹 Debouncing
        if char and char != last_char:
            decoded_text += char
            last_char = char
        total_powers += np.array(low_powers + high_powers)

    # ===== Grafikler – Stil Görünümü Düzeltilmiş =====
    plt.rcParams.update({'font.size': 12, 'font.family': 'Arial'})

    # 🔹 Zaman Domaini
    fig1, ax1 = plt.subplots(figsize=(8,3), facecolor='black')
    ax1.plot(time_axis, data, color='#FF69B4', linewidth=1.5)  # neon pembe
    ax1.set_facecolor('black')
    ax1.set_title("Zaman Domaini Sinyali", fontsize=14, fontweight='bold', color='white')
    ax1.set_xlabel("Zaman (s)", color='white')
    ax1.set_ylabel("Genlik", color='white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    ax1.grid(True, linestyle='--', alpha=0.3, color='white')

    # 🔹 FFT
    fig2, ax2 = plt.subplots(figsize=(8,3), facecolor='black')
    ax2.plot(freqs[pos_mask], magnitude[pos_mask], color='#FFA500', linewidth=1.5)  # turuncu
    ax2.set_facecolor('black')
    ax2.set_title("Frekans Domaini (FFT)", fontsize=14, fontweight='bold', color='white')
    ax2.set_xlabel("Frekans (Hz)", color='white')
    ax2.set_ylabel("Genlik", color='white')
    ax2.set_xlim(0, samplerate/2)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')
    ax2.grid(True, linestyle=':', alpha=0.3, color='white')  # noktalı grid

    # 🔹 Goertzel
    fig3, ax3 = plt.subplots(figsize=(8,3), facecolor='black')
    ax3.bar(all_freqs, total_powers, color='#8000FF', width=20, alpha=0.8)  # mor
    ax3.set_facecolor('black')
    ax3.set_title("Goertzel Frekans Güçleri", fontsize=14, fontweight='bold', color='white')
    ax3.set_xlabel("Frekans (Hz)", color='white')
    ax3.set_ylabel("Toplam Güç", color='white')
    ax3.tick_params(axis='x', colors='white')
    ax3.tick_params(axis='y', colors='white')
    ax3.grid(True, linestyle='--', alpha=0.2, color='white')

    if gui:
        return decoded_text, [fig1, fig2, fig3]
    else:
        plt.show()
        print("Çözümlenen Metin:", decoded_text)
        return decoded_text
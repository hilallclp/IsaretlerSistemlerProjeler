import numpy as np
import librosa
import soundfile as sf
import sounddevice as sd
import os

def analyze_audio(record=True, duration=5, file_path=None):
    """
    Ses kaydı alır veya dosyadan okur.
    record=True ise mikrofon kaydı yapılır.
    Orijinal ve iyileştirilmiş dosyalar kaydedilir.
    """
    if record:
        fs = 44100
        print(f"{duration}s boyunca kayıt yapılıyor...")
        audio = sd.rec(int(duration*fs), samplerate=fs, channels=1)
        sd.wait()
        audio = audio.flatten()
        # Orijinal kaydı kaydet
        sf.write("orijinal_kaydi.wav", audio, fs)
        print("Orijinal ses kaydedildi: orijinal_kaydi.wav")
    else:
        if file_path is None or not os.path.exists(file_path):
            raise FileNotFoundError(f"Ses dosyası bulunamadı: {file_path}")
        audio, fs = librosa.load(file_path, sr=None)

    # ----------------------
    # 1️⃣ Normalizasyon
    # ----------------------
    audio = audio / np.max(np.abs(audio))

    # ----------------------
    # 2️⃣ Pencereleme ve Hamming
    # ----------------------
    frame_length = int(fs*0.02)  # 20 ms
    hop_length   = int(frame_length*0.5)  # %50 overlap
    frames = librosa.util.frame(audio, frame_length=frame_length, hop_length=hop_length).T
    window = np.hamming(frame_length)

    energies = []
    zcr_rates = []

    for f in frames:
        w = f * window
        energies.append(np.sum(w**2) / frame_length)
        zcr_rates.append(np.sum(np.abs(np.diff(np.sign(w)))) / (2*frame_length))

    energies = np.array(energies)
    zcr_rates = np.array(zcr_rates)

    # ----------------------
    # 3️⃣ Dinamik eşik ve VAD
    # ----------------------
    noise_floor = np.mean(energies[:20])  # İlk 20 frame sessizlik varsayımı
    threshold = max(noise_floor * 3, np.max(energies) * 0.01)
    vad_mask = np.zeros(len(energies))
    hangover_limit = 20
    counter = 0
    for i in range(len(energies)):
        if energies[i] > threshold:
            vad_mask[i] = 1
            counter = hangover_limit
        elif counter > 0:
            vad_mask[i] = 1
            counter -= 1

    # ----------------------
    # 4️⃣ Voiced / Unvoiced (Enerji + ZCR)
    # ----------------------
    v_uv_labels = np.zeros(len(energies))
    zcr_thresh = 0.15
    energy_thresh = threshold  # VAD eşiği ile uyumlu

    for i in range(len(energies)):
        if vad_mask[i] == 1:
            if zcr_rates[i] < zcr_thresh and energies[i] > energy_thresh:
                v_uv_labels[i] = 1  # Voiced
            else:
                v_uv_labels[i] = 2  # Unvoiced

    # ----------------------
    # 5️⃣ İyileştirilmiş konuşmayı kaydet
    # ----------------------
    sample_mask = np.zeros(len(audio), dtype=bool)
    for i in range(len(vad_mask)):
        if vad_mask[i] == 1:
            start = i * hop_length
            end = min(start + frame_length, len(audio))
            sample_mask[start:end] = True

    speech_audio = audio[sample_mask]
    sf.write("yeni_cikti.wav", speech_audio, fs)
    print("İyileştirilmiş ses kaydedildi: yeni_cikti.wav")

    return audio, fs, energies, zcr_rates, v_uv_labels, hop_length
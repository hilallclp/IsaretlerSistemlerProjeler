import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100       # Örnekleme frekansı
duration = 2     # Kaç saniye kaydedeceğin
filename = "ses_input.wav"

print("🔴 Kayıt başlıyor...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
write(filename, fs, recording)
print(f"✅ Kayıt bitti ve '{filename}' olarak kaydedildi.")
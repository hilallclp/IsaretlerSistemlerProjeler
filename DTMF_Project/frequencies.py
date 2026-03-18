# Türk alfabesi + boşluk
chars = list("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ ")

low_freqs = [697, 770, 852, 941, 1020, 1090]
high_freqs = [1209, 1336, 1477, 1633, 1777]

# Karakter -> (low, high)
char_map = {}
idx = 0
for low in low_freqs:
    for high in high_freqs:
        if idx >= len(chars):
            break
        char_map[chars[idx]] = (low, high)
        idx += 1

reverse_map = {v: k for k, v in char_map.items()}

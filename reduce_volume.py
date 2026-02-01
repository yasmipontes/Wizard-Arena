import pygame
pygame.mixer.init()

# Carregar o som
sound = pygame.mixer.Sound("sounds/attack.mp3")
sound.set_volume(0.05)  # 5% do volume

# Salvar como WAV com volume reduzido tocando silenciosamente
import wave
import struct
import math

# Gerar um arquivo WAV silencioso curto
duration = 0.5  # 0.5 segundos
sample_rate = 22050
num_samples = int(duration * sample_rate)

# Criar samples muito baixos (simular som baixo)
samples = [int(500 * math.sin(2 * math.pi * 440 * i / sample_rate)) for i in range(num_samples)]

# Salvar
with wave.open("sounds/attack_low.wav", "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(struct.pack('h' * len(samples), *samples))

print("Arquivo criado: attack_low.wav")

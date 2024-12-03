"""
Convertit une image en WAV. Le fichier ci-dessous encode et décode l'image.
Pour une image de 375x220, cela prend au programme environ 0.1 seconde.

Auteur : Jules Henriot-Colin
LICENSE : GPL-3.0
(Ce programme est destiné à des fins de recherche...)

Tout crédit est apprécier mais pas obligatoire.
"""
from base64 import b64encode, b64decode
from time import time
from struct import pack, unpack
from zlib import compress, decompress
from PIL import Image
import wave

def compress_image(image_path):

    f"""
    Va compresser l'image grace a pillow, paramtre: 
    le chemin de l'image a compresser
    return : rien, un image compresser a commpressed_{image_path}
    """
    image = Image.open(image_path)

    SIZE_ORIGINAL_IMAGE = image.size

    image_16_colors = image.resize((SIZE_ORIGINAL_IMAGE[0]//8, SIZE_ORIGINAL_IMAGE[1]//8))

    image_16_colors = image_16_colors.convert("RGB")
    image_16_colors.save(f"commpressed_{image_path}", optimize=True, quality=50)


def encode_base64(image_path):
    """
    Encode l'image en base 64
    Prend en compte le chemin de l'image
    return l'image en base64
    """

    with open(image_path, "rb") as image_file:
        image_binary = image_file.read()

    compressed_binary = compress(image_binary, level=9)
    image_data = b64encode(compressed_binary).decode("utf-8")
    return image_data

def decode_base64(encoded_text, output_image_path):

    """
    Decode l'image en base 64
    Prend en compte l'image en base64
    return Rien, enregistre l'image
    """
    received_compressed_binary = b64decode(encoded_text)
    decompressed_binary = decompress(received_compressed_binary)

    with open(output_image_path, "wb") as image_file:
        image_file.write(decompressed_binary)
    print(f"Image saved to: {output_image_path}")

def base64_to_wav(base64_string, wav_file):
    """tranform le le base 64 en audio WAV
    Prend en entrer le texte en base 64 et le fichier wav a enregistrer"""

    data = [ord(char) for char in base64_string]
    print(data)
    with wave.open(wav_file, 'w') as wav:

        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(44100)
        
        frames = pack(f'{len(data)}B', *data)
        wav.writeframes(frames)

def wav_to_base64(wav_file):
    """Convertie le wav en base64
    prend en entrer le fichier wav et retourn le texte en base 64"""

    with wave.open(wav_file, 'r') as wav:
        if wav.getnchannels() != 1 or wav.getsampwidth() != 1:
            raise ValueError("Le WAV doit etre mono avec des sample de 8-BIT")
        
        frames = wav.readframes(wav.getnframes())
        data = unpack(f'{len(frames)}B', frames)
        return ''.join(chr(byte) for byte in data)


start = time()
input_image = "image_de_test.jpg"
output_image = "output_image.png"
wav_filename = "base64_audio.wav"


print("==========ENCODAGE==============")
compress_image(input_image)

encoded_text = encode_base64(f"commpressed_{input_image}")
print(f"L'image est en BASE64 {encoded_text[:100]}, ...")
    
base64_to_wav(encoded_text, wav_filename)
print(f"L'image est enregistrer en wav {wav_filename}")

print("==========DECODAGE==============")

decoded_base64 = wav_to_base64(wav_filename)
    
decode_base64(decoded_base64, output_image)
print(f"L'image est enregistrer : {output_image}")

print("==========TEMPS FINAL==============")
print(f"Temps total {time()-start}")

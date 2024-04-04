from tkinter import Tk, Button, filedialog
from PIL import Image
import os
import random

def decrypt_image(image_path, key, mod):
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            if len(pixel) == 4:
                r, g, b, a = pixel
            else:
                r, g, b = pixel

            r = (r * pow(key, -1, mod)) % mod
            g = (g * pow(key, -1, mod)) % mod
            b = (b * pow(key, -1, mod)) % mod

            if len(pixel) == 4:
                pixels[x, y] = (r,g,b,a)
            else:
                pixels[x, y] = (r,g,b)

    return img

def brute_force_decrypt(image_path):
    filename = os.path.basename(image_path)
    keys = list(range(1, 300))  # 0 is excluded because it has no multiplicative inverse
    random.shuffle(keys)  # shuffle the keys to try them in random order
    for mod in range(256, 500):  # try different modulus values
        for key in keys:
            try:
                decrypted_image = decrypt_image(image_path, key, mod)
                decrypted_image.save(f'decrypted_{filename}_{key}_{mod}.png')
            except Exception as e:
                print(f"Failed to decrypt {filename} with key {key} and modulus {mod}: {e}")
def on_button_click():
    root = Tk()
    image_path = filedialog.askopenfilename()
    brute_force_decrypt(image_path)

root = Tk()
button = Button(root, text="Decrypt Image", command=on_button_click)
button.pack()
root.mainloop()
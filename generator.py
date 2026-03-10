import os
from PIL import Image, ImageDraw

# Output Ordner erstellen
os.makedirs("output", exist_ok=True)

# Bild erzeugen
img = Image.new("RGB", (1080,1920), "black") draw = ImageDraw.Draw(img)

draw.text((300,900),"JSG TEST GENERATOR", fill="white")

img.save("output/test.png")

print("Testbild erstellt")

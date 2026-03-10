import os
from PIL import Image

os.makedirs("output", exist_ok=True)

img = Image.new("RGB", (1080,1920), "black")

img.save("output/test.png")

print("OK")

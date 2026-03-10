import os
from PIL import Image, ImageDraw, ImageFont

# Output Ordner
os.makedirs("output", exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
MAX_SPIELE = 6

font = ImageFont.load_default()

spiele = [
("09.03", "JSG C vs SEEBACH", "18:30", "ST.MARTIN"), ("10.03", "JSG D vs EDENKOBEN", "17:30", "EDENKOBEN"), ("11.03", "JSG E1 vs HAMBACH", "11:00", "HAMBACH"), ("12.03", "JSG E2 vs ALTDORF", "11:00", "ALTDORF"), ("13.03", "JSG B vs SPEYER", "13:30", "SPEYER"), ("14.03", "JSG A vs LANDAU", "16:00", "LANDAU"), ("15.03", "JSG G vs HASSLOCH", "09:00", "HASSLOCH") ]

pages = [spiele[i:i+MAX_SPIELE] for i in range(0, len(spiele), MAX_SPIELE)]

index = 1

for page in pages:

    img = Image.new("RGB", (WIDTH, HEIGHT), "black")
    draw = ImageDraw.Draw(img)

    y = 300
    toggle = True

    for datum, teams, zeit, ort in page:

        bg = (255,255,255) if toggle else (212,175,55)

        draw.rectangle((80, y-20, 1000, y+60), fill=bg)

        text = f"{datum}  {teams}  {zeit}  {ort}"

        draw.text((100, y), text, fill="black", font=font)

        toggle = not toggle
        y += 130

    img.save(f"output/{index:02d}_spielplan.png")

    index += 1

print("Spielplan erstellt")

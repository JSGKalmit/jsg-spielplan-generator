import requests
import datetime
import os

print("JSG Kalmit Spielplan Generator gestartet")

# Vereins-ID von fussball.de
VEREIN_ID = "00ES8GNBC800007OVV0AG08LVUPGND5I"

# Zeitraum bestimmen
today = datetime.date.today()
start = today - datetime.timedelta(days=7)
end = today + datetime.timedelta(days=7)

print("Zeitraum:", start, "-", end)

# Beispiel API (wird später erweitert)
url = f"https://www.fussball.de/api/club/matches/{VEREIN_ID}"

try:
    r = requests.get(url)
    print("API Status:", r.status_code)
except:
    print("Daten konnten noch nicht geladen werden")

# Testdaten solange API noch nicht genutzt wird
spiele = [
    {"datum":"09.03","team":"JSG C","gegner":"Seebach","zeit":"18:30","ort":"St. Martin"},
    {"datum":"14.03","team":"JSG E1","gegner":"Hassloch","zeit":"11:00","ort":"Hassloch"}
]

os.makedirs("output", exist_ok=True)

with open("output/spielplan.txt","w") as f:
    for s in spiele:
        f.write(f'{s["datum"]} {s["team"]} vs {s["gegner"]} {s["zeit"]} {s["ort"]}\n')

print("Spielplan erstellt")

from PIL import Image, ImageDraw, ImageFont

width = 1080
height = 1920

img = Image.new("RGB",(width,height),"black")
draw = ImageDraw.Draw(img)

font = ImageFont.load_default()

y = 300

for s in spiele:
    text = f'{s["datum"]}  {s["team"]} vs {s["gegner"]}  {s["zeit"]}'
    draw.text((100,y),text,fill="white",font=font)
    y += 80

os.makedirs("output", exist_ok=True)

img.save("output/spielplan_story.png")

print("Storygrafik erstellt")

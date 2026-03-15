import os
import datetime
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

os.makedirs("output", exist_ok=True)

URL = "https://www.fussball.de/verein/tus-1920-maikammer-suedwest/-/id/00ES8GNBC800007OVV0AG08LVUPGND5I#!/"

WIDTH = 1080
HEIGHT = 1920
MAX_SPIELE = 6

font = ImageFont.load_default()

def roman_to_number(name):
    return name.replace(" II"," 2").replace(" III"," 3").replace(" IV"," 4")

def shorten_opponent(name):

    if "JSG" in name:
        part = name.split("JSG")[-1]
        return "JSG " + roman_to_number(part).strip()

    name = name.replace(" e.V.","")
    name = roman_to_number(name)

    return name.strip()

def shorten_place(place):
    return place.split(" ")[0]

def get_week_dates(offset=0):

    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    monday += datetime.timedelta(days=offset)

    sunday = monday + datetime.timedelta(days=6)

    return monday, sunday

def load_games():

def load_games():

    r = requests.get(URL)
    soup = BeautifulSoup(r.text,"html.parser")

    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)

    games = []

    for row in soup.select("tr"):

        text = row.get_text(" ",strip=True)

        if ":" not in text:
            continue

        if "Herren" in text:
            continue

        if not any(j in text for j in ["A-Junioren","B-Junioren","C-Junioren","D-Junioren","E-Junioren","F-Junioren","G-Junioren"]):
            continue

        parts = text.split()

        try:

            datum = parts[0]
            zeit = parts[1]

            tag,monat,jahr = datum.split(".")
            datum_obj = datetime.date(int(jahr),int(monat),int(tag))

            if datum_obj < monday or datum_obj > sunday:
                continue

            heim = parts[2] + " " + parts[3]
            gast = parts[4] + " " + parts[5]

            ort = parts[-1]

            heim = shorten_opponent(heim)
            gast = shorten_opponent(gast)

            ort = shorten_place(ort)

            games.append((datum,f"{heim} – {gast}",zeit,ort))

        except:
            pass

    return games

def create_story(games,start,end,prefix):

    pages = [games[i:i+MAX_SPIELE] for i in range(0,len(games),MAX_SPIELE)]

    index = 1

    for page in pages:

        img = Image.new("RGB",(WIDTH,HEIGHT),"black")
        draw = ImageDraw.Draw(img)

        title = f"{prefix} {start.strftime('%d.%m')} - {end.strftime('%d.%m')}"

        draw.text((120,150),title,fill="white",font=font)

        y = 350
        toggle = True

        for datum,teams,zeit,ort in page:

            bg = (255,255,255) if toggle else (212,175,55)

            draw.rectangle((80,y-20,1000,y+60),fill=bg)

            text = f"{datum}  {teams}  {zeit}  {ort}"

            draw.text((100,y),text,fill="black",font=font)

            toggle = not toggle
            y += 130

        img.save(f"output/{index:02d}_{prefix}.png")

        index += 1


# Spielplan aktuelle Woche
start,end = get_week_dates(0)
games = load_games()

create_story(games,start,end,"spielplan")

# Ergebnisse letzte Woche
start,end = get_week_dates(-7)

create_story(games,start,end,"ergebnisse")

print("Generator fertig")


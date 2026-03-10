import os
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont

os.makedirs ("output", exist_ok=True)

VEREIN_ID="00ES8GNBC800007OVV0AG08LVUPGND5I"

WIDTH=1080
HEIGHT=1920
MAX_SPIELE=6

font=ImageFont.load_default()

def clean_ort(text):

    if not text:
        return ""

    words=text.split()

    if len(words)>=2 and words[0].lower()=="st.":
        ort=words[0]+words[1]
    else:
        ort=words[0]

    return ort.upper()

def shorten_opponent(name):

    name=name.replace(" e.V.","")

    if "JSG" in name:

        part=name.split("JSG")[1].strip()

        part=part.replace("III"," 3")
        part=part.replace("II"," 2")
        part=part.replace("IV"," 4")

        return "JSG "+part.upper()

    if "/" in name:
        name=name.split("/")[0]

    words=name.split()

    prefixes=["SV","SG","FC","VFB","TUS","TSV","SC"]

    if words[0].upper() in prefixes and len(words)>1:

        club=words[1]

        if len(words)>2 and words[2] in ["II","III","IV"]:

            number={"II":"2","III":"3","IV":"4"}[words[2]]
            return f"{words[0].upper()} {club.upper()} {number}"

        return f"{words[0].upper()} {club.upper()}"

    if len(words)>1 and words[1] in ["II","III","IV"]:

        number={"II":"2","III":"3","IV":"4"}[words[1]]
        return f"{words[0].upper()} {number}"

    return words[0].upper()

def convert_team(name,liga):

    if "A-Junioren" in name: return "JSG A"
    if "B-Junioren" in name: return "JSG B"
    if "C-Junioren" in name: return "JSG C"
    if "D-Junioren" in name: return "JSG D"

    if "E-Junioren" in name:
        if "Kreisliga" in liga: return "JSG E1"
        else: return "JSG E2"

    if "F-Junioren" in name: return "JSG F"
    if "G-Junioren" in name: return "JSG G"

    return None

def next_week():

    today=datetime.date.today()

    monday=today+datetime.timedelta(days=-today.weekday(),weeks=1)
    sunday=monday+datetime.timedelta(days=6)

    return monday,sunday

def last_week():

    today=datetime.date.today()

    monday=today+datetime.timedelta(days=-today.weekday()-7)
    sunday=monday+datetime.timedelta(days=6)

    return monday,sunday

def draw_story(rows,title,week,name,start):

    os.makedirs("output",exist_ok=True)

    pages=[rows[i:i+MAX_SPIELE] for i in range(0,len(rows),MAX_SPIELE)]

    index=start

    for games in pages:

        img=Image.new("RGB",(WIDTH,HEIGHT),"black")
        draw=ImageDraw.Draw(img)

        draw.text((120,120),title,fill="white",font=font)
        draw.text((120,180),week,fill="white",font=font)

        y=350
        toggle=True

        for text,color in games:

            if name=="spielplan":

                bg=(255,255,255) if toggle else (212,175,55)

                draw.rectangle((80,y-20,1000,y+60),fill=bg)
                draw.text((100,y),text,fill="black",font=font)

                toggle=not toggle

            else:

                draw.rectangle((80,y-20,1000,y+60),fill="white")
                draw.text((100,y),text,fill=color,font=font)

            y+=130

        file=f"output/{index:02d}_{name}.png"

        img.save(file)

        index+=1

    return index

spielplan=[]
ergebnisse=[]

nm,ns=next_week()
lm,ls=last_week()

try:

    url=f"https://www.fussball.de/api/club/matches/{VEREIN_ID}"

    r=requests.get(url,timeout=20)

    data=r.json()

    for m in data["matches"]:

        team=convert_team(m["teamName"],m.get("competitionName",""))

        if not team: continue

        gegner=shorten_opponent(m["opponentName"])

        datum=datetime.datetime.strptime(m["matchDate"][0:10],"%Y-%m-%d").date()

        zeit=m.get("matchTime","")

        ort=clean_ort(m.get("venue",""))

        teams=f"{team} vs {gegner}"

        if nm<=datum<=ns:

            text=f"{datum.strftime('%d.%m')}  {teams}  {zeit}  {ort}"

            spielplan.append((text,"black"))

        if m.get("result") and lm<=datum<=ls:

            if team in ["JSG F","JSG G"]:

                text=f"{datum.strftime('%d.%m')}  {teams}  KINDERFUSSBALL"

                ergebnisse.append((text,"black"))

            else:

                result=m["result"]

                h,g=map(int,result.split(":"))

                color="black"

                if h>g: color="green"
                if h<g: color="red"

                text=f"{datum.strftime('%d.%m')}  {teams}  {result}"

                ergebnisse.append((text,color))

except:
    print("Fehler beim Laden")

index=1

week1=f"{nm.strftime('%d.%m')} – {ns.strftime('%d.%m')}"
week2=f"{lm.strftime('%d.%m')} – {ls.strftime('%d.%m')}"

index=draw_story(spielplan,"SPIELPLAN",week1,"spielplan",index)

draw_story(ergebnisse,"ERGEBNISSE",week2,"ergebnisse",index)

print("Fertig")


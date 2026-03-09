import datetime
import json
import os

print("JSG Kalmit Generator gestartet")

# heutiges Datum
today = datetime.date.today()

print("Heute:", today)

# Beispielspiele (Test)
spiele = [
    {
        "datum": "09.03",
        "team": "JSG C",
        "gegner": "Seebach",
        "zeit": "18:30",
        "ort": "St. Martin",
        "typ": "spielplan"
    },
    {
        "datum": "14.03",
        "team": "JSG E1",
        "gegner": "Hassloch",
        "zeit": "11:00",
        "ort": "Hassloch",
        "typ": "spielplan"
    },
    {
        "datum": "07.03",
        "team": "JSG B",
        "gegner": "Landau",
        "ergebnis": "3:1",
        "typ": "ergebnis"
    }
]

print("Gefundene Spiele:", len(spiele))

spielplan = []
ergebnisse = []

for spiel in spiele:

    if spiel["typ"] == "spielplan":
        spielplan.append(spiel)

    if spiel["typ"] == "ergebnis":
        ergebnisse.append(spiel)

print("Spielplan Spiele:", len(spielplan))
print("Ergebnis Spiele:", len(ergebnisse))

# Ausgabe Dateien erstellen
os.makedirs("output", exist_ok=True)

with open("output/spielplan.txt", "w") as f:
    for s in spielplan:
        f.write(f'{s["datum"]} {s["team"]} vs {s["gegner"]} {s["zeit"]} {s["ort"]}\n')

with open("output/ergebnisse.txt", "w") as f:
    for s in ergebnisse:
        f.write(f'{s["team"]} vs {s["gegner"]} {s["ergebnis"]}\n')

print("Dateien erstellt!")







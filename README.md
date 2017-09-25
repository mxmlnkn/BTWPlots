# Schnelles Visualisierungsskript für die Bundestagswahlergebnisse

Ein Skript, was die Karte von [Wikipedia](https://de.wikipedia.org/wiki/Datei:Bundestagswahlkreise_2017.svg) gemäß der erreichten Prozente für die Zweitstimme unter zuhilfename des natural-break-Algorithmus einfärbt. Hiermit sind regionale Präferenzen für bestimmte Parteien visualisierbar. CSU wird als CDU gewertet. Die Daten sind vom [Bundesamt für Statistik](https://www.bundeswahlleiter.de/bundestagswahlen/2017/wahlkreiseinteilung/umgerechnete-ergebnisse.html).

# 2013

## Verteilung der Ergebnisse

Aus Interesse wurde die Verteilung der Prozente visualisiert. Ein direkter Plot der Prozente über die Wahlkreisnummer:
![Parties](parties.png)
Und ein weiterer Plot, wo die Prozente sortiert sind. Es ist also wie eine Platzierungsliste zu betrachten, gibt aber interessante Einblicke in die Verteilung der Ergebnisse. Z.B. sieht man bei der Linken einen Sprung von 10% auf 20%. Das heißt es gibt eine Gruppe von Wahlbezirken die signifikant höher liegt als die restlichen. Interessant ist auch dass die Verteilung für die CDU beinahe enie perfekte um 90° rotierte Sigmoidkurve ist.
![result distributions](https://github.com/mxmlnkn/BTWPlots/blob/master/parties-distributions.png)

## Räumliche Verteilung

### Übersicht
![Übersicht](/btw-small.png)

### CDU/CSU
![CDU/CSU](/btw-CDU.png)

### SPD
![SPD](/btw-SPD.png)

### Die Linke
![Die Linke](/btw-DIE%20LINKE.png)

### Grüne
![Grüne](/btw-GR%C3%9CNE.png)

### AfD
![AfD](/btw-AfD.png)

### FDP
![FDP](/btw-FDP.png)

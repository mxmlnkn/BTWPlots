#!/bin/bash

python3 ./jenks2.py
parties=( 'CDU' 'SPD' 'FDP' 'DIE LINKE' 'GRÜNE' 'AfD' )
for party in "${parties[@]}"; do
    cssFile="kreise.$party.svg"
    if [ -f "$cssFile" ]; then
        cat 'kreise.header.svg' "$cssFile" 'kreise.body.svg' > "btw-$party.svg"
        inkscape -z -e "btw-$party."{png,svg}
    else
        echo "Couldn't find '$cssFile'"
    fi
done
convert +append btw-*.png btw.png

#!/bin/bash

# wget 'https://www.bundeswahlleiter.de/dam/jcr/8e88ad23-18ad-4685-9ded-f50988351ebd/Geometrie_Wahlkreise_19DBT_svg.zip'
# unzip 'Geometrie_Wahlkreise_19DBT_svg.zip'
# 'cp' 'Geometrie_Wahlkreise_19DBT.svg' tmp.svg
# for (( i=1; i<=299; ++i )); do
#   echo $i
#   sed -i '0,/fill="none"/{s|fill="none"|class="kreis'$i'"|}' tmp.svg
# done
# sed '/<svg/,/>/{ s|>|>ioubfibuiq| }' tmp.svg | sed '/ioubfibuiq/q' | sed 's|ioubfibuiq||' > 'kreise.header.svg'
# echo '<defs><style type="text/css"><![CDATA[' >> 'kreise.header.svg'
# sed '/<svg/,/>/{ s|>|>ioubfibuiq| }' tmp.svg | sed '0,/ioubfibuiq/d' > 'kreise.body.svg.tmp'
# echo ']]></style></defs>' > 'kreise.body.svg'
# cat 'kreise.body.svg.tmp' >> 'kreise.body.svg'

# Test loop to check wahlkreisnummern -.-
# for (( i=1; i<=299; ++i )); do
#   echo $i
#   echo '.kreis'$i' { fill: red; }' > tmp.css
#   cat 'kreise.header.svg' 'kreise.css.svg' 'tmp.css' 'kreise.body.svg' > 'btw-css.svg'
#   # xdotool search --name '.*btw-css.svg' key F5
#   xdotool key --window 0x7400012 F5
#   read -n 1
# done
# #  1-23 korrekt -> problem is that 24  Aurich for some reason is missing in the sequence -.-
# #  24-136 += 1
# #  138 Hagen is missing -.- in sequence
# #  137-297 +=2
# #  298 -> 24
# #  299 -> 138
#
# for (( i=1; i<=299; ++i )); do
#   if [ $i -eq 298 ]; then j=24
#   elif [ $i -eq 299 ]; then j=138
#   elif [ $i -lt 24 ]; then j=$i
#   elif [ $i -lt 137 ]; then j=$((i+1))
#   elif [ $i -lt 298 ]; then j=$((i+2))
#   fi
#   echo "$i -> $j"
#   sed -i '0,/fill="none"/{s|fill="none"|class="kreis'$j'"|}' tmp.svg
# done
#
#


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
rm btw-small.png
convert +append btw-*.png -trim btw.png
convert -resize 25%x25% btw{,-small}.png

# 'mv' btw*.{png,svg} parties-*.{png,svg} Results/2017


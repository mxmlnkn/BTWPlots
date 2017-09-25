#!/bin/bash

getUrls() { sed 's|<a href="|\nKEEP!!|g' "$1" | sed '/^KEEP!!/!d; s/KEEP!!//; s/".*$//g; s/ /%20/g'; }

mkdir -p '2017'
wget -q -O a 'https://www.bundeswahlleiter.de/bundestagswahlen/2017/ergebnisse.html'
for land in $( getUrls a | sed -n '/ergebnisse\/.*land-.*\.html/p' ); do
    url='https://www.bundeswahlleiter.de/bundestagswahlen/2017/'"$land"
    wget -q -O a "$url"
    for wk in $( getUrls a | sed -nr '/land-[0-9]+\/wahlkreis-[0-9]+.html/p' ); do
        wget -q -O a "${url%/*}/$wk"
        wk=${wk#*wahlkreis-}
        wk=${wk%.html}
        echo "Wahlkreis $wk"
        sed -n '/<table class="tablesaw table-stimmen"/,/<\/table>/p' a > "$wk.tmp"

        cat "$wk.tmp" |
            sed 's/^[\ \t]*//g' |
            tr -d '\r\n' |
            sed 's/<\/TR[^>]*>/\n/Ig
                 s|<caption>|# |Ig
                 s|</caption>|\n|Ig
                 s|<tbody[^>]*>||Ig
                 s|</tbody[^>]*>|\n|Ig
                 s|</thead[^>]*>|\n|Ig
                 s|<th[^>]*>|# |Ig
                 s/<\/\?\(TABLE\|TR\)[^>]*>//Ig' |
            sed 's/^<T[DH][^>]*>\|<\/\?T[DH][^>]*>$//Ig
                 s|</T[DH][^>]*><T[DH][^>]*>|;|Ig' > "2017/$wk.csv"
         if [ "$( cat "2017/$wk.csv" | wc -l )" -lt 5 ]; then
            echo -e "\e[31Something went wrong when parsing '$url' to '2017/$wk.csv'\e[0m"
         fi
         rm "$wk.tmp"
    done
done

# cat 18.tmp |
# # 'grep' -i -e '</\?TABLE\|</\?TD\|</\?TR\|</\?TH' |  # only keep lines corresponding to the table
# sed 's/^[\ \t]*//g' |   # remove beginning whitespaces
# tr -d '\r\n' |    # remove all line breaks
# sed 's/<\/TR[^>]*>/\n/Ig'  |    # put each <tr> on a new line
# sed 's/<\/\?\(TABLE\|TR\)[^>]*>//Ig' |
# sed 's/^<T[DH][^>]*>\|<\/\?T[DH][^>]*>$//Ig' |
# sed 's/<\/T[DH][^>]*><T[DH][^>]*>/,/Ig'



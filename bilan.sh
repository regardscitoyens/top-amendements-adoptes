#!/bin/bash

typeparl=$1

if [ -z "$typeparl" ]; then
  typeparl="deputes"
fi

function extract_column {
  awk -F ',' '{print $'"$1"'}' data/$typeparl-tops.csv | sed 's/(.*//' | grep -i [a-z] | grep -v "^[A-Z]\+$"
}

mkdir -p data/tops

extract_column 3  >  data/tops/SRC-SER.csv.tmp
extract_column 11 >> data/tops/SRC-SER.csv.tmp
extract_column 4  >  data/tops/UDI.csv.tmp
extract_column 5  >  data/tops/UMP-LR.csv.tmp
extract_column 10 >> data/tops/UMP-LR.csv.tmp
extract_column 12 >> data/tops/UMP-LR.csv.tmp
extract_column 6  >  data/tops/GDR.csv.tmp
extract_column 7  >  data/tops/NI.csv.tmp
extract_column 8  >  data/tops/ECOLO.csv.tmp
extract_column 9  >  data/tops/RRDP.csv.tmp

for groupe in SRC-SER UDI UMP-LR GDR NI ECOLO RRDP ; do
    sort "data/tops/"$groupe".csv.tmp" | uniq -c | sort -n | sed 's/^ *//' | sed 's/ /;/' > "data/tops/"$typeparl"_"$groupe".csv" 
    tail -n 1 "data/tops/"$typeparl"_"$groupe".csv" | awk -F ';' '{print $1}' | while read nb ; do
        grep ^$nb "data/tops/"$typeparl"_"$groupe".csv" | while read l ; do
            echo -n $l";"$groupe";"
            grep "$(echo $l | sed 's/.*;//')" data/$typeparl-tops.csv | awk -F ',' '{printf ("%d-%02d, ", $1, $2)}'
            echo 
        done
    done
done
rm data/tops/*tmp



awk -F ',' '{print $3}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_SRC-SER.csv.tmp
awk -F ',' '{print $4}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_UDI.csv.tmp
awk -F ',' '{print $5}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_UMP-LR.csv.tmp
awk -F ',' '{print $6}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_GDR.csv.tmp
awk -F ',' '{print $7}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_NI.csv.tmp
awk -F ',' '{print $8}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_ECOLO.csv.tmp
awk -F ',' '{print $9}' data/deputes-tops.csv  | sed 's/(.*//' | grep -i [a-z] >  data/tops_RRDP.csv.tmp
awk -F ',' '{print $10}' data/deputes-tops.csv | sed 's/(.*//' | grep -i [a-z] >> data/tops_UMP-LR.csv.tmp
awk -F ',' '{print $11}' data/deputes-tops.csv | sed 's/(.*//' | grep -i [a-z] >> data/tops_SRC-SER.csv.tmp
awk -F ',' '{print $12}' data/deputes-tops.csv | sed 's/(.*//' | grep -i [a-z] >> data/tops_UMP-LR.csv.tmp

for groupe in SRC-SER UDI UMP-LR GDR NI ECOLO RRDP ; do
    sort "data/tops_"$groupe".csv.tmp" | uniq -c | sort -n | sed 's/^ *//' | sed 's/ /;/' > "data/tops_"$groupe".csv" 
    tail -n 1 "data/tops_"$groupe".csv" | awk -F ';' '{print $1}' | while read nb ; do grep ^$nb "data/tops_"$groupe".csv" | while read l ; do
        echo -n $l";"$groupe";"
        grep "$(echo $l | sed 's/.*;//')" data/deputes-tops.csv | awk -F ',' '{printf ("%d-%02d, ", $1, $2)}'
        echo 
    done; done
done
rm data/*tmp

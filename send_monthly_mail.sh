#!/bin/bash
# USAGE: ./send_monthly_mail.sh <not a test>
# i.e.  test: ./send_monthly_mail.sh
# not a test: ./send_monthly_mail.sh 1

cd $(dirname $0)
pwd
source config.sh
source $(which virtualenvwrapper.sh)
workon baro-amdmts

istest=""
dest="-c $TEST_EMAIL $DEST_EMAIL"
if [ -z "$1" ]; then
  istest="[TEST] "
  dest="$TEST_EMAIL"
fi

for typeparl in deputes senateurs; do
  ls data/$typeparl-*.json | tail -1 | while read f; do
    rm -f $f;
  done
  ./build_tops.py $typeparl
done

month=`ls data/deputes-*.json | tail -1 | sed 's/[^0-9]//g' | sed 's/\(..\)\(..\)/\2\/20\1/'`

./print_last_tops.py |
  iconv -f UTF8 -t ISO8859-1 |
  mail -a "Content-Type: text/plain; charset=ISO-8859-1; format=flowed" -a "From: Regards Citoyens <contact@regardscitoyens.org>" -s "${istest}Barometre deputes et senateurs - $month" $dest

deactivate

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, json, sys
from datetime import date
from subprocess import call

typeparls = sys.argv[1] if len(sys.argv) > 1 else "deputes"

parl_file = os.path.join(".cache", "%s.json" % typeparls)
if os.path.isfile(parl_file):
    os.remove(parl_file)

since = (12, 6)
now = (date.today().year - 2000, date.today().month)

months = []
groupes = []

while since < now:
    date = "%02d%02d" % since
    month_file = os.path.join("data", "%s-%s.json" % (typeparls, date))

    if not os.path.isfile(month_file):
        call(["python", "build_month.py", typeparls, date])

    with open(month_file) as f:
        data = json.load(f)

        month = {
          u"année": str(since[0] + 2000),
          "mois": str(since[1])
        }

        for g in data:
            if g not in groupes:
                groupes.append(g)
            month[g] = u"%s (%s adoptés - %2.1f%s)" % (data[g]["nom"], data[g][u"adoptés"], data[g]["taux_adoption"], "%")
        months.append(month)

        if since[1] == 12:
            since = (since[0] + 1, 1)
        else:
            since = (since[0], since[1] + 1)

headers = [u"année", "mois"] + groupes
with open(os.path.join("data", "%s-tops.csv" % typeparls), "w") as f:
    print >> f, ",".join([h.encode("utf-8") for h in headers])
    for m in months:
        print >> f, ",".join([m[h].encode("utf-8") if h in m else "" for h in headers])

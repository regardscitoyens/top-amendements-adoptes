#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, sys, requests, json
from pprint import pprint

date = sys.argv[1]
typeparl = sys.argv[2]
typeparls = "%ss" % typeparl
print typeparls, date
for dirs in [".cache", "data"]:
    if not os.path.isdir(dirs):
        os.makedirs(dirs)

parl_file = os.path.join(".cache", "%s.json" % typeparls)
if not os.path.isfile(parl_file):
    parls = {}
    for d in requests.get("http://www.nos%s.fr/%s/json" % (typeparls, typeparls)).json()[typeparls]:
        parls[str(d[typeparl]["id"])] = d[typeparl]["slug"]
    with open(parl_file, "w") as f:
        json.dump(parls, f)
else:
    with open(parl_file, "r") as f:
        parls = json.load(f)

data = requests.get("http://www.nos%s.fr/synthese/%s/json" % (typeparls, date)).json()[typeparls]

groupes = {}
for parl in data:
    d = parl[typeparl]
    d[u"signés"] = int(d["amendements_signes"])
    d[u"adoptés"] = int(d["amendements_adoptes"])
    d["taux_adoption"] = 100 * float(d[u"adoptés"]) / d[u"signés"] if d[u"signés"] else 0
    if d[u"adoptés"] and (d["groupe"] not in groupes or \
      groupes[d["groupe"]][u"adoptés"] < d[u"adoptés"] or \
      (groupes[d["groupe"]][u"adoptés"] == d[u"adoptés"] and groupes[d["groupe"]]["taux_adoption"] < d["taux_adoption"])):
        groupes[d["groupe"]] = {
          "nom": d["nom"],
          u"signés": d[u"signés"],
          u"adoptés": d[u"adoptés"],
          "taux_adoption": d["taux_adoption"],
          "photo": "http://www.nos%s.fr/%s/photo/%s/120" % (typeparls, typeparl, parls[str(d["id"])])
        }


with open(os.path.join("data", "%s-%s.json" % (typeparls, date)), "w") as f:
    json.dump(groupes, f, indent=4)

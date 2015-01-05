#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path, sys, requests, json
from pprint import pprint

date = sys.argv[1]
print date
for dirs in [".cache", "data"]:
    if not os.path.isdir(dirs):
        os.makedirs(dirs)

dep_file = os.path.join(".cache", "deputes.json")
if not os.path.isfile(dep_file):
    deputes = {str(d["depute"]["id"]): d["depute"]["slug"] for d in requests.get("http://www.nosdeputes.fr/deputes/json").json()["deputes"]}
    with open(dep_file, "w") as f:
        json.dump(deputes, f)
else:
    with open(dep_file, "r") as f:
        deputes = json.load(f)

data = requests.get("http://www.nosdeputes.fr/synthese/%s/json" % date).json()["deputes"]

groupes = {}
for dep in data:
    d = dep["depute"]
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
          "photo": "http://www.nosdeputes.fr/depute/photo/%s/120" % deputes[str(d["id"])]
        }


with open(os.path.join("data", "%s.json" % date), "w") as f:
    json.dump(groupes, f, indent=4)

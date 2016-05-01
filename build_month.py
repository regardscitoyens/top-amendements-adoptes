#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

from cpc_api import CPCApi
import os.path
import sys
import json


def get_or_set_cache(name, func, cache_dir='.cache'):
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    file_path = os.path.join(cache_dir, name)

    if not os.path.isfile(file_path):
        data = func()
        with open(file_path, "w") as f:
            json.dump(data, f)
    else:
        with open(file_path) as f:
            data = json.load(f)

    return data


def get_months_data(typeparls, datebegin, dateend):
    api = CPCApi(ptype=typeparls[:-1])

    parls = get_or_set_cache("%s.json" % typeparls,
      lambda: dict((str(parl_['id']), parl_) for parl_ in api.parlementaires()))

    synthese = {}

    for idate in range(int(datebegin), int(dateend) + 1) :
      date = str(idate)

      synthese_mois = api.synthese(date)

      for parl in synthese_mois:
        try:
          synthese[parl['id']][u"signés"] += int(synthese[parl['id']]["amendements_signes"])
          synthese[parl['id']][u"adoptés"] += int(synthese[parl['id']]["amendements_adoptes"])
          synthese[parl['id']]["amendements_signes"] = str(synthese[parl['id']][u"signés"])
          synthese[parl['id']]["amendements_adoptes"]= str(synthese[parl['id']][u"adoptés"])
        except KeyError:
          synthese[parl['id']] = parl
          synthese[parl['id']][u"signés"] = int(synthese[parl['id']]["amendements_signes"])
          synthese[parl['id']][u"adoptés"] = int(synthese[parl['id']]["amendements_adoptes"])

    groupes = {}

    for parl in synthese.values():

        parl[u"signés"] = int(parl["amendements_signes"])
        parl[u"adoptés"] = int(parl["amendements_adoptes"])
        parl["taux_adoption"] = 100 * parl[u"adoptés"] / parl[u"signés"] if parl[u"signés"] else 0

        parl_groupe = parl["groupe"]
        if parl[u"adoptés"] and (parl_groupe not in groupes or \
            groupes[parl_groupe][u"adoptés"] < parl[u"adoptés"] or \
            (groupes[parl_groupe][u"adoptés"] == parl[u"adoptés"] and groupes[parl_groupe][
            "taux_adoption"] < parl["taux_adoption"])):

            groupes[parl_groupe] = {
                "nom": parl["nom"],
                u"signés": parl[u"signés"],
                u"adoptés": parl[u"adoptés"],
                "taux_adoption": parl["taux_adoption"],
                "photo": api.picture_url(parls[str(parl["id"])]["slug"], pixels="120")
            }

    return groupes


if __name__ == '__main__':
    typeparls = sys.argv[1]
    datebegin = sys.argv[2]
    try:
      dateend = sys.argv[3]
      filename = "%s-%s-%s.json" % (typeparls, datebegin, dateend)
    except IndexError:
      dateend = datebegin
      filename = "%s-%s.json" % (typeparls, datebegin)

    print typeparls, datebegin, dateend

    with open(os.path.join("data", filename), "w") as f:
        json.dump(get_months_data(typeparls, datebegin, dateend), f, indent=4)

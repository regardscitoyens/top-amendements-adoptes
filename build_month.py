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
        data = json.load(open(file_path))

    return data


def get_month_data(typeparls, date):
    api = CPCApi(ptype=typeparls[:-1])

    parls = get_or_set_cache("%s.json" % typeparls, lambda: dict((str(parl_['id']), parl_) for parl_ in api.parlementaires()))
    synthese = api.synthese(date)

    groupes = {}

    for parl in synthese:
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
    date = sys.argv[1]
    typeparls = sys.argv[2]

    print typeparls, date

    with open(os.path.join("data", "%s-%s.json" % (typeparls, date)), "w") as f:
        json.dump(get_month_data(typeparls, date), f, indent=4)
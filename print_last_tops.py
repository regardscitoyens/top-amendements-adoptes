#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import re

def unicode_print(s):
    print s.encode("utf-8")

re_adoptes = re.compile(r'\((\d+) adopt')
get_adoptes = lambda x: int(re_adoptes.search(x).group(1)) if x else 0

def get_last_tops(typeparls):
    with codecs.open("data/%s-tops.csv" % typeparls, encoding="utf-8") as f:
        rows = f.readlines()
        headers = rows[0].strip('\n').split(',')
        tops = dict((header.strip(), value.strip()) for header, value in zip(headers, rows[-1].split(',')))
        tops["groupes"] = [v for v, _ in sorted(
          [(header, get_adoptes(tops[header]))
            for header in headers
            if header not in [u"mois", u"année"]
          ], key=lambda x: -x[1])]
        return tops

top_deputes = get_last_tops("deputes")
top_senateurs = get_last_tops("senateurs")

unicode_print(u"Baromètre des députés %.2d/%s" % (int(top_deputes[u"mois"]), top_deputes[u"année"]))

print "-" * 50

for groupe in top_deputes["groupes"]:
    if top_deputes[groupe]:
        unicode_print("%s : %s" % (groupe, top_deputes[groupe]))

print " " * 50 + "\n"
print " " * 50 + "\n"

unicode_print(u"Baromètre des sénateurs %.2d/%s" % (int(top_deputes[u"mois"]), top_deputes[u"année"]))

print "-" * 50

for groupe in top_senateurs["groupes"]:
    if top_senateurs[groupe]:
        unicode_print(u"%s : %s" % (groupe, top_senateurs[groupe]))

print " " * 50 + "\n"
print " " * 50 + "\n"
print "---"
print "Regards Citoyens"
print " " * 50 + "\n"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs


def unicode_print(s):
    print s.encode("utf-8")


def get_last_tops(typeparls):
    with codecs.open("data/%s-tops.csv" % typeparls, encoding="utf-8") as f:
        rows = f.readlines()
        headers = rows[0].split(',')
        tops = dict((header.strip(), value.strip()) for header, value in zip(headers, rows[-1].split(',')))
        tops["groupes"] = [header.strip() for header in headers if header not in [u"mois", u"année"]]
        return tops

top_deputes = get_last_tops("deputes")
top_senateurs = get_last_tops("senateurs")

unicode_print(u"Baromètre des députés %.2d/%s" % (int(top_deputes[u"mois"]), top_deputes[u"année"]))

print "-" * 50

for groupe in top_deputes["groupes"]:
    unicode_print("%s : %s" % (groupe, top_deputes[groupe]))

print " " * 50
print " " * 50

unicode_print(u"Baromètre des sénateurs %.2d/%s" % (int(top_deputes[u"mois"]), top_deputes[u"année"]))

print "-" * 50

for groupe in top_senateurs["groupes"]:
    unicode_print(u"%s : %s" % (groupe, top_senateurs[groupe]))

print " " * 50
print "---"
print "Regards Citoyens"
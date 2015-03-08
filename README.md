Baromètre amendements adoptés L'Hémicycle
-----------------------------------------

- Dépendances :

```bash
  pip install -r requirements.txt
```

- Pour générer toutes les données et la version agrégée :

```bash
  python build_tops.py deputes
  python build_tops.py senateurs
```

- Pour générer les données d'un mois :

```bash
  python build_month.py 1501 deputes
  python build_month.py 1209 deputes
  python build_month.py 1305 senateurs
```

Données issues de [NosDéputés.fr](http://www.nosdeputes.fr) et [NosSénateurs.fr](http://www.nossenateurs.fr) par [Regards Citoyens](http://www.regardscitoyens.org) sous [licence ODBL](http://vvlibri.org/fr/licence/odbl/10/fr/legalcode) pour le mensuel [L'Hémicycle](http://www.lhemicycle.com/).

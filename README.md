Baromètre amendements adoptés L'Hémicycle
-----------------------------------------

- Dépendances :

```bash
  sudo apt-get install pip
  sudo pip install virtualenv virtualenvwrapper
  source $(which virtualenvwrapper.sh)
  mkvirtualenv --no-site-packages baro-amdmts
  workon baro-amdmts
  pip install -r requirements.txt
  add2virtualenv .
  deactivate
```

- Pour générer toutes les données et la version agrégée :

```bash
  python build_tops.py deputes
  python build_tops.py senateurs
```

- Pour générer les données d'un mois :

```bash
  python build_month.py deputes 1501
  python build_month.py deputes 1209
  python build_month.py senateurs 1305
```

- Pour configurer l'envoi automatique du mail :

```bash
  cp config.sh{.example,}
```

Éditer les champs TEST_EMAILS et DEST_EMAILS et rêgler deux cron du type:
```bash
00 11  7 * *  <PATH TO REPO>/send_monthly_mail.sh
00 11  9 * *  <PATH TO REPO>/send_monthly_mail.sh 1 
```

Données issues de [NosDéputés.fr](http://www.nosdeputes.fr) et [NosSénateurs.fr](http://www.nossenateurs.fr) par [Regards Citoyens](http://www.regardscitoyens.org) sous [licence ODBL](http://vvlibri.org/fr/licence/odbl/10/fr/legalcode) pour le mensuel [L'Hémicycle](http://www.lhemicycle.com/).

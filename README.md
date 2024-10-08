﻿# Seminarska-naloga-UVP
## Predstavitev
Za seminarsko nalogo sem izbral analizo receptov na strani [okusno.je](https://okusno.je/). Na dan 14.08. 2024 je bilo na njej malo manj kot 6600 receptov. 
Stran objavlja tudi članke na temo trikov pri kuhanju, prehrane in  druge z njo povezane teme.

## Delovanje
Program deluje, tako da najprej iz prve strani z recepti iz gumba konec, ki te preusmeri na zadnjo stran z recepti, dobi število vseh strani z recepti. Program nato teče po teh straneh iz njih nabere povezave do samih receptov. Sproti povezave odpre in pobere iz recepta podatke o:
* Imenu recepta,
* Številu sestavin,
* Številu besed v receptu,
* Številu odstavkov,
* Težavnosti,
* Času priprave,
* Času kuhanja,
* Skupnemu času,
* Vrsti kuhinje,
* Energijski vrednosti na porcijo.
  
Te podatke nato zapiše v datoteko 'podatki.csv'.

## Navodila uporabe 
Če želite, pognati program sami naložite datoteke main.py, pomozne_funkcije.py, analiza_podatkov.ipynb in jih shranite v isto direktorijo. Da bo program deloval morate imeti naloženo knjižnico BeautifulSoup4. To naredite, tako da v ukazno vrstico napišete pip install BeautifulSoup4. Nato lahko poženete "analiza_podatkov.ipynb". Ta bo ustvaril datoteko "podatki.csv", kamor bo zapisoval podatke o receptih. Opozorilo, program, da dobi podatke o vseh receptih potrebuje preko 20 minut, zato program vrača v terminal svoje stanje o napredku. Zaradi časa nabiranja podatkov sem to naredil že jaz in z "#" naredil, da program ta korak preskoči. Več o temu sem napisal znotraj "analiza_podatkov.ipynb" v drugem odstavku. Ko program zaključi z nabiranjem podatkov bo opravil analizo s pomočjo knjižnice "Pandas".

 

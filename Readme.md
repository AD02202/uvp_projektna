# Program za analizo besed na portalu mojedelo.com

Avtor: Alja Dostal

Seminarska naloga pri predmetu Uvod v programiranje za analizo besed na portalu [mojedelo.com](https://www.mojedelo.com/).

Za vir podatkov sem uporabila portal [mojedelo.com](https://www.mojedelo.com/). Mojedelo.com je spletni portal, namenjen povezovanju iskalcev zaposlitve s podjetji, ki iščejo nove sodelavce. Deluje na področju Slovenije in ima več funkcij, ki omogočajo učinkovito iskanje zaposlitve in upravljanje kariere.

## Opis programa

Program v `projekt.ipynb` najprej shrani podatke o oglasih za službo s pomočjo `shrani.py`. Nato s pomočjo `obdelaj.py` pretvori html datoteke v csv datoteko. Na koncu z uporabo knjižnic pandas in matplotlib analizira prenesene podatke, jih grafično predstavi in naredi analizo najpogostejših besed, ki se uporabljajo v opisih oglasov.

## Navodila za uporabo

Za uporabo programa sledimo zvezku `projekt.ipynb`.


## Virtualno okolje

Aktivacija virtualnega okolja:

```
source venv/bin/activate
```

## Knjižnice
Inštalacija vseh potrebnih knjižnic:

```
pip3 install requests
pip3 install pandas
pip3 install matplotlib
```


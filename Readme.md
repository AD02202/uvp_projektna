# Program za analizo besed na portalu mojedelo.com

Repozitorij za program za analizo besed na portalu mojedelo.com. Zaključni projekt pri predmetu Uvod v programiranje na programu finančna matematika.

Avtor: Alja Dostal

## Uvod

Za vir podatkov sem uporabila portal [mojedelo.com](https://www.mojedelo.com/). Mojedelo.com je spletni portal, namenjen povezovanju iskalcev zaposlitve s podjetji, ki iščejo nove sodelavce. Deluje na področju Slovenije in ima več funkcij, ki omogočajo učinkovito iskanje zaposlitve in upravljanje kariere.


## Opis programa

Program v `projekt.ipynb` najprej shrani podatke o oglasih za sluzbo s pomocjo `shrani.py`. Nato s pomocjo `obdelaj.py` pretvori html datoteke v csv datoteko. Na koncu z uporabo knjiznic pandas in matplotlib analizira prenesene podatke, jih graficno predstavi in naredi analizo najpogostejsih besed, ki se uporabljajo v opisih oglasov.

## Navodila za uporabo

Za uporabo programa sledimo zvezku `projekt.ipynb`


## Virtualno okolje

Aktivacija virtualnega okolja:

```
source venv/bin/activate
```

## Knjiznice
Instalacija vseh potrebnih knjiznic:

```
pip3 install requests
pip3 install pandas
pip3 install matplotlib
```


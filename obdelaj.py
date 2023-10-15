import re
import os
import csv


class Sluzba():
    '''
    Razred sluzba predstavlja eno razpisano delovno mesto, vsaka sluzba ima ime, delodajalca, opis, kategorijo in regijo
    '''

    def __init__(self, ime, delodajalec, opis):
        # nastavimo zacetne vrednosti razen kategorije in regije, ki jih nastavimo naknadno
        self.ime = ime
        self.delodajalec = delodajalec
        self.opis = opis
        self.kategorija = None
        self.regija = None

    def __str__(self):
        '''
        Vrnemo niz, ki opisuje sluzbo
        '''
        return f"SLUZBA ime: {self.ime}, delodajalec: {self.delodajalec}, opis: {self.opis})"

    def pretvori_v_slovar(self):
        '''
        Vrnemo slovar, ki vsebuje polja sluzbe, ki ga lahko potem zapisemo v csv
        '''
        return {"ime": self.ime, "delodajalec": self.delodajalec, "opis": self.opis, "kategorija": self.kategorija, "regija": self.regija}


def load_string_from_file(filename):
    '''
    Ta funkcija prebere niz iz podane datoteke in ga vrne
    '''
    with open(filename, "r", encoding='utf-8') as file_in:
        text = file_in.read()
        return text


def get_job_data(job_text):
    '''
    Ta funkcija iz bloka html kode izlusci vse potrebne podatke o sluzbi
    '''

    # 1. IZLUSCIMO IME
    ime_vzorec = r'<h2 class="title">.*?</h2>'
    ime = re.search(ime_vzorec, job_text, flags=re.DOTALL).group()
    # odstranimo html znacke
    ime = ime.strip('<h2 class="title">').strip('</h2>')
    # odstranimo vejice, znake \n, narekovaje, ker bomo shranjevali v csv
    ime = ime.replace(',', ' ').replace('"', '').replace(
        '\n', '').replace('(m/ž)', '').replace('m/ž', '')

    # 2. IZLUSCIMO OPIS
    opis_vzorec = r'<p class="premiumDescription">.*?</p>'
    opis = re.search(opis_vzorec, job_text, flags=re.DOTALL)
    if opis != None:
        # odstranimo html znacke
        opis = opis.group().strip('<p class="premiumDescription">').strip('</p>')
        # odstranimo nepotrebne znake
        opis = opis.replace(',', ' ').replace('"', '').replace('\n', '')
    else:
        # Ce oglas nima opisa, ga filtriramo
        return None

    # 3. IZLUSCIMO DELODAJALCA
    delodajalec_vzorec = r'<div class="box-details-icon icon icon-home"></div>.*?<div class="detail">.*?</div>'
    delodajalec = re.search(delodajalec_vzorec, job_text,
                            flags=re.DOTALL).group()
    # odstranimo html znacke
    delodajalec = delodajalec.strip(
        '<div class="box-details-icon icon icon-home"></div>').strip('</div>')
    # odstranimo nepotrebne znake
    delodajalec = delodajalec.replace('\n', '').replace(
        '\t', '').strip(' ').replace(',', ' ').replace('"', '')

    delodajalec = delodajalec.strip('<div class=detail>')
    print(delodajalec)

    return Sluzba(ime, delodajalec, opis)


def izvozi_sluzbe(text):
    '''
    Ta funckija iz html datoteke potegne bloke, ki predstavljajo posamezne sluzbe
    '''
    vzorec = r'<div class="w-inline-block job-ad top w-clearfix">.*?<a.*?>.*?</a>'
    # bloki html kode, ki predstavljajo posamezno sluzbo
    sluzbe_texts = re.findall(vzorec, text, flags=re.DOTALL)
    # seznam ki hrani vse sluzbe
    sluzbe = []
    for sluzba in sluzbe_texts:
        prebrana_sluzba = get_job_data(sluzba)
        if prebrana_sluzba != None:
            sluzbe.append(prebrana_sluzba)
    return sluzbe


def load_category(path):
    '''
    Ta funkcija nalozi celotno mapo datotek oblike 1.html, 2.html, 3.html ... in iz njega
    izlusci podatke o sluzbah
    '''
    # seznam, ki hrani vse sluzbe
    sluzbe = []
    index = 1

    # dokler obstajajo datoteke 1,2,3... .html jih nalagamo
    while os.path.exists(path + '/' + str(index) + '.html'):
        text = load_string_from_file(path + '/' + str(index) + '.html')
        # izvozi sluzbe
        nove_sluzbe = izvozi_sluzbe(text)
        sluzbe.extend(nove_sluzbe)
        index += 1

    return sluzbe


def write_csv(sluzbe, mapa, filename, fieldnames):
    '''
    Ta funkcija zapise seznam sluzb v csv datoteko
    '''

    # naredi mapo, ce ne obstaja
    os.makedirs(mapa, exist_ok=True)
    # odpremo datoteko
    with open(mapa + '/' + filename, "w", encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # zapisemo prvo vrstico z imeni polj
        writer.writeheader()
        for sluzba in sluzbe:
            # zapisemo vsako vrstico
            writer.writerow(sluzba.pretvori_v_slovar())


def parse_data_to_csv():
    '''
    Ta funkcija obdela shranjene podatke v /podatki in jih shrani v csv datoteko.
    '''

    kategorije = ["bancnistvo-finance",
                  "matematika-fizika-in-naravoslovje", "upravljanje-svetovanje-vodenje"]
    regije = ["osrednjeslovenska", "obalna", "gorenjska"]

    # seznam v katerem so vse sluzbe
    vse_sluzbe = []
    for kategorija in kategorije:
        for regija in regije:
            sluzbe = load_category("podatki/" + regija + "/" + kategorija)

            for sluzba in sluzbe:
                # nastavimo kategorijo in regijo
                sluzba.kategorija = kategorija
                sluzba.regija = regija

            vse_sluzbe.extend(sluzbe)

    print("Stevilo vseh sluzb", len(vse_sluzbe))

    # imena polj v csv datoteki
    fieldnames = ["ime", "delodajalec", "opis", "kategorija", "regija"]
    # zapisemo sluzbe v csv datoteko
    write_csv(vse_sluzbe, "obdelani", "sluzbe.csv", fieldnames)

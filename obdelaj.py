import re
import os
import csv

kategorije = ["bancnistvo-finance", "matematika-fizika-in-naravoslovje", "upravljanje-svetovanje-vodenje"]
regije = ["osrednjeslovenska", "obalna", "gorenjska"]


class Sluzba():
    '''
    Razred sluzba predstavlja eno razpisano delovno mesto, vsaka sluzba ima ime, delodajalca, opis, kategorijo in regijo
    '''
    def __init__(self, ime, delodajalec, opis):
        self.ime = ime
        self.delodajalec = delodajalec
        self.opis = opis
        self.kategorija = None
        self.regija = None
        

    def __str__(self):
        return f"SLUZBA ime: {self.ime}, delodajalec: {self.delodajalec}, opis: {self.opis})"
    
    def to_dict(self):
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
    
    ime_vzorec = r'<h2 class="title">.*?</h2>'
    ime = re.search(ime_vzorec, job_text, flags=re.DOTALL).group()
    ime = ime.strip('<h2 class="title">').strip('</h2>')
    ime = ime.replace(',', ' ').replace('"', '').replace('\n', '')
    
    opis_vzorec = r'<p class="premiumDescription">.*?</p>'
    opis = re.search(opis_vzorec, job_text, flags=re.DOTALL)
    if opis != None:
        opis = opis.group().strip('<p class="premiumDescription">').strip('</p>')
        opis = opis.replace(',', ' ').replace('"', '').replace('\n', '')
    else:
        opis = ""

    delodajalec_vzorec = r'<div class="box-details-icon icon icon-home"></div>.*?<div class="detail">.*?</div>'
    delodajalec = re.search(delodajalec_vzorec, job_text, flags=re.DOTALL).group()
    delodajalec = delodajalec.strip('<div class="box-details-icon icon icon-home"></div>')
    delodajalec = delodajalec.replace('\n', '').replace('\t', '').strip(' ')
    delodajalec = delodajalec.strip('<div class="detail">').strip('</div>')
    delodajalec = delodajalec.replace(',', ' ').replace('"', '').replace('\n', '')
    
    return Sluzba(ime, delodajalec, opis)


def extract_jobs(text):
    '''
    Ta funckija iz html datoteke potegne bloke, ki predstavljajo posamezne sluzbe
    '''
    vzorec = r'<div class="w-inline-block job-ad top w-clearfix">.*?<a.*?>.*?</a>'
    sluzbe_texts = re.findall(vzorec, text, flags=re.DOTALL)
    sluzbe = []
    for sluzba in sluzbe_texts:
        sluzbe.append(get_job_data(sluzba)) 
    return sluzbe
   

def load_category(path):
    '''
    Ta funkcija nalozi celoten direktorij datotek oblike 1.html, 2.html, 3.html ... in iz njega
    izlusci podatke o sluzbah
    '''

    sluzbe = []
    index = 1
    while os.path.exists(path + '/' + str(index) + '.html'):
        text = load_string_from_file(path + '/' + str(index) + '.html')
        nove_sluzbe = extract_jobs(text)
        sluzbe.extend(nove_sluzbe)
        index += 1

    return sluzbe


def write_csv(sluzbe, directory, filename, fieldnames):
    os.makedirs(directory, exist_ok=True)
    with open(directory + '/' + filename, "w", encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for sluzba in sluzbe:
            writer.writerow(sluzba.to_dict())


if __name__ == "__main__":
    vse_sluzbe = []
    for kategorija in kategorije:
        for regija in regije:
            sluzbe = load_category("podatki/" + regija + "/" + kategorija)
            
            for sluzba in sluzbe:
                sluzba.kategorija = kategorija
                sluzba.regija = regija
            
            vse_sluzbe.extend(sluzbe)
    
    print("Stevilo vseh sluzb", len(vse_sluzbe))
    
    fieldnames = ["ime", "delodajalec", "opis", "kategorija", "regija"]
    write_csv(vse_sluzbe, "obdelani", "sluzbe.csv", fieldnames)

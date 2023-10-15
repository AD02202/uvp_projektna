import requests
import re
import os


def download_url_to_string(url):
    '''
    Ta funkcija nalozi vsebino spletne strani in jo vrne kot niz
    '''
    # s try ujamemo napako, ce spletna stran ni dostopna
    try:
        # poslji zahtevo na dani url in shrani text - html besedilo
        text = requests.get(url).text

    except requests.exceptions.RequestException:
        print('Ni mogoce najti spletne strani')
        return None
    return text


def save_text_to_file(text, mapa, filename):
    '''
    Ta funkcija shrani podani niz v datoteko v ustrezni mapi npr. podatki/gorenjska/bancnistvo-in-finance
    filename pove ime datoteke npr. 1.html
    '''
    # naredi mapo, ce se ne obstaja
    os.makedirs(mapa, exist_ok=True)
    # path je niz, v katerem se nahajata mapa in ime datoteke npr. podatki/gorenjska/bancnistvo-in-finance/1.html
    path = os.path.join(mapa, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        # shrani besedilo
        file_out.write(text)
    return None


def contains_jobs(text):
    '''
    Ta funkcija z regularnimi izrazi (regex) preveri, ali je v nizu html znacka za podatke o sluzbi
    '''
    vzorec = r'<div class="w-inline-block job-ad top w-clearfix">.*?<a.*?>.*?</a>'
    # vrnemo, ali smo nasli vzorec
    return bool(re.search(vzorec, text, flags=re.DOTALL))


def get_all_pages(osnovni_url, kategorija, regija):
    '''
    Ta funkcija v zanki nalaga nadaljne strani v doloceni kategoriji in regiji, dokler
    ji funkcija contains_jobs ne vrne, da stran ne vsebuje sluzb
    '''

    # generiramo ustrezni url
    url = osnovni_url + "/" + kategorija + "/" + regija
    # page steje, na kateri strani smo
    page = 1
    # maximalno_st_strani, ki jih bomo prenesli
    maximalno_st_strani = 10
    # nalozimo prvo stran
    text = download_url_to_string(url + "?p=" + str(page))

    # contains_jobs preveri, ali je spletna stran prazna (ne vsebuje nobenega oglasa)
    while contains_jobs(text) and page <= maximalno_st_strani:
        # primer mape: podatki/gorenjska/bancnistvo-finance, primer datoteke: 1.html
        save_text_to_file(text, "podatki/" + regija + "/" +
                          kategorija, str(page) + ".html")
        page += 1
        text = download_url_to_string(url + "?p=" + str(page))


def save_web_data():
    '''
    Ta funkcija shrani podatke iz spleta in jih shrani v ustrezno datoteko na disku
    '''

    link = "https://www.mojedelo.com/prosta-delovna-mesta"
    kategorije = ["bancnistvo-finance",
                  "matematika-fizika-in-naravoslovje", "upravljanje-svetovanje-vodenje"]
    regije = ["osrednjeslovenska", "obalna", "gorenjska"]

    for kategorija in kategorije:
        for regija in regije:
            get_all_pages(link, kategorija, regija)

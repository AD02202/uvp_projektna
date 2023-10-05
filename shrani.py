import requests
import re
import os


def download_url_to_string(url):
    '''
    Ta funkcija nalozi vsebino spletne strani in jo vrne kot niz
    '''
    try:
        response = requests.get(url)
        text = response.text
    except requests.exceptions.RequestException: 
        print('Ni mogoce najti spletne strani')
        return None
    return text


def save_text_to_file(text, directory, filename):
    '''
    Ta funkcija shrani podani niz v datoteko v ustrezni mapi
    '''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


def contains_jobs(text):
    '''
    Ta funkcija preveri, ali je v nizu html znacka za podatke o sluzbi
    '''
    vzorec = r'<div class="w-inline-block job-ad top w-clearfix">.*?<a.*?>.*?</a>'
    return bool(re.search(vzorec, text, flags=re.DOTALL))


def get_all_pages(osnovni_url, kategorija, regija):
    '''
    Ta funkcija v zanki nalaga nadaljne strani v doloceni kategoriji in regiji, dokler
    ji funkcija contains_jobs ne vrne, da stran ne vsebuje sluzb
    '''
    url = osnovni_url + "/" + kategorija + "/" + regija
    page = 1
    text = download_url_to_string(url + "?p=" + str(page))
    
    while contains_jobs(text) and page <= 10:
        save_text_to_file(text, "podatki/" + regija + "/" + kategorija, str(page) + ".html")
        page += 1
        text = download_url_to_string(url + "?p=" + str(page))


def save_web_data():
    link = "https://www.mojedelo.com/prosta-delovna-mesta"
    kategorije = ["bancnistvo-finance", "matematika-fizika-in-naravoslovje", "upravljanje-svetovanje-vodenje"]
    regije = ["osrednjeslovenska", "obalna", "gorenjska"]

    for kategorija in kategorije:
            for regija in regije:
                get_all_pages(link, kategorija, regija)    

from requests import get


link = "https://www.mojedelo.com/prosta-delovna-mesta/bancnistvo-finance/vse-regije"


def preberi_url(url):
    file = get(url)
    return file.text


if __name__ == "__main__":
    vsebina = preberi_url(link)

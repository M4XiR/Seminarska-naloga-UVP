import re
from bs4 import BeautifulSoup
import requests

def povprecen_cas(vrste_kuhinje,seznam):
    return str(seznam[vrste_kuhinje]//1)+" min"

def pretvori_cas(cas):
    cas = cas.lower()
    ure = re.search(r'(\d+)\s*h', cas)
    min = re.search(r'(\d+)\s*min', cas)
    if ure:
        ure = int(ure.group(1)) * 60
    else:
        ure = 0
    if min:
        min = int(min.group(1))
    else:
        min = 0
    return ure + min


def čas_priprave(html):
    vzorec_priprava = r'PRIPRAVA</span>\s*((\d+ h )?\d+ min)'
    čas_priprave = re.search(vzorec_priprava, html)
    if čas_priprave:
        return čas_priprave.group(1)
    else:
        return "0"


def čas_kuhanja(html):
    vzorec_kuhanje = r'KUHANJE</span>\s*((\d+ h )?\d+ min)'
    čas_kuhanja = re.search(vzorec_kuhanje, html)
    if čas_kuhanja:
        return čas_kuhanja.group(1)
    else:
        return "0"


def skupni_čas(html):
    vzorec_skupaj = r'SKUPAJ</span>\s*((\d+ h )?\d+ min)'
    čas_kuhanja = re.search(vzorec_skupaj, html)
    if čas_kuhanja:
        return čas_kuhanja.group(1)
    else:
        return "0"


def stevilo_sestavin(html):
    vzorec_sestavine = r'<div class="w-2/3 md:4/5 lg:w-2/3 p-8 leading-normal flex items-center">(.*?)</div>'
    sestavine = re.findall(vzorec_sestavine, html)
    if sestavine:
        return len(sestavine)
    else:
        return "ta recept nima sestavin"


def tezavnost(html):
    vzorec_tezavnosti = r'difficulty-(\d+)'
    tezavnost = re.search(vzorec_tezavnosti, html)
    if tezavnost:
        return tezavnost.group(1)
    else:
        return "ta recept nima težavnosti"


def vrsta_recepta(html):
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find('h2', class_='label bg-primary')

    if a:
        return a.text.strip()
    else:
        return "ta recept nima vrste"


def stevilo_besed_v_receptu(html):

    soup = BeautifulSoup(html, 'html.parser')
    odstavki = soup.find_all(
        'div', class_='leading-tight text-secondary dark:text-white/80 w-full font-semi transition hover:text-black dark:hover:text-white')
    stevec = 0
    for odstavek in odstavki:
        besedilo = odstavek.get_text()
        words = besedilo.split()
        stevec += len(words)
    if stevec == 0:
        return "To ni recept", "0"
    else:
        return stevec, len(odstavki)


def energijska_vrednost(html):
    pattern = r'(\d+\.?\d*)\s*kCal'

    vrednost = re.search(pattern, html)

    if vrednost:
        return vrednost.group(0).strip()
    else:
        return "ni podatka o energijski vrednosti"


def ime_recepta(html):
    soup = BeautifulSoup(html, 'html.parser')
    ime = soup.find('h1', class_='font-bold text-secondary dark:text-white text-20 md:text-28 leading-normal pt-0 p-16 md:pb-0 md:p-32 pb-0 bg-white dark:bg-slate-800 rounded-t-lg')
    if ime:
        return ime.text.strip()
    else:
        return "to ni recept"


def naloži_spletno_stran(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """

    try:
        # del kode, ki morda sproži napako
        headers = {"User-agent": "Chrome/124.0.6367.202"}
        vsebina_strani = requests.get(url, headers=headers)
    except requests.exceptions.RequestException:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Spletna stran ni dosegljiva")
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    return vsebina_strani.text

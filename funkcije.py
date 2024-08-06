import requests
from bs4 import BeautifulSoup
import os


def link_do_spletne_strani(stevilka_strani):
    return f"https://okusno.je/iskanje?t=recipe&sort=score&p={stevilka_strani}"


def naloži_spletno_stran(url):
    """Funkcija kot argument sprejme niz in poskusi vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        headers = {"User-agent": "Chrome/124.0.6367.202"}
        vsebina_strani = requests.get(url, headers=headers)
    except requests.exception.RequestException:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Spletna stran ni dosegljiva")
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    return vsebina_strani.text


def save_string_to_file(text, direktorija, ime_datoteke):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi. 
    """
    os.makedirs(direktorija, exist_ok=True)
    path = os.path.join(direktorija, ime_datoteke)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return 


#funkcija, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(stran, direktorija, ime_datoteke):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    text = naloži_spletno_stran(stran)
    save_string_to_file(text, direktorija, ime_datoteke)


povezava_do_prve_strani = link_do_spletne_strani(1)
stran = naloži_spletno_stran(povezava_do_prve_strani)
mapa_s_podatki = 'podatki'
ime_strani = "recepti.html" 
pot=os.path.join(os.getcwd(),mapa_s_podatki)





def stevilo_zavihkov(path,ime_datoteke):
    pot = os.path.join(path, ime_datoteke)
    with open(pot, 'r', encoding='utf-8') as html:
        # poišče število zavihkov na html strani
        soup = BeautifulSoup(html, 'html.parser')
    # tipka konec ima vrednost zadnje strani
    tipka_konec = soup.find('button', string='Konec »')
    vrednost = tipka_konec.get('value')
    return vrednost


st_zavihkov=stevilo_zavihkov(pot,"recepti.html")



def funkcija_ki_naloži_strani_z_recepti():
    for i in list(range(int(st_zavihkov))):
        i=str(int(i)+1)
        ime_strani_i="stran_z_recepti_"+f"{i}"+".html"
        save_frontpage(link_do_spletne_strani(i),pot,ime_strani_i)
        print(i)
    

def odpri_strani_receptov():
    
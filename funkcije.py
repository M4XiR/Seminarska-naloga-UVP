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

#



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
    
#funkcija_ki_naloži_strani_z_recepti()

def funkcija_ki_odpre_stran_z_receptom():
    for i in list(range(int(st_zavihkov))):
        i=str(int(i)+1)
        #odpri html datoteko
        ime_datoteke="stran_z_recepti_"+f"{i}"+".html"
        datoteka=os.path.join(pot, ime_datoteke)
        
        with open(datoteka, "r", encoding="utf-8") as html:
            #poišče linke do strani receptov
            soup=BeautifulSoup(html,'html.parser')
        seznam_vseh_linkov_do_receptov=soup.find_all('a', class_='group border border-black/10 dark:border-white/10 flex rounded-lg shadow-small flex-col h-full transition hover:shadow-center-large')
        
        #naloži strani receptov v direktorij recepti
        for a_znacka in seznam_vseh_linkov_do_receptov:
            href = a_znacka['href']
            link= f"https://okusno.je{href}"
            direktorija="recepti"
            ime_recepta=href[8:]+".html"
            
            save_frontpage(link, direktorija, ime_recepta)


#funkcija_ki_odpre_stran_z_receptom()


















#todo
#pobrati linke do receptov
#iz vsake strani recepta pobrati:
#seznam sestavin-število sestavin
#število besed v receptu
#težavnost recepta
#šas priprave
#energijska vrednost

import requests
import os
from bs4 import BeautifulSoup
import re
import csv


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
    except requests.exceptions.RequestException:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print("Spletna stran ni dosegljiva")
        return None
    # nadaljujemo s kodo če ni prišlo do napake
    return vsebina_strani.text



#######################################################################################

def stevilo_zavihkov():
    html = naloži_spletno_stran(link_do_spletne_strani(1))
    # poišče število zavihkov na html strani
    soup = BeautifulSoup(html, 'html.parser')
    # tipka konec ima vrednost zadnje strani
    tipka_konec = soup.find('button', string='Konec »')
    vrednost = tipka_konec.get('value')
    return vrednost


# def funkcija_ki_naloži_strani_z_recepti(pot):     useless
#    for i in list(range(int(stevilo_zavihkov()))):
#        i = str(int(i)+1)
#        ime_strani_i = "stran_z_recepti_"+f"{i}"+".html"
#        save_frontpage(link_do_spletne_strani(i), pot, ime_strani_i)
def funkcija_ki_vrne_seznam_linkov_do_receptov():
    seznam_vseh_linkov = []
    for i in list(range(int(1))):
        
    
    #for i in list(range(int(stevilo_zavihkov()))):

        i = str(int(i)+1)
        print(i)
        html = naloži_spletno_stran(link_do_spletne_strani(i))
    
    # poišče linke do strani receptov
        soup = BeautifulSoup(html, 'html.parser')
        seznam_vseh_linkov_do_receptov = soup.find_all('a', href=True, class_='group')
        for link in seznam_vseh_linkov_do_receptov:
            seznam_vseh_linkov.append("https://okusno.je"+link.get('href'))
        
        
    return seznam_vseh_linkov


#####################################################################################

def ime_recepta(html):
    soup = BeautifulSoup(html, 'html.parser')
    ime = soup.find('h1', class_='font-bold text-secondary dark:text-white text-20 md:text-28 leading-normal pt-0 p-16 md:pb-0 md:p-32 pb-0 bg-white dark:bg-slate-800 rounded-t-lg')
    if ime:
        return ime.text.strip()
    else:
        return "to ni recept"
    




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

################################################################################################


def main():
    seznam_linkov = funkcija_ki_vrne_seznam_linkov_do_receptov()
    števec_ni_recept = 0
    števec_receptov=0
    with open("podatki.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ime recepta", "Število sestavin", "Število besed v receptu", "Število odstavkov", "Težavnost",
                        "Čas priprave", "Čas kuhanja", "Skupni čas", "Vrsta kuhinje", "Energijska vrednost na porcijo"])
        
        for i in list(range(int(stevilo_zavihkov()))):
            i = str(int(i)+1)
            print("stran "+str(i)+" od " +str(stevilo_zavihkov()))
            html = naloži_spletno_stran(link_do_spletne_strani(i))
            seznam_linkov = []
            # poišče linke do strani receptov
            soup = BeautifulSoup(html, 'html.parser')
            seznam_vseh_linkov_do_receptov = soup.find_all('a', href=True, class_='group')
            for link in seznam_vseh_linkov_do_receptov:
                seznam_linkov.append("https://okusno.je"+link.get('href'))


            for link in seznam_linkov:      
                števec_receptov+=1      
                html = naloži_spletno_stran(link)
                ime_recept = ime_recepta(html)
                st_sestavin = stevilo_sestavin(html)
                število_besed_v_receptu, st_odstavkov = stevilo_besed_v_receptu(html)
                težavnost = tezavnost(html)
                priprava_čas = čas_priprave(html)
                kuhanje_čas = čas_kuhanja(html)
                čas_skupni = skupni_čas(html)
                vrsta_receptov = vrsta_recepta(html)
                energijska_vrednos = energijska_vrednost(html)
                print(str(števec_receptov)+". "+ime_recept)
                if število_besed_v_receptu == "to ni recept":
                    števec_ni_recept += 1
                    print(števec_ni_recept)
                    print(ime_recepta+število_besed_v_receptu)
                    pass
                elif st_sestavin == "ta recept nima sestavin":
                    števec_ni_recept += 1
                    print(števec_ni_recept)
                elif ime_recept=="to ni recept":
                    števec_ni_recept +=1
                    print(števec_ni_recept)
                else:
                    writer.writerow([ime_recept, st_sestavin, število_besed_v_receptu, st_odstavkov,
                                    težavnost, priprava_čas, kuhanje_čas, čas_skupni, vrsta_receptov, energijska_vrednos])
                
    print(števec_ni_recept)



main()

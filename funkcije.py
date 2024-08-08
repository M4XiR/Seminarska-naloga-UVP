import requests
from bs4 import BeautifulSoup
import os
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
pot = os.path.join(os.getcwd(), mapa_s_podatki)
direktorij = "recepti"
#########################################################################################################


def stevilo_zavihkov(path, ime_datoteke):
    pot = os.path.join(path, ime_datoteke)
    with open(pot, 'r', encoding='utf-8') as html:
        # poišče število zavihkov na html strani
        soup = BeautifulSoup(html, 'html.parser')
    # tipka konec ima vrednost zadnje strani
    tipka_konec = soup.find('button', string='Konec »')
    vrednost = tipka_konec.get('value')
    return vrednost


st_zavihkov = stevilo_zavihkov(pot, "recepti.html")


def funkcija_ki_naloži_strani_z_recepti():
    for i in list(range(int(st_zavihkov))):
        i = str(int(i)+1)
        ime_strani_i = "stran_z_recepti_"+f"{i}"+".html"
        save_frontpage(link_do_spletne_strani(i), pot, ime_strani_i)


# funkcija_ki_naloži_strani_z_recepti()---done


def funkcija_ki_odpre_stran_z_receptom():
    for i in list(range(int(st_zavihkov))):
        i = str(int(i)+1)
        # odpri html datoteko
        ime_datoteke = "stran_z_recepti_"+f"{i}"+".html"
        datoteka = os.path.join(pot, ime_datoteke)

        with open(datoteka, "r", encoding="utf-8") as html:
            # poišče linke do strani receptov
            soup = BeautifulSoup(html, 'html.parser')
        seznam_vseh_linkov_do_receptov = soup.find_all(
            'a', class_='group border border-black/10 dark:border-white/10 flex rounded-lg shadow-small flex-col h-full transition hover:shadow-center-large')

        # naloži strani receptov v direktorij recepti
        for a_znacka in seznam_vseh_linkov_do_receptov:
            href = a_znacka['href']
            link = f"https://okusno.je{href}"
            direktorija = "recepti"
            ime_recepta = href[8:]+".html"

            save_frontpage(link, direktorija, ime_recepta)


# funkcija_ki_odpre_stran_z_receptom()---done


# funkcija,ki naredi slovar, ključ je ime recepta, vrednost pa je tuple stvari, ki jih bom poiskal


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
    a=soup.find('h2', class_='label bg-primary')
    
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
    if stevec==0:
        return "to ni recept", "0"
    else:
        return stevec, len(odstavki)
# print(sestavine("v-pecici-pecene-mesne-kroglice-in-krompir.html",direktorij))


def energijska_vrednost(html):
    pattern = r'(\d+\.?\d*)\s*kCal'
    # dotall je zato da gre regex čez več vrstic, ker je v vrstici višje
    vrednost = re.search(pattern, html)
    
    if vrednost:
        return vrednost.group(0).strip()
    else:
        return "ni podatka o energijski vrednosti"


def zapisi_v_csv(direktorij):
    seznam_datotek = os.listdir(direktorij)
    števec_ni_recept=0
    with open("podatki.csv","w",encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ime recepta", "Število sestavin", "Število besed v receptu","Število odstavkov","Težavnost", "Čas priprave", "Čas kuhanja", "Skupni čas", "Vrsta kuhinje", "Energijska vrednost na porcijo"])
        for stran in seznam_datotek:
            datoteka = os.path.join(direktorij, stran)
            with open(datoteka, "r", encoding="utf-8") as file:
                html = file.read()
            ime_recepta = stran[:-5]
            st_sestavin = stevilo_sestavin(html)
            število_besed_v_receptu, st_odstavkov = stevilo_besed_v_receptu(html)
            težavnost = tezavnost(html)
            priprava_čas = čas_priprave(html)
            kuhanje_čas=čas_kuhanja(html)
            čas_skupni=skupni_čas(html)
            vrsta_receptov = vrsta_recepta(html)
            energijska_vrednos = energijska_vrednost(html)

            if število_besed_v_receptu=="to ni recept":
                števec_ni_recept+=1
                print(števec_ni_recept)
                print(ime_recepta+število_besed_v_receptu)
                pass
            elif st_sestavin=="ta recept nima sestavin":
                števec_ni_recept+=1
                print(števec_ni_recept)
            else:
                writer.writerow([ime_recepta.strip(), st_sestavin, število_besed_v_receptu,st_odstavkov,težavnost,priprava_čas,kuhanje_čas,čas_skupni,vrsta_receptov,energijska_vrednos])
                print(ime_recepta)
    print(števec_ni_recept)

#zapisi_v_csv(direktorij) done
ste=0
mnozica=set()
seznam_datotek = os.listdir(direktorij)
for stran in seznam_datotek:
    datoteka = os.path.join(direktorij, stran)
    with open(datoteka, "r", encoding="utf-8") as file:
            html = file.read()
    mnozica.add(vrsta_recepta(html))
    ste+=1
    print(ste)
with open("vrste.txt","w",encoding="utf-8") as file:
    for element in mnozica:
        file.write(element+"\n")
        print(element)



# def seznam_sestavin(direktorij):                                                               neuporabno
#    seznam_datotek = os.listdir(direktorij)
#    množica_sestavin=set()
#    for stran in seznam_datotek:
#        množica_sestavin.update(sestavine(stran,direktorij))
#        print(stran)
#    with open("seznam sestavin.txt","w",encoding="utf-8") as datoteka:
#        for element in množica_sestavin:
#            datoteka.write(element+"\n")
#
#
# seznam_sestavin(direktorij)

# test  čas_priprave("v-pecici-pecene-mesne-kroglice-in-krompir.html",direktorij)


# def število_besed_v_receptu(ime_datoteke):

    # todo
    # pobrati linke do receptov---done
    # iz vsake strani recepta pobrati:
    # seznam sestavin-število sestavin---done
    # število besed v receptu---done
    # težavnost recepta---done
    # šas priprave---done
    # energijska vrednost--done
    # zapiši v csv
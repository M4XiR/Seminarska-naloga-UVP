
from bs4 import BeautifulSoup
import csv
from pomozne_funkcije import čas_priprave, čas_kuhanja, skupni_čas, stevilo_sestavin, tezavnost, vrsta_recepta, stevilo_besed_v_receptu, energijska_vrednost, ime_recepta, naloži_spletno_stran


def link_do_spletne_strani(stevilka_strani):
    return f"https://okusno.je/iskanje?t=recipe&sort=score&p={stevilka_strani}"


#######################################################################################

def stevilo_zavihkov():
    html = naloži_spletno_stran(link_do_spletne_strani(1))
    # poišče število zavihkov na html strani
    soup = BeautifulSoup(html, 'html.parser')
    # tipka konec ima vrednost zadnje strani
    tipka_konec = soup.find('button', string='Konec »')
    vrednost = tipka_konec.get('value')
    return vrednost

################################################################################################

# pobere podatke iz strani in ustvari csv


def main():

    števec_ni_recept = 0
    števec_receptov = 0
    with open("podatki.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Ime recepta", "Število sestavin", "Število besed v receptu", "Število odstavkov", "Težavnost",
                        "Čas priprave", "Čas kuhanja", "Skupni čas", "Vrsta kuhinje", "Energijska vrednost na porcijo"])
        # vse povezave do strani so iste oblike zato lahko zanka teče po številih, ki jih dobi iz števila vseh strani
        for i in list(range(int(stevilo_zavihkov()))):
            i = str(int(i)+1)
            print("stran "+str(i)+" od " + str(stevilo_zavihkov()))
            html = naloži_spletno_stran(link_do_spletne_strani(i))
            seznam_linkov = []
            # poišče linke do strani receptov
            soup = BeautifulSoup(html, 'html.parser')
            seznam_vseh_linkov_do_receptov = soup.find_all(
                'a', href=True, class_='group')

            # funkcija ima v seznamu naenkrat le 20 povezav
            for link in seznam_vseh_linkov_do_receptov:
                seznam_linkov.append("https://okusno.je"+link.get('href'))
            # zanka gre po vseh povezavah jih odpre in pobere podatke in jih zapiše v csv, če pa v nekaterih primerih ne ustreza nekaterim pogojem, to zapiše
            for link in seznam_linkov:

                števec_receptov += 1 #samo informativno o delovanju programa
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
                elif ime_recept == "to ni recept":
                    števec_ni_recept += 1
                    print(števec_ni_recept)
                else:
                    writer.writerow([ime_recept, st_sestavin, število_besed_v_receptu, st_odstavkov,
                                    težavnost, priprava_čas, kuhanje_čas, čas_skupni, vrsta_receptov, energijska_vrednos])

    print(števec_ni_recept)
############################################################


if __name__ == "__main__":
    main()

"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie
author: Daniel Filip
email: danielfilip102@gmail.com
discord: Danko#3595
"""
#-----------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------#
# potřebné importy

import requests
import sys
import bs4
#from bs4 import BeautifulSoup
import csv 

#-----------------------------------------------------------------------------------------------------#
#--------------------------------------------Zdrojový kód---------------------------------------------#
#-----------------------------------------------------------------------------------------------------#

# TODO: Získat HTML stránky(soup, html parser)
#       Získat číslo obce z tabulky
#       Získat název obce z tabulky 
#       Získat odkaz pod číslem obce
#       Získat list kandidujících stran
#       Získat počet registrovaných
#       Získat počet zúčastněných
#       Získat počet platných hlasů
#       Získat kolik hlasů dostala jednotlivá strana 
#       Spojení všech listů s daty do jednoho
#       Finální zápis do SCV
#       Kontrola vstupních argumentů....




def ziskaniHTML(url):
    """
    Funkce "ziskaniHTML" vezme námi zadanou URL adresu a pomocí BS4
    vrátí kompletní zdrojoví kod webové stránky, na kterou směruje URL odkaz
    zadaný uživatelem.

    """
    pozadavek = requests.get(url)
    soup = bs4.BeautifulSoup(pozadavek.text, "html.parser")

    return soup
    
def ziskejCisloObce() -> list:
    """
    Funkce "ziskejCisloObce" hledá v zadané URL adrese veškeré buňky tabulky
    s párovým tagem "td" a zároveň tagem "cislo". Veškeré nalezené hodnoty buňky 
    jsou uloženy do listu "cisloObce".
    
    """
    cisloObce= []
    cisloTag = urlAdr.find_all("td", "cislo")

    for cislo in cisloTag:
        cisloObce.append(cislo.text)

    return cisloObce

def ziskejNazevObce() -> list:
    """
    Funkce "ziskejNazevObce" hledá tagy "td" a "overflow_name" a ukládá
    jejich hodnoty do listu "nazevObce".
    
    """
    nazevObce = []
    overflow_nameTag = urlAdr.find_all("td", "overflow_name")

    for overflow_name in overflow_nameTag:
        nazevObce.append(overflow_name.text)

    return nazevObce

def ziskejOdkazVoleb() -> list:
    """
    Funkce "ziskejOdkazVolem" nalezne všechny odkazy pro získání "pod stránky"  
    voleb jednotlivých obcí pomocí tagů "href". Tyto odkazy se dále uloží do 
    listu "odkazy"
    
    """
    odkazy = []
    hrefTag = urlAdr.find_all("td", "cislo", "href")

    for href in hrefTag:
        href = href.a["href"]
        odkazy.append(f"https://volby.cz/pls/ps2017nss/{href}")

    return odkazy

def kandidujiciStrany() -> list:
    """
    Funkce "kandidujiciStrany" ukládá názvy všech politických stran, které kandidují 
    v jednotlivých městech/obcí.

    """
    nazevStran = []
    obec = ziskejOdkazVoleb()
    pozadavek = requests.get(obec[0])
    soup = bs4.BeautifulSoup(pozadavek.text, "html.parser")
    overflow_nameTag = soup.find_all("td", "overflow_name")

    for overflow_name in overflow_nameTag:
        nazevStran.append(overflow_name.text)

    return nazevStran

def registrovaniVolici() -> list:
    """
    Funkce "registrovaniVolici" ukládá počet registrovaných voličů v jednotlivé obci.
    Vyhledávání pomocí tagů "td" a "sa2".

    """
    odkazy = ziskejOdkazVoleb()
    listRegistrovanychVolicu = []

    for odkaz in odkazy:
        pozadavek = requests.get(odkaz)
        soup = bs4.BeautifulSoup(pozadavek.text, "html.parser")
        tdTag = soup.find_all("td", headers="sa2")

        for td in tdTag:
            td = td.text
            listRegistrovanychVolicu.append(td.replace('\xa0', ' '))

    return  listRegistrovanychVolicu 

def zucastneniVolici() -> list:
    """
    Funkce "zucastneniVolici" získává celkový počet voličů v jednotlivých
    obcích.

    """
    odkazy = ziskejOdkazVoleb()
    voliciZucastneni = []

    for odkaz in odkazy:
        pozadavek = requests.get(odkaz)
        soup = bs4.BeautifulSoup(pozadavek.text, "html.parser")    
        tdTag = soup.find_all("td", headers="sa3")

        for td in tdTag:
            td = td.text
            voliciZucastneni.append(td.replace('\xa0', ' '))

    return voliciZucastneni
    
def platneHlasy() -> list:
    """
    Funkce "platneHlasy" ukládá veškeré platné hlasy jednotlivých obcí do listu
    "platne".

    """
    odkazy = ziskejOdkazVoleb()
    platne = []

    for odkaz in odkazy:
        pozadavek = requests.get(odkaz)
        soup= bs4.BeautifulSoup(pozadavek.text, "html.parser")     
        tdTag = soup.find_all("td", headers="sa6")

        for td in tdTag:
            td = td.text
            platne.append(td.replace('\xa0', ' '))

    return platne    

def hlasyJednotlivychStran() -> list:
    """
    Funkce "hlasyJednotlivychStran" ukládá do listu, kolik jednotlivá politická
    strana získala jednotlivých hlasů.

    """
    odkazy = ziskejOdkazVoleb()
    hlasy = []

    for odkaz in odkazy:
        list = []
        obec = ziskaniHTML(odkaz)
        tdTag = obec.find_all("td", "cislo", headers=["t1sb3", "t2sb3"])

        for td in tdTag:
            list.append(td.text)

        hlasy.append(list)

    return hlasy

def zipuj() -> list:
    """
    Funkce "zipuj" slouží ke spojení listů pomocí metody zip. Metoda vytvoří finální 
    output pro vytvoření CSV souboru.
    
    """
    zipList = []
    list = []

    cisloObce =ziskejCisloObce()
    nazevObce = ziskejNazevObce()
    pocetRegistrovanych = registrovaniVolici()
    pocetZucastnenych = zucastneniVolici()
    hlasyPlatne = platneHlasy()
    pocetHlasu = hlasyJednotlivychStran()
    zipList2 = zip(cisloObce, nazevObce, pocetRegistrovanych, pocetZucastnenych, hlasyPlatne )
    

    for cislo, nazev, registrovani, zucastnenych,  platne in zipList2:
        list.append([cislo, nazev, registrovani, zucastnenych,  platne])

    zipList2 = zip(list, pocetHlasu)

    for list, pocet in zipList2:
        zipList.append(list + pocet)

    return zipList

def dataWriter(url, soubor) -> None:
    """
    Funkce "dataWriter" slouží k vepsání scrapovaných dat do CSV souboru
    s požadovaným názvem, zadaným uživatelem.
    
    """
    try:
        nazevSloupcu = ['Kód příslušné obce', 'Název obce', 'Počet voličů v seznamu', 'Počet vydaných obálek', 'Validní hlasy']
        ziskanaData = zipuj()
        politickeStrany = kandidujiciStrany()

        for strana in politickeStrany:
            nazevSloupcu.append(strana)

        with open(soubor, 'w', encoding='UTF-8', newline='') as writer:
            fileWriter = csv.writer(writer)
            fileWriter.writerow(nazevSloupcu)
            fileWriter.writerows(ziskanaData)

        

    except IndexError:
        print("Error")
        quit()

if __name__ == '__main__' and len(sys.argv) == 3:
    urlAdr = ziskaniHTML(sys.argv[1]) 
    argument1 = sys.argv[1] #URL adresa
    argument2 = sys.argv[2] # Název CSV souboru
    dataWriter(argument1, argument2)
else:
    print('Nesprávné vstupní argumenty')
    quit()    
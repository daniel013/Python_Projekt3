# Python_Projekt3
Engeto Python projekt #3

Úkolem tohoto projektu bylo scrapovat data voleb ze stránky https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ, kde si uživatel vybere libovolný okres, ze kterého chce scrapovat zadaná data.
Uživatel při startu programu musí zadat 2 argumenty. První argument je URL odkaz libovolného okresku a druhý argument, název CSV souboru. Program prochází kontrolu, zda první argument, tj. odkaz, zda se nachází na předem zadané stránce a zda bylo zadán název CSV souboru. Pokud je vše v pořádku, program proběhne a ve složce, kde se nachází program, najdeme CSV soubor s názvem, který jsme zadali.

Spuštění programu:
- instalace všech potřebných pluginů
-> Uživatel musí zadat do terminálu příkaz: pip install -r requirements.txt

- otevření CMD (Příkazový řádek)
-> python projekt3_V2.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107" "Boleslav.csv"
  - odkaz a název souboru si uivatel zadá libovolně

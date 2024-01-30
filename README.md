Project 3


Engeto Academy třetí projekt

Elections Scraper

Projekt slouží k extrahování výsledku voleb z roku 2017 (např. do csv.). Odkaz


Instalace knihoven


pip3 install -r requirements.txt

Spuštění


python scraping.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "data.csv"

Ukázka


1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
2. argument: data.csv
 
   python scraping.py "1.argument" "2.argument"
   python scraping.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "data.csv"

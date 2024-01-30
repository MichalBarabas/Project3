"""

projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Michal Barabáš

email: Michal.barabas51@gmail.com   

discord: 

"""

import csv
import sys
import requests
from bs4 import BeautifulSoup


#Hlavní
def main(url, file_name):
    print("Stahuji data z", url)
    data_to_csv(url, file_name, server_responce(url))
    print("Ulozeno do", file_name)
    
#Odpoved serveru na stranku
def server_responce(url):
    url_res = requests.get(url)
    soup = BeautifulSoup(url_res.text, 'html.parser')
    return soup

#Výpis stran do listu 
def hlavicka(url, soup) -> list:
    hlavicka_list = []
    url_res = requests.get(inner_url(url, soup)[0])
    soup = BeautifulSoup(url_res.text, 'html.parser')

    for i in soup.findAll("td", class_="overflow_name"):
        hlavicka_list.append(i.text)
    return hlavicka_list

#List cisel obcí 
def location_num(soup) -> list:
    list_of_nums = []
    for i in soup.findAll("td", class_="cislo"):
        num = i.text
        list_of_nums.append(num)
    return list_of_nums

#List názvu obcí
def location(soup) -> list:
    list_of_names = []
    for value in soup.findAll("td", class_="overflow_name"):
        name = value.text
        list_of_names.append(name)
    return list_of_names

#List URL pro dalsí data
def inner_url(url, soup) -> list:
    list_of_inner_urls = []
    
    for value in soup.findAll("td", class_="cislo"):
        url_fetch = value.a["href"]
        stripped_url = url.split("/")
        stripped_url.pop()
        stripped_url.append(url_fetch)
        new_url = "/".join(stripped_url)
        list_of_inner_urls.append(new_url)
    return list_of_inner_urls

def voters_and_envelopes(url, soup):
    list_voters = []
    list_envelopes = []

    for i in inner_url(url, soup):
        url_res_inner = requests.get(i)
        soup = BeautifulSoup(url_res_inner.text, 'html.parser')
        value = soup.findAll("td", class_="cislo")
        list_voters.append(value[3].text)
        list_envelopes.append(value[4].text)
    return list_voters, list_envelopes

def valid_votes(url, soup):
    l = 0
    valid_vote_list = []
    vote_summary = []

    for i in inner_url(url, soup):
        url_res_inner = requests.get(i)
        soup = BeautifulSoup(url_res_inner.text, 'html.parser')
        value1 = soup.findAll("td", {"class": "cislo", "headers": "t1sa2 t1sb3"})
        value2 = soup.findAll("td", {"class": "cislo", "headers": "t2sa2 t2sb3"})
        valid_vote_list.append([])
        for value in (value1 + value2):
            valid_vote_list[l].append(value.text)
        l += 1

    for i in range(len(valid_vote_list[0])):
        row =[]
        for item in valid_vote_list:
            row.append(item[i])
        vote_summary.append(row)
    return vote_summary

#Ulozeni dat do CSV souboru
def data_to_csv(url, file_name, soup):
    header_list = ["Číslo obce", "Název obce", "Voliči v seznamu", "Vydané obálky"]
    data = [location_num(soup), location(soup), voters_and_envelopes(url, soup)[0], voters_and_envelopes(url, soup)[1]]

    for value in hlavicka(url, soup):
        header_list.append(value)

    for value in valid_votes(url, soup):
        data.append(value)

    data2 = zip(*data)

    with open(file_name, "w", newline="", encoding="UTF-8") as f:
        writer = csv.writer(f)
        writer.writerow(header_list)
        for row in data2:
            writer.writerow(row)



if __name__ == "__main__":
    try:
        main(url=sys.argv[1], file_name=sys.argv[2])
    except IndexError:
        print("""Byli zadáné spatné argumenty, pro správné spustení vlozte argumenty v poradí: <URL> <název CSV souboru s príponou CSV>""")
        
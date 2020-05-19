import requests
from bs4 import BeautifulSoup
import csv

titles = ['name', 'description', 'height', 'weight', 'gender', 'category', 'abilities', 'type', 'weakness']
with open('pokedex.csv', 'w') as f:
    csv_writer = csv.writer(f, delimiter=',')
    csv_writer.writerow(titles)
    base ='https://www.pokemon.com' 
    url = 'https://www.pokemon.com/us/pokedex/bulbasaur'
    while True:
        rows = []
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find('div', 'pokedex-pokemon-pagination-title')
        rows.append(divs.div.text.split()[0])
        num = divs.div.text.split()[1]

        description = soup.find('p', 'version-x')
        rows.append(description.text.strip())
        
        attributes = soup.find('div', 'pokemon-ability-info')
        attributes = attributes.find_all('span', 'attribute-title')
        for el in attributes:
            rows.append(el.parent.find('span', 'attribute-value').string)
        
        types_el = soup.find('div', 'dtm-type')
        rows.append(','.join([temp.text for temp in types_el.find_all('a')]))
        
        weaknesses_el = soup.find('div', 'dtm-weaknesses')
        rows.append(','.join([temp.text.strip() for temp in weaknesses_el.find_all('a')]))
        
        csv_writer.writerow(rows)
        next_url = soup.find('a', 'next')
        url = base + next_url['href']
        
        if url == 'https://www.pokemon.com/us/pokedex/bulbasaur':
            break
        print(f'{num}-->{rows[0]}')
        
from bs4 import BeautifulSoup
import requests
from collections import Counter
import re

url = input('Inserisci url da analizzare: ')
response = requests.get(url)

# Verifica che la richiesta HTTP sia andata a buon fine
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Ottieni il titolo della pagina
    title = soup.title.string
    print('Titolo della Pagina:')
    print(title)
    print('-' * 80)
    
    
    # Check for 'description' meta tag
    description_tag = soup.find('meta', {'name': 'description'})
    description = description_tag['content'] if description_tag else None

    # If 'description' meta tag is not found, check for 'og:description' meta tag
    if not description:
        og_description_tag = soup.find('meta', {'property': 'og:description'})
        description = og_description_tag['content'] if og_description_tag else None

    # If 'og:description' meta tag is not found, check for 'twitter:description' meta tag
    if not description:
        twitter_description_tag = soup.find('meta', {'name': 'twitter:description'})
        description = twitter_description_tag['content'] if twitter_description_tag else None

    # If no description is found, set to 'No description available'
    description = description if description else "Nessuna descrizione disponibile"

    print('Descrizione:')
    print(description)
    print('-' * 80)
    
    # Intestazioni
    print("Elenco di tutte le intestazioni h1, h2, h3:")
    for heading in soup.find_all(["h1", "h2", "h3"]):
        print(heading.name + ' ' + heading.text.strip())
    print('-' * 80)
    
    # Titolo SEO
    og_title = soup.find("meta", property="og:title")
    if og_title:
        print("Titolo SEO (OG TITLE):")
        print(og_title["content"])
        print('-' * 80)
    
    # Descrizione SEO
    og_description = soup.find("meta", property="og:description")
    if og_description:
        print("Descrizione SEO (OG DESCRIPTION):")
        print(og_description["content"])
        print('-' * 80)
    
    # Schema tags
    schema_tags = soup.find_all("script", type="application/ld+json")
    if schema_tags:
        print("Schema Tags:")
        for tag in schema_tags:
            print(tag.string)
        print('-' * 80)
    
    # Robots tag
    robots_tag = soup.find("meta", attrs={"name": "robots"})
    if robots_tag:
        print("Robots Tag:")
        print(robots_tag["content"])
        print('-' * 80)
    
    # Estrai il contenuto testuale dalla pagina
    text_content = soup.get_text().lower()

    # Tokenizza il testo in parole
    words = re.findall(r'\w+', text_content)

    # Filtra le parole includendo solo quelle con almeno 4 caratteri
    words = [word for word in words if len(word) >= 4]

    # Conta la frequenza delle parole
    word_count = Counter(words)

    exclude_words = ['della', 'delle', 'degli', 'dello', 'dell', 'questo', 'avere','come', 'piã¹']

    # Filtra le parole più comuni per rimuovere quelle escluse
    common_words = [(word, count) for word, count in word_count.most_common() if word.lower() not in exclude_words]
    
    # Mostra le parole più comuni
    words_10 = []
    print('Parole più comuni (4 o più caratteri, escluse le parole specificate):')
    for word, count in common_words[:15]:
        print(f'{word}: {count}')
        print('-' * 80)
        words_10.append(word)
    print(', '.join(words_10))
    print('-' * 80)

else:
    print('Impossibile recuperare la pagina. Codice di stato HTTP:', response.status_code)

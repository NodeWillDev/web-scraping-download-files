import requests
import re
from bs4 import BeautifulSoup

soup = BeautifulSoup(
    requests.get('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos').content, 
    'html.parser'
)

keyword = input("🔎 Enter the word to search in the links: ").strip()

if keyword:    
    links = [element for element in soup.find_all('a') if element.string and re.compile(rf'\b\w*{re.escape(keyword)}\w*\b', re.IGNORECASE).search(element.string)]
    
    if links:
        print("\n🔗 Links found:")
        for link in links:
            print(f"- {link.get_text(strip=True)} → {link.get('href')}")
        index = int(input(f"🔗 You can download it by the corresponding index (0 a {len(links) - 1}): "))
        print(links[index].get('href'))
    else:
        print("\n❌ No links found for that keyword.")
else:
    print("⚠️ Keyword cannot be empty!")

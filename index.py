import requests
import re
from bs4 import BeautifulSoup
import time
import zipfile
import os

def main(url: str):

    more = True
    files = []
    data = requests.get(url).content
    while more:

        name = input(f"📶 {url}\n🔎 Enter the word to search in the links: ") or 'name'
        links = [element for element in BeautifulSoup(data, "html.parser").find_all("a") if element.string and re.compile(rf"\b\w*{re.escape(name)}\w*\b", re.IGNORECASE).search(element.string)]        
        if not links:
            exit("\n❌ No links found for that keyword.")

        print("\n🔗 Links found:")

        for i, link in enumerate(links):
            print(f"[{i}] {link.get_text(strip=True)} → {link.get('href')}")

        try:    

            url = links[int(input(f"\n🔗 Choose an index to download (0 - {len(links) - 1}): "))].get("href")            
            name = f"{name}.{round(time.time(), 2)}.{url.split(".")[-1]}"

            with open(f"scraping/{name}", "wb") as file:
                file.write(requests.get(url).content)
            print(f"\n✅ Download completed: /scraping/{name}")
            files.append(name)
        except (ValueError, IndexError):
            print("\n⚠️ Invalid index selection!")
        
        more = input("🔄 Do you want to continue? (1 - Yes / 2 - No) ") == "1"
    compact = (input("📦 Do you want to compress everything into a .zip file? (1 1 Yes / 2 - No)") == '1') if files else False

    if(compact):
        with zipfile.ZipFile(f"compact-{time.time():.2f}.zip", "a") as compact:
            for file in files:                                
                    compact.write(os.path.join('scraping', file))

if __name__ == '__main__':
    main(input('🌐 Enter the URL for scraping: '))
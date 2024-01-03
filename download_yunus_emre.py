import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

list_of_poems = set()

for idx in range(1,7):
    r = requests.get(("https://www.antoloji.com/"
                      "yunus-emre/siirleri/ara-/"
                      f"sirala-/sayfa-{idx}/"))
    r.raise_for_status()

    soup = bs(r.text,"html.parser")

    divs = soup.find_all("div",{"class":"poemListBox"})[0]

    for link in divs.find_all("a"):
        href = link["href"].split("?")[0]

        list_of_poems.add(
            "https://www.antoloji.com" + href
        )

poem_lines = []

for poem_href in tqdm(list_of_poems):

    r = requests.get(poem_href)
    
    if r.status_code != 200:
        print(f"Skipping {poem_href}")
        continue

    soup = bs(r.text,"html.parser")

    div = soup.find_all("div",{"class":"pd-text"})[0]
    poem_lines.extend([p.text for p in div.find_all("p")])
    

open("yunus_emre.txt","w").write("\n".join(poem_lines))
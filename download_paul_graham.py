import requests
from bs4 import BeautifulSoup as bs

if __name__ == "__main__":

    r = requests.get("https://www.paulgraham.com/articles.html")
    r.raise_for_status()

    #parse the list of essays

    soup = bs(r.text,features="html.parser")

    l = list(soup.find_all("table"))[2]

    for link in l.find_all("a"):
        r = requests.get(f"https://www.paulgraham.com/{link['href']}")
        
        if r.status_code == 200:

            ns = bs(r.text, features="html.parser")
            ll = ns.find_all("table")[0].find_all("font")[0]
            open(f"paul_graham/{link['href'].split('.')[0]}.txt","w")\
                .write(ll.text)



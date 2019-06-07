from lxml import html
import requests
import pandas as pd
import unidecode

page = requests.get('http://www.festiwaldobregopiwa.pl/lista-piw-2019/')
tree = html.fromstring(page.content)

beer_title = tree.xpath('//h3[@class="beer-title"]/text()')
beer_maker = tree.xpath('//p[@class="beer-maker"]/text()')
beer_style = tree.xpath('//p[@class="beer-style"]/strong/text()')


rating = []
i = 1
for beer in beer_title:
    if " - PREMIERA!" in beer:
        beer.replace(" - PREMIERA!", "")
    word = unidecode.unidecode(beer).replace(' ', '_').lower()
    try:
        search = requests.get("https://www.polskikraft.pl/szukaj/" + word)
        tree = html.fromstring(search.content)
        links = tree.xpath('//a/@href')
        true_link = ''
        for link in links:
            if word in link:
                true_link = link
        search = requests.get(true_link)
        tree = html.fromstring(search.content)
        rating.append(tree.xpath('//span[@itemprop="ratingValue"]/text()')[0])
    except:
        rating.append("Brak")
    print(i)
    i += 1

df = pd.DataFrame.from_dict({'Maker': beer_maker, 'Title': beer_title, 'Style': beer_style, 'Rating': rating})
df = df.applymap(str)
df.to_excel('wfdp.xlsx', header=True, index=False)
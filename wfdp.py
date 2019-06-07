from lxml import html
import requests

page = requests.get('http://www.festiwaldobregopiwa.pl/lista-piw-2019/')
tree = html.fromstring(page.content)

beer_title = tree.xpath('//h3[@class="beer-title"]/text()')
beer_maker = tree.xpath('//p[@class="beer-maker"]/text()')
beer_style = tree.xpath('//p[@class="beer-style"]/strong/text()')
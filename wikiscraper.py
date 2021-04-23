import requests
from bs4 import BeautifulSoup
import random

f = open("output.txt", "w+")

response = requests.get(
	url="https://en.wikipedia.org/wiki/Harry_Potter",
)
soup = BeautifulSoup(response.content, 'html.parser')

title = soup.find(id="firstHeading")
print(title.string)
f.write(title.string)
f.close()

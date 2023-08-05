# import required modules
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import re

# get URL
page = requests.get("https://en.wikipedia.org/wiki/Main_Page")
#page = requests.get("https://en.wikipedia.org/wiki/Trees")

# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')

list(soup.children)

# find all occurrence of p in HTML
# includes HTML tags
text_with_headers = soup.find_all('h2')
text = soup.find_all('p')
print(text)

print("Printing extracted text from page:")

text_under_header = {}
links_under_header = {}
for header in soup.find_all('h2'):
    nextNode = header
    while True:
        headerTitle = header.getText()
        nextNode = nextNode.nextSibling
        sub_soup = BeautifulSoup(str(nextNode), 'html.parser')
        for found_text in sub_soup.find_all('p'):
            text_under_header.setdefault(headerTitle, found_text.getText())
            links_under_header.setdefault(headerTitle, [])
            for link in found_text.find_all('a', attrs={'href': re.compile("/")}):
                # input urls into list
                links_under_header[headerTitle].append((link.get('title'), link.get('href')))

        if nextNode is None:
            break
        if isinstance(nextNode, Tag):
            if nextNode.name == "h2":
                break
print(text[0].get_text())

print("Printing Links:")
links = BeautifulSoup(''.join([str(x) for x in text]), 'html.parser')
link_title_pair = []
for link in links.find_all('a', attrs={'href': re.compile("/")}):
    # input urls into list
    link_title_pair.append((link.get('href'), link.get('title')))

print(len(link_title_pair))
user_input = input("Enter 1 to see all links : \n> ")
if user_input == '1' or user_input == 1:
    for i in link_title_pair:
        print(i)
else:
    print("closing program")




print("DONE ___________________")

# example I am using __Aidan__ dunder method?
# for header in soup.find_all('h2'):
#     nextNode = header
#     while True:
#         nextNode = nextNode.nextSibling
#         if nextNode is None:
#             break
#         if isinstance(nextNode, NavigableString):
#             text_under_header += nextNode.strip()
#         if isinstance(nextNode, Tag):
#             if nextNode.name == "h2":
#                 break
#             text_under_header = (nextNode.get_text(strip=True).strip())

# import required modules
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import re


class WikiScraper:
    _page = requests.get("https://en.wikipedia.org/wiki/list_of_tall_trees")
    _soup = BeautifulSoup(_page.content, 'html.parser')
    _dict_with_text_links = {}
    _vision = 1
    _always_commands = ['-h', '--help', '-v', '--v', '-d', '--done', "searching"]
    _number_commands = []
    # _page = requests.get("https://en.wikipedia.org/wiki/Main_Page")
    # _page = requests.get("https://en.wikipedia.org/wiki/trees")

    def __init(self):
        self._dict_with_text_links = {}

    def __int__(self, page):
        self._page = page

    def set_vision(self, vision):
        self._vision = vision

    def search(self, user_search: str) -> None:
        user_url = "_".join(user_search.split(" ")).strip()
        url = "https://en.wikipedia.org/wiki/" + user_url
        self._page = requests.get(url)
        self._soup = BeautifulSoup(self._page.content, 'html.parser')
        list(self._soup.children)

    def _quick_search_link(self, link_number: int) -> str:
        num = 1
        for key in self._dict_with_text_links:
            for links in self._dict_with_text_links[key][1]:
                if num == link_number:
                    return links[1]
                num += 1

    def _quick_search(self, user_search: str) -> None:
        user_url = "https://en.wikipedia.org/" + user_search
        self._page = requests.get(user_url)
        self._soup = BeautifulSoup(self._page.content, 'html.parser')
        list(self._soup.children)

    def scrape_web_page(self) -> None:
        self._dict_with_text_links = {}
        title = self._soup.find_all('h1')[0].get_text()
        all_text = self._soup.find_all('p')

        print("Extracting Page Contents... \n")
        text_under_header = []
        links_under_header = []

        header_elements = ['h3', 'h4', 'h5', 'h6']
        if self._vision > 0:
            for header in self._soup.find_all('h2'):
                nextNode = header
                headerTitle = header.getText()
                curr_text = ''
                while headerTitle not in ['Wikipedia languages', 'Wikipedia\'s sister projects',
                                          'Other areas of Wikipedia']:
                    nextNode = nextNode.nextSibling
                    sub_soup = BeautifulSoup(str(nextNode), 'html.parser')
                    if isinstance(nextNode, Tag) and nextNode in header_elements:
                        if curr_text is not None and curr_text.size() > 0:
                            text_under_header.append(curr_text)
                            curr_text = ''
                        text_under_header.append(nextNode.getText())
                    for found_text in sub_soup.find_all('p'):
                        all_text.remove(found_text)
                        curr_text += (' ' + found_text.getText())
                        curr_text = re.sub(' ', ' ', curr_text)
                        curr_text = re.sub(r'\n', '', curr_text)
                        for link in found_text.find_all('a', attrs={'href': re.compile("/")}):
                            # input urls into list
                            links_under_header.append((link.get('title'), link.get('href')))
                    if self._vision == 2:
                        for found_text in sub_soup.find_all('li'):
                            if found_text.getText() not in ['Archive', 'By email', 'More featured articles', 'About',
                                                            'Nominate an article', 'Start a new article',
                                                            'List of days of the year', 'More featured pictures']:
                                curr_text += ('\n\t' + found_text.getText())
                                curr_text = re.sub(' ', ' ', curr_text)
                    if nextNode is None or (isinstance(nextNode, Tag) and nextNode.name == "h2"):
                        text_under_header.append(curr_text)
                        self._dict_with_text_links.update({headerTitle: (text_under_header, links_under_header)})
                        curr_text = ''
                        text_under_header = []
                        links_under_header = []
                        break

        links = []
        final_soup = BeautifulSoup(" ".join([str(x) for x in all_text]), 'html.parser')
        for link in final_soup.find_all('a', attrs={'href': re.compile("/")}):
            links.append((link.get('title'), link.get('href')))
        self._dict_with_text_links = {k: v for k, v in [
            (title, ([re.sub(' ', ' ', " ".join([str(x.getText()) for x in all_text]))], links))] + list(
            self._dict_with_text_links.items())}

        print("Information on your article")

    def num_links_on_page(self) -> int:
        num_links = 0
        for key in self._dict_with_text_links:
            num_links += len(self._dict_with_text_links[key][1])
        return num_links

    def print_help(self):
        help_box = """+---------------------------------------------+
| Wiki Help:                                  |
| -h | --help   = To show commands            |
| -v | --vision = [0|1|2] changes amount shown|
| "[text]"      = To search something new     |
| -d | --done   = Exit to homepage            |
|                                             |
|                                             |
+---------------------------------------------+"""
        print(help_box)

    def print_wiki_page(self, line_length: int = 150) -> None:
        temp = None
        curr_line_length = None
        for key in self._dict_with_text_links:
            if iter:
                print(key + ": ")
                temp = []
                curr_line_length = 0
            for pos in self._dict_with_text_links[key][0]:
                sentence = pos.split(" ")
                for word in sentence:
                    temp.append(word)
                    curr_line_length += len(word)
                    if curr_line_length > line_length:
                        print(" ".join(temp))
                        temp = []
                        curr_line_length = 0
            if temp is not None and len(temp) != 0:
                print(" ".join(temp))

            num_links = self.num_links_on_page()
        print("""+----------------------------+
| {first} links found{second}|
| Enter 0 for list of link   |
+----------------------------+""".format(first=num_links, second=" " * (15 - len(str(num_links)))))
        self._number_commands.append(0)
        self._number_commands.append(num_links)

    def print_links_on_page(self) -> None:
        num = 1
        print("Printing Links>>>")
        for key in self._dict_with_text_links:
            for links in self._dict_with_text_links[key][1]:
                print(str(num) + " : " + links[0] + " | " + links[1])
                num += 1
        print("Enter a number to quick search from above list: ")

    def handle_input(self, user_input: str) -> None:
        tokens = user_input.split(" ")
        if user_input is None or len(tokens) < 0:
            print("Please input something :)")
        elif tokens[0] in self._always_commands or (tokens[0][0] == '\"' and tokens[len(tokens) - 1][len(tokens[len(tokens) - 1]) - 1] == '\"'):
            if user_input in ['-h', '--help']:
                self.print_help()
            elif tokens[0] in ['-v', '--vision']:
                self.set_vision(int(tokens[1]))
            elif tokens[0] in ['-d', '--done']:
                return
            else:
                search_str = re.sub('["]', "", user_input)
                self.search(search_str)
                self.scrape_web_page()
                self.print_wiki_page(150)
        elif tokens[0] in [str(x) for x in range(self._number_commands[0], self._number_commands[1])]:
            if tokens[0] == '0':
                self.print_links_on_page()
                self._number_commands[0] = 1
            else:
                self._quick_search(self._quick_search_link(int(tokens[0])))
                self.scrape_web_page()
                self.print_wiki_page(150)
        else:
            print("Looks like an error occurred")


p1 = WikiScraper()
print("Welcome to wikipedia enter what you want to do")
user_input = input("> ")
while True:
    p1.handle_input(user_input)
    user_input = input("> ")



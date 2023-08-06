from requests_html import HTMLSession
import random
from goose3 import Goose
from goose3.configuration import Configuration
from urllib.parse import urlparse, parse_qs

def getRandomUSerAgent():
    lines = open('user-agents.txt').read().splitlines()
    return random.choice(lines)


def extract_url(original_url):
    # Parse the original URL
    parsed_url = urlparse(original_url)

    # Parse the query string
    query_params = parse_qs(parsed_url.query)

    # Get the 'url' parameter
    url = query_params.get('url')

    # The 'url' parameter is a list, so get the first item
    if url:
        return url[0]


def google(phrase):
    irrelevant_phrases = ["People also ask", "More results", "From your IP address", "-","·","","About Featured Snippets","All","/"]
    session = HTMLSession()
    searchq = phrase
    searchq.replace(" ",'+')
    searchq = searchq.replace(" ",'+')

    url = f'https://www.google.com/search?q={searchq}'
    headers = {
            'User-Agent': getRandomUSerAgent()
    }

    response = session.get(url,headers=headers)
    response.html.render(sleep=1)
    elements = response.html.xpath('//div/span')
    link_elements = response.html.xpath('//div/a')
    clean = [nums.text for nums in elements if nums.text not in irrelevant_phrases]
    clean = clean[:10]
    linkElementsClean = link_elements[10:21]
    
    return [clean,linkElementsClean]

def linkDisplay(doubleObj):
    results = doubleObj[0]
    links = doubleObj[1]

    print("\n" + "="*50)
    print("Top results from Google!!!")
    print("="*50 + "\n")
    for i, num in enumerate(results, start=1):
        print(f"Result #{i}: {num}\n")
        
    print("\n" + "="*50)
    print("Here are the top links from Google")
    print("="*50 + "\n")
    for i, num in enumerate(links, start=1):
        print(f"Link #{i}: {num.text}\n")
        
def linkPage(linker):
    url = extract_url(linker)
    # create a configuration object
    config = Configuration()

    # set the User-Agent string
    config.browser_user_agent = getRandomUSerAgent()

    # create a Goose object with the configuration
    g = Goose(config)

    # use Goose to extract the article
    article = g.extract(url=url)

    # print the cleaned article text
    print("\n" + "=" * 50)
    print("\033[1m" + "Title: " + "\033[0m" + article.title)
    print("=" * 50 + "\n")

    print("\033[1m" + "Article Text: " + "\033[0m")
    print(article.cleaned_text + "\n")

def handleInput(): 
    user = ''
    while user != 'done':
        print('What do you want to look up on Google or type "done" to quit?')
        user = input('> ')
        if user == 'done':
            break
        googleBox = google(user)
        linkDisplay(googleBox)

        while True:
            try:
                print('Type the number to look at that page?')
                user = input('> ')
                if user == 'done':
                    break
                user = int(user)
                linkPage(googleBox[1][user].attrs.get('href'))
                break  # break out of the loop if input is valid
            except ValueError:
                print("Invalid input, please enter an integer.")
            except IndexError:
                print("Invalid index, please enter a valid number.")
                
if __name__ == "__main__":
    handleInput()
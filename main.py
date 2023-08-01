from requests_html import HTMLSession
import random

def getRandomUSerAgent():
    lines = open('user-agents.txt').read().splitlines()
    return random.choice(lines)

def Reddit():
    # Instantiate the session
    session = HTMLSession()

    # Define the target URL
    url = 'https://www.reddit.com/r/OnePiece/top/?t=day'

    # Define a custom User-Agent string
    headers = {
        'User-Agent': getRandomUSerAgent()
    }

    # Send a GET request
    response = session.get(url, headers=headers)
    response.html.render(sleep=1)
    elements = response.html.find('div[id^="post-title"]')
    # Print the text of the response

    return elements

def Google(phrase):
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
    clean = [nums.text for nums in elements if nums.text not in irrelevant_phrases]
    clean = clean[:10]
    print(response.status_code)

    return clean
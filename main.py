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

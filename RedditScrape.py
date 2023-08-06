from requests_html import HTMLSession
import random
import json
import datetime

def getRandomUSerAgent():
    lines = open('user-agents.txt').read().splitlines()
    return random.choice(lines)

def Reddit(num):
    # Instantiate the session
    session = HTMLSession()
    
    num= num.replace(" ","%20")
    # Define the target URL
    url = f'https://www.reddit.com/search/?q={num}'

    # Define a custom User-Agent string
    headers = {
        'User-Agent': getRandomUSerAgent()
    }

    # Send a GET request
    response = session.get(url, headers=headers)
    response.html.render(sleep=1)

    links = response.html.find('faceplate-tracker')
        
    clean = [json.loads(num.attrs.get('data-faceplate-tracking-context')) for num in links if (num.attrs.get('data-faceplate-tracking-context'))]
    cleaner = [nums for nums in clean if 'post' in nums]
    return cleaner

def linkDisplay(cleaner):
    for i,num in enumerate(cleaner):
        dt = datetime.datetime.fromtimestamp(num['post']['created_timestamp'] / 1000.0, tz=datetime.timezone.utc)
        print(f"#{i} Subreddit: r/{num['post']['subreddit_name']} Title: {num['post']['title']} Date: {dt.date()} Comments: {num['post']['number_comments']}")
            
            
def print_comment(comment, indent=0):
    if isinstance(comment, dict) and comment['kind'] == 't1':
        print('  ' * indent + 'Author: ' + str(comment['data']['author']))
        print('  ' * indent + 'Comment: ' + comment['data']['body'])
        print('-' * 50)  # print a separator line
        if 'replies' in comment['data'] and isinstance(comment['data']['replies'], dict) and 'children' in comment['data']['replies']['data']:
            for reply in comment['data']['replies']['data']['children']:
                print_comment(reply, indent+1)

def print_comments(data):
    for comment in data['data']['children']:
        print_comment(comment)

def Comments(Link):
    # Instantiate the session
    session = HTMLSession()
    
    # Define the target URL
    url = f'https://www.reddit.com{Link}.json'
    # Define a custom User-Agent string
    headers = {
        'User-Agent': getRandomUSerAgent()
    }

    # Send a GET request
    response = session.get(url, headers=headers)
    jresponse = (response.json()[1])
    print(jresponse['data']['children'][0]['data']['body'])
    print_comments(jresponse)
    
    


def handleUSerInputReddit():       
    user = ''
    while user != 'done':
        print('What do you want to look up on Reddit or type "done" to quit?')
        user = input('> ')
        if user == 'done':
            break
        redditBox = Reddit(user)
        linkDisplay(redditBox)

        while True:
            try:
                print('Type the number to go to the comments?')
                user = int(input('> '))
                Comments(redditBox[user]['post']['url'])
                break  # break out of the loop if input is valid
            except ValueError:
                print("Invalid input, please enter an integer.")
            except IndexError:
                print("Invalid index, please enter a valid number.")
                

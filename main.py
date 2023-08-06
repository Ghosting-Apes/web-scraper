import typer
from typing_extensions import Annotated
import RedditScrape
import GoogleScrape
import WikiScrape

app = typer.Typer()
        
@app.command()
def search(phrase: Annotated[str, typer.Argument(help="Input the phrase to be scraped.")], 
           location: Annotated[str, typer.Argument(help="Input source to scrape (e.g. Wikipedia)")] = "Google"):
    if location.lower() == "wiki" or location.lower() == "wikipedia":
        wiki = WikiScrape.WikiScraper()
        wiki.handle_input('\"'+phrase+'\"')
    elif location.lower() == "google":
        gbox = GoogleScrape.google(phrase)
        GoogleScrape.linkDisplay(gbox)
    elif location.lower() == "reddit":
        rbox = RedditScrape.reddit(phrase)
        RedditScrape.linkDisplay(rbox)
    else:
        print("Not a search engine option. ::") 

@app.command()
def run():
    print("Enter search engine. :: ")
    engine = input(">> ")
    
    if engine.lower() == "reddit":
        RedditScrape.handleInput()
        exit()
    elif engine.lower() == "google":
        GoogleScrape.handleInput()
        exit()
    elif engine.lower() == "wiki" or engine.lower() == "wikipedia":
        WikiScrape.handleInput()
        exit()

@app.callback()
def main():
    pass
        
if __name__ == "__main__":
    app()


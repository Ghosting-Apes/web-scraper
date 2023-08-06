import typer
from typing_extensions import Annotated
import RedditScrape
import GoogleScrape

state = {"hasCommand": False}
app = typer.Typer()
        
@app.command()
def search(phrase: Annotated[str, typer.Argument(help="Input the phrase to be scraped.")], 
           location: Annotated[str, typer.Argument(help="Input source to scrape (e.g. Wikipedia)")] = "Google"):
    print(f"Searching for {phrase} within {location}...")
        
        
@app.command()
def run():
    print("Enter search engine. :: ")
    engine = input(">> ")
    
    if engine.lower() == "reddit":
        RedditScrape.handleUserInputReddit()
        exit()
    elif engine.lower() == "google":
        GoogleScrape.handleUserInputGoogle()
        exit()
        
    
    # print("Enter prompt. ::")
    # prompt = input(">> ")
    # while True:
    #     if prompt == "quit":
    #         exit()
        
    #     if prompt == "done":
    #         run()
            
    #     search(prompt, engine)
    #     prompt = input(">> ")
        

@app.callback()
def main():
    pass
        
if __name__ == "__main__":
    app()


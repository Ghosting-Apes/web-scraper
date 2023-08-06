import typer
from typing_extensions import Annotated

state = {"hasCommand": False}
app = typer.Typer()
        
@app.command()
def search(phrase: Annotated[str, typer.Argument(help="Input the phrase to be scraped.")], 
           location: Annotated[str, typer.Argument(help="Input source to scrape (e.g. Wikipedia)")] = "Google"):
    print(f"Searching for {phrase} within {location}...")
        
        
@app.command()
def run():
    typer.Argument(help="Input source to scrape (e.g. Wikipedia)")
    print("Enter search engine. :: ")
    engine = input(">> ")
    
    print("Enter prompt. ::")
    prompt = input(">> ")
    while True:
        if prompt == "quit":
            exit()
        
        if prompt == "done":
            run()
            
        search(prompt, engine)
        prompt = input(">> ")
        

@app.callback()
def main():
    pass
        
if __name__ == "__main__":
    app()


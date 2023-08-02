import typer
from typing_extensions import Annotated

state = {"hasCommand": False}
app = typer.Typer()
        
@app.command()
def search(phrase: Annotated[str, typer.Argument(help="Input the phrase to be scraped.")], 
           location: Annotated[str, typer.Argument(help="Input source to scrape (e.g. Wikipedia)")] = "Google"):
    print(f"Searching for {phrase} within {location}...")
        
        
@app.command()
def run(hasCommand: bool = True):
        print(">> ", end="")
        inp = input()
        inpList = inp.split("\"")[1:]
        inpList[1] = inpList[1].strip()
        print(inpList)
        while hasCommand:
             search(inpList[0], inpList[1])
             print(">> ", end="")
             inp = input()
             if inp == "quit":
                  break
             inpList = inp.split("\"")[1:]
             inpList[1] = inpList[1].strip()

@app.callback()
def main():
    pass
        
if __name__ == "__main__":
    app()


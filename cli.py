import typer
from typing_extensions import Annotated

app = typer.Typer()
        
@app.command()
def search(phrase: Annotated[str, typer.Argument(help="Input the phrase to be scraped.")], location: Annotated[str, typer.Argument(help="Input source to scrape (e.g. Wikipedia)")] = "Google"):
    print(f"Searching for {phrase} within {location}...")
        
@app.callback()
def main():
    pass
        
if __name__ == "__main__":
    app()

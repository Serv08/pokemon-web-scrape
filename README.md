# pokémon-web-scrape
## [Sir Josh challenge](https://www.facebook.com/share/p/shSjfPoG5PaD6bnm/): Scraping data from the [Pokémon Pokédex](https://pokemondb.net/pokedex/all).

This is a Scraping challenge of Pokemon Pokedex by Sir Josh.

## Learning Objectives:
- Learn to use web scraping tools using Python.
- Learn how to work with database using Python and SQLite.
- Learn creation of log files and error-handling code structure for loggings.
- Learn to create visualization from database.

## Notes:
The filepath used in the source code should be `'.\datasets'`. However, Windows protects my directory for GitHub repositories, preventing changes from the path, hence, the filepath used is outside the location of my GitHub Repositories.

## Snapshots:
Saving and reading database with pandas (*from Jupyter Notebook*).
<img src='documentation/read_from_db_with_pd.png'></img>

|Libraries used|PIP command|Description|
|---|---|---|
|bs4|`pip install bs4`| Beautiful Soup is a library that makes it easy to scrape information from web pages|
|requests|`pip install requests`|Allows you to send HTTP requests using Python.|
|pandas| `pip install pandas`| A Python library used for working with data sets.|

## References

### Tutorial Videos:
- [Scraping Data from a Real Website | Web Scraping in Python](https://www.youtube.com/watch?v=8dTpNajxaH0) by *Alex the Analyst*.
- [Upload A CSV File (Or Any Data File) To SQLite Using Python](https://www.youtube.com/watch?v=UZIhVmkrAEs) by *Jie Jenn*.

### Reading Material:
- [SQLite with Python using CSV files.](https://medium.com/@eliud.giroma/sqlite-with-python-using-csv-files-6772bdd3fc5e) by *Eliud Rodríguez*.

### Error handling:
- [Windows not letting executable files create changes.](https://www.reddit.com/r/learnpython/comments/1af0hti/oserror_errno_9_bad_file_descriptor/)

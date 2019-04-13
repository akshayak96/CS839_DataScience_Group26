from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm

movies_whole = pd.DataFrame(
    {'Title': [], 'Year_of_Release': [], 'Rating': [], 'Metascore': [], 'Vote': [], 'Description': []})

# Redeclaring the lists to store data in
names = []  # titles of the movies
years = []  # dates that the movies are released
imdb_ratings = []  # the rating of each movie
metascores = []  #
votes = []  #
descriptions = []  # the description of the movies
requests = 0

pages = [str(i) for i in range(1, 1)]
year_url = '2000'  # [str(i) for i in range(2000,2018)]

# form the pages keys
pages = [str(i) for i in range(1, 356)]
headers = {"Accept-Language": "en-US, en;q=0.5"}
# For every page in the interval 1-356
for page in tqdm(pages):

    # Make a get request
    response = get('http://www.imdb.com/search/title?release_date=' + year_url +
                   '&sort=num_votes,desc&page=' + page, headers=headers)

    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')

    # Select all the 50 movie containers from a single page
    mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

    names = []  # titles of the movies
    years = []  # dates that the movies are released
    imdb_ratings = []  # the rating of each movie
    metascores = []  #
    votes = []  #
    descriptions = []  # the description of the movies
    # For every movie of these 50
    for container in mv_containers:
        # If the movie has a Metascore, then:
        if container.find('div', class_='ratings-metascore') is not None:
            # Scrape the name
            name = container.h3.a.text
            names.append(name)

            # Scrape the year
            year = container.h3.find('span', class_='lister-item-year').text
            years.append(year)

            # Scrape the IMDB rating
            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)

            # Scrape the Metascore
            m_score = container.find('span', class_='metascore').text
            metascores.append(int(m_score))

            # Scrape the number of votes
            vote = container.find('span', attrs={'name': 'nv'})['data-value']
            votes.append(int(vote))

            # Scrape the descriptions
            descp = container.find('div', class_='lister-item-content').findAll('p', class_='text-muted')[
                1].text.lstrip()
            descriptions.append(descp)

    movies_container = pd.DataFrame({'Title': names,
                                     'Year_of_Release': years,
                                     'Rating': imdb_ratings,
                                     'Metascore': metascores,
                                     'Vote': votes,
                                     'Description': descriptions})

    movies_whole = movies_whole.append(movies_container, ignore_index=True)
print(movies_whole)
movies_whole.to_csv('themoviedb.csv', sep=',')
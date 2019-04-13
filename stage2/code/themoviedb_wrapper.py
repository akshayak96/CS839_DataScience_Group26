from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from time import sleep
from random import randint
from tqdm import tqdm

movies_whole = pd.DataFrame({'Title': [], 'Date_of_Release': [], 'Rating': [], 'Description': []})

# Redeclaring the lists to store data in
titles = []  # titles of the movies
dates = []  # dates that the movies are released
ratings = []  # the rating of each movie (% percent)
descriptions = []  # the description of the movies
requests = 0

# form the pages keys
pages = [str(i) for i in range(1, 356)]
headers = {"Accept-Language": "en-US, en;q=0.5"}
# For every page in the interval 1-356
for page in tqdm(pages):

    # Make a get request
    response = get('https://www.themoviedb.org/movie/top-rated?language=en-US&page=' + page, headers=headers)

    # Pause the loop
    sleep(randint(8, 15))

    # Monitor the requests
    requests += 1

    # Parse the content of the request with BeautifulSoup
    html_soup = BeautifulSoup(response.text, 'html.parser')

    # Select all the 50 movie containers from a single page
    mv_containers = html_soup.find_all('div', attrs={"class": 'item poster card'})
    i = 1

    # Redeclaring the lists to store data in
    titles = []  # titles of the movies
    dates = []  # dates that the movies are released
    ratings = []  # the rating of each movie (% percent)
    descriptions = []  # the description of the movies
    print('Page Number:', page)
    # For every movie of these 20
    for container in tqdm(mv_containers):
        # Scrape the title
        title = container.find('div', class_='flex').a.text
        titles.append(title)

        # Scrape the date
        date = container.find('div', class_='flex').span.text
        dates.append(date)

        # Scrape the description
        description = container.find('p', class_='overview').text
        descriptions.append(description)

        # Scrape the rating
        rating = container.find('div', class_='percent').span['class'][1].replace('icon-r', '')
        ratings.append(int(rating))
        i += 1

    movies_container = pd.DataFrame({'Title': titles,
                                     'Date_of_Release': dates,
                                     'Rating': ratings,
                                     'Description': descriptions})

    movies_whole = movies_whole.append(movies_container, ignore_index=True)
print(movies_whole)
movies_whole.to_csv('themoviedb.csv', sep=',')
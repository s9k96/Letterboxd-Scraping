# Have a list of letterboxd lists in config, scroll them and extract data. 
# a function here which takes a movie name/url and download its details.


from helper import *
from config import *

movie_lists_urls = [
    'https://letterboxd.com/jack/list/official-top-250-films-with-the-most-fans'
]


for movie_lists_url in movie_lists_urls:

    total_pages = get_total_pages_to_scrape(movie_lists_url)
    print(f'Found {len(total_pages)} paginated pages')

    movie_urls = []
    for i, page in enumerate(total_pages):
        print(f'Checking page {i+1}')
        soup = get_soup_from_url(page)
        job_elements = soup.find_all("div", class_="film-poster")
        for i, element in tqdm(enumerate(job_elements)):
            movie_name = element.get('data-film-slug')
            movie_link = element.get('data-target-link')
            movie_urls.append(movie_link)


    print(f'Found {len(movie_urls)} movies')

    data = {}
    for i, movie_url in tqdm(enumerate(movie_urls[:])):

        movie_url = f'https://letterboxd.com{movie_url}'
        soup = get_soup_from_url(movie_url)

        header = soup.find_all('section', class_ = 'film-header-lockup')
        
        movie_director = header[0].find('span', class_ = 'prettify').text.strip()
        release_year = header[0].find('small', class_ = 'number').text.strip()
        movie_name = header[0].find('h1', class_ ='headline-1').text.strip()
        genres = soup.find(id ='tab-genres' ).find('div').text.strip()
        
        data[i] = {
            'movie_name': movie_name, 
            'release_year': release_year,
            'director':movie_director, 
            'genres': genres
            
        }
    data = pd.DataFrame.from_dict(data).T
    print(data.shape)
    data.to_csv('data/movies_dump.csv')


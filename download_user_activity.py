
from helper import *

os.makedirs('data', exist_ok=True)
os.makedirs('data/profile_data', exist_ok=True)

sns.set_style('darkgrid')
pd.set_option('display.max_rows', 100)


parser = argparse.ArgumentParser()
parser.add_argument('username')

def get_total_pages_to_scrape(username, base_url):
    pages = []
    
    soup = get_soup_from_url(base_url)
    total_pages = soup.find_all("div", class_="paginate-pages")[0].find_all('li')
    
    for i in range(len(total_pages)):

        suffix = '' if i <1 else f'page/{i+1}'
        url = f"{base_url}/{suffix}"

        pages.append(url)
    return pages


def get_data_from_soup(soup):
    job_elements = soup.find_all("tr", class_="diary-entry-row viewing-poster-container")

    data_dict = {}
    last_present_month_year = ''
    
    for i, element in tqdm(enumerate(job_elements)):
        
        title = element.find_all("h3", class_ = 'headline-3 prettify')
        month_year = element.find_all("div", class_ = 'date')
        date = (element.find_all("td", class_ = 'td-day'))

        title = title[0].text.strip() if len(title)>0 else ''
        month_year = month_year[0].text.strip() if len(month_year)>0 else last_present_month_year
        date = date[0].text.strip() if len(date) >0 else ''

        # print(date, month_year, title)
        last_present_month_year = month_year 
        
        data_dict[i]=  {
            'date':date, 
            'month_year':month_year, 
            'title':title
        }
    return pd.DataFrame.from_dict(data_dict).T


def get_user_data_from_username(username):

    profile_url = f'https://letterboxd.com/{username}/films/diary/'

    total_pages = get_total_pages_to_scrape(username, base_url=profile_url)
    df = pd.DataFrame()

    for page in total_pages:    
        soup = get_soup_from_url(page)
        data = get_data_from_soup(soup)
        df = pd.concat([df, data])

    df['dw_date'] = datetime.today().date()
    
    print(f'Downloaded {df.shape[0]} rows for {username}')
    df.to_csv(f'data/profile_data/{username}.csv')    
    return df


if __name__ == '__main__':

    args = parser.parse_args()
    # print(args)

    username = args.username
    _ = get_user_data_from_username(username)

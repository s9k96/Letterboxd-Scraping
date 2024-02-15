import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from tqdm.auto import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import os 


def get_soup_from_url(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_total_pages_to_scrape( base_url):
    pages = []
    
    soup = get_soup_from_url(base_url)
    total_pages = soup.find_all("div", class_="paginate-pages")[0].find_all('li')
    
    for i in range(len(total_pages)):

        suffix = '' if i <1 else f'page/{i+1}'
        url = f"{base_url}/{suffix}"

        pages.append(url)
    return pages


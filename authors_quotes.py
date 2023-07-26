import requests
from bs4 import BeautifulSoup
import json

def get_author_info(base_url, authors):
    author_info_list = []

    for author in authors:
        author_info = {}
        author_link = base_url + author.find_next('a')['href']
        author_doc = requests.get(author_link)

        if author_doc.status_code == 200:
            author_soup = BeautifulSoup(author_doc.content, 'html.parser')

            authors_fullname = author_soup.find_all('h3', class_='author-title')
            for author_fullname in authors_fullname:
                author_info['fullname'] = author_fullname.text

            born_dates = author_soup.find_all('span', class_='author-born-date')
            for born_date in born_dates:
                author_info['born_date'] = born_date.text

            born_locations = author_soup.find_all('span', class_='author-born-location')
            for born_location in born_locations:
                author_info['born_location'] = born_location.text

            author_descriptions = author_soup.find_all('div', class_='author-description')
            for author_description in author_descriptions:
                author_info['description'] = author_description.text.strip()

        author_info_list.append(author_info)

    return author_info_list

def parse_data():
    result = []
    
    for page in range(1, 11):
        url = f'http://quotes.toscrape.com/page/{page}/'
        html_doc = requests.get(url)

        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')

            
            quotes = soup.find_all('span', class_='text')
            authors = soup.find_all('small', class_='author')
            tags = soup.find_all('div', class_='tags')

            for i in range(len(quotes)):
                quote_dict = {}
                quote_dict['quote'] = quotes[i].text
                quote_dict['author'] = authors[i].text

                tags_list = []
                tagsforquote = tags[i].find_all('a', class_='tag')
                for tagforquote in tagsforquote:
                    tags_list.append(tagforquote.text)
                quote_dict['tags'] = tags_list

                result.append(quote_dict)

    return result


if __name__ == '__main__':
    base_url = 'http://quotes.toscrape.com/'
    total_pages = 10
    authors_list = []

    for page in range(1, total_pages + 1):
        url = f'{base_url}page/{page}/'
        html_doc = requests.get(url)

        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.content, 'html.parser')

            
            authors = soup.find_all('small', class_='author')
            authors_list.extend(get_author_info(base_url, authors))

    with open('authors.json', 'w') as authors_file:
        json.dump(authors_list, authors_file, indent=2)
    quotes_list = parse_data()

    with open('quotes.json', 'w') as quotes_file:
        json.dump(quotes_list, quotes_file, indent=2)
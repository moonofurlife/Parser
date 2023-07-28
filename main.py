import requests
import bs4
from fake_headers import Headers
import json

headers = Headers(os='win', browser='chrome')
vacancy = []
hh_link = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def get_vacancy(url):
    return requests.get(url, headers=headers.generate())


def vacancy_link(url):
    vacancy_html = get_vacancy(url).text
    soup = bs4.BeautifulSoup(vacancy_html, 'lxml')
    links_tag = soup.find_all(class_='serp-item__title')
    for link_tag in links_tag:
        link = link_tag['href']
        find_flask_django(link)


def find_flask_django(vacancy_url):
    vacancy_html = get_vacancy(vacancy_url).text
    soup = bs4.BeautifulSoup(vacancy_html, 'lxml')
    descriptions = soup.find_all(class_='g-user-content')
    for desc in descriptions:
        text = desc.text
        django = text.find('Django')
        flask = text.find('Flask')
        if django != -1 or flask != -1:
            parse_vacancy(vacancy_url)
            break


def parse_vacancy(vacancy_url):
    vacancy_html = get_vacancy(vacancy_url).text
    soup = bs4.BeautifulSoup(vacancy_html, 'lxml')
    link = vacancy_url
    vacancy_title = soup.find(class_='vacancy-title')
    salary = vacancy_title.find('span').text
    company = soup.find(class_='vacancy-company-name').text
    city_tag = soup.find(class_='vacancy-company-redesigned')
    city = city_tag.find('p').text.split()

    res = {
        'link': link,
        'salary': salary,
        'company': company,
        'city': city
    }
    vacancy.append(res)
    print(vacancy)


def save_json():
    with open('vacancy_info.json', 'a') as f:
        f.write(json.dumps(vacancy, ensure_ascii=False))


if __name__ == '__main__':
    vacancy_link(hh_link)
    save_json()

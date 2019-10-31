import requests
from bs4 import BeautifulSoup as bs
import csv

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

baseUrl = 'https://hh.ru/search/vacancy?area=1search_period=3&text=php&page=0'


def hhParse(baseUrl, headers):
    jobs = []
    urls = []
    urls.append(baseUrl)
    session = requests.Session()
    request = session.get(baseUrl, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?area=1search_period=3&text=php&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')

        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                content = responsibility + ' ' + requirement
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'content': content,
                })
            except:
                pass

        print(len(jobs))
    else:
        print('ERROR OR DONE = ' + str(request.status_code))
    return jobs


def filesWriter(jobs):
    with open('parsed_jobs.csv', 'w', encoding='utf-8') as file:
        record = csv.writer(file)
        record.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            record.writerow((job['title'], job['href'], job['company'], job['content']))


jobs = hhParse(baseUrl, headers)
filesWriter(jobs)

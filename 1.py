import requests as req
from bs4 import BeautifulSoup
import json
import tqdm

data ={"data":[]}

for page in range(10):
    url = f'https://spb.hh.ru/search/vacancy?text=python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list'
    us_ag = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
    resp = req.get(url, headers=us_ag)
    soup = BeautifulSoup(resp.text, 'lxml')
    tags = soup.find_all(attrs={"data-qa":"serp-item__title"})

    for item in tqdm.tqdm(tags):

        url_object = item.attrs["href"]
        resp_object = req.get(url_object, headers=us_ag)
        soup_object = BeautifulSoup(resp_object.text, 'lxml')

        def prov(a):
            if a is None:
                return ""
            else:
                return a.text

        tag_price = soup_object.find(attrs={"data-qa":"vacancy-salary-compensation-type-net"})
        if tag_price is None:
            tag_price = soup_object.find(attrs={"data-qa":"vacancy-salary-compensation-type-undefined"})
            if tag_price is None:
                tag_price = soup_object.find(attrs={"data-qa":"vacancy-salary-compensation-type-gross"})
       
        tag_item = item

        tag_region = soup_object.find(attrs={"data-qa":"vacancy-view-location"})
        if tag_region is None:
            tag_region = soup_object.find(attrs={"data-qa":"vacancy-view-raw-address"})

        tag_op = soup_object.find(attrs={"data-qa":"vacancy-experience"})
        if tag_op is None:
            tag_op = soup_object.find(attrs={"data-qa":"vacancy-salary-compensation-type-undefined"})

        data["data"].append({"title":prov(tag_item), "work experience":prov(tag_op), "salary":prov(tag_price), "region":prov(tag_region)})

        with open("1.json", "w", encoding='utf-8') as file:
            json.dump(data, file, indent=3, ensure_ascii=False)
        
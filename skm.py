from bs4 import BeautifulSoup as bs4
import requests
import json
import html
import fake_useragent
from faker import Faker

base_url = 'https://skm.dephub.go.id/'

urls = ["F1LhIfnA",
        "YLaqzrf9",
        "4j6CnrlK",
        "IZKoTlC3"]

for url in urls[:1]:
    s = requests.Session()
    r1 = s.head(base_url + 'ly/' + url)
    rurl = r1.headers['Location']
    
    r2 = s.get(rurl)
    sp_r2 = bs4(r2.text, 'html.parser')
    form = sp_r2.find('form', {'id':'form_input_survey'})
    # print(form)
    
    ids = form.find('div',{'class':'col-lg-12'}).find_all('input')
    d = {id['name']:id['value'] for id in ids}
    d['language_id'] = d.pop('customer_list_id')
    
    r3 = s.get(
        base_url + 'survey/get_questionnaire_form',
        headers = {'X-Requested-With':'XMLHttpRequest'},
        params=d
    )

    sp_r3 = bs4(html.unescape(r3.json()), 'html.parser')
    institution = sp_r3.find('span',{'style':"font-weight: 700;"}).text.strip()
    services = sp_r3.find('select',{'name':'instance_group_service_id'}).find_all('option')[:-1]

    print(institution)
    # print(services)
    rows = sp_r3.find('div', {'id':'page-title-geo'}).find_all('div', class_ = 'statement-response')
    for row in rows:#[2:10]:
        # print(serve.text.strip(), serve['value'])
        print(row)
    print("")
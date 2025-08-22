import requests
import pandas as pd
from bs4 import BeautifulSoup as bs4
import html

headers = {'X-Requested-With': 'XMLHttpRequest'}
cookies={'7daddac39a11a204eb4d726888e93594': 'dcp133ukvjjondthuqtgjh6f6eh4hllc'}
payloads = {
    'is_active': '',
    'pageSize': '75000',
    'pageIndex': '1',
}

r = requests.post('https://skm.dephub.go.id/survey/respondent/get_list_json', 
                         cookies=cookies, 
                         headers=headers,
                         data=payloads)
data = r.json()['data']

print(len(data))

list1 = []
for j, d in enumerate(data):#[:1]:
    id = d['id']
    detail_url = 'https://skm.dephub.go.id/survey/respondent/detail/'
    try:
        r1 = requests.get(detail_url + id,headers=headers, cookies=cookies)
        # print(r1.status_code)
        sp_r1 = bs4(html.unescape(r1.json()), 'html.parser').find('div', {'id':'data_raw_info'})
        rows = sp_r1.find_all('dd', class_='col-sm-12')
        list2 = []
        for i, row in enumerate(rows):
            if i < 3:
                x = row.text.strip().replace('\t','').split('-')[1:][0]
                list2.append(x)

            if i >= 3 and i < 20:
                x = row.text.strip().split('. ')[1:][0]
                list2.append(x)
        
        x = [row.text.strip().split('. ')[1:][0] for row in rows[20:]]
        list2.append(x)
        list1.append(list2)
        print("Succes", j)
    except Exception as e:
        print("Error:", j, e)

df = pd.DataFrame(list1)
df.to_csv('Hasil_Survey.csv', index=False)
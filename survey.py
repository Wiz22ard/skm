import requests
from bs4 import BeautifulSoup as bs4
import html
import time
import csv
import random
from datetime import datetime

headers = {
    "X-Requested-With": "XMLHttpRequest",
}
cookies = {
    "7daddac39a11a204eb4d726888e93594": "fhome3pb3sgtt19foegm28017kij3cm4"
}
payloads = {
    "is_active": "",
    "pageSize": "75000",
    "pageIndex": "1",
}

session = requests.Session()
r = session.post(
    "https://skm.dephub.go.id/survey/respondent/get_list_json",
    cookies=cookies,
    headers=headers,
    data=payloads,
)
data = r.json()["data"]

print(f"Total data: {len(data)}")

with open("hasil_skm.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    for j, d in enumerate(data):
        ts = datetime.now().strftime("%H:%M:%S")
        id = d["id"]
        detail_url = f"https://skm.dephub.go.id/survey/respondent/detail/{id}"

        for attempt in range(3):
            try:
                r1 = session.get(detail_url, cookies=cookies, headers=headers, timeout=15)
                sp_r1 = bs4(html.unescape(r1.json()), "html.parser").find(
                    "div", {"id": "data_raw_info"}
                )
                rows = sp_r1.find_all("dd", class_="col-sm-12")

                list2 = []
                for i, row in enumerate(rows):
                    if i < 3:
                        x = row.text.strip().replace("\t", "").split("-")[1:][0]
                        list2.append(x)
                    elif 3 <= i < 20:
                        x = row.text.strip().split(". ")[1:][0]
                        list2.append(x)

                x = [row.text.strip().split(". ")[1:][0] for row in rows[20:]]
                list2.append(x)

                writer.writerow(list2)
                print("Success", j, ts)
                break  

            except Exception as e:
                print(f"Error {j} attempt {attempt+1, ts}: {e}")
                time.sleep(1)
        time.sleep(random.uniform(0.5, 1.5))

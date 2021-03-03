import os
import requests
from bs4 import BeautifulSoup
from save import save_to_file

os.system("clear")
URL = "http://www.alba.co.kr"


def get_brand_links():
    all_pairs = []
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    brand_container = soup.find("div", {"id": "MainSuperBrand"}).find("ul", {"class": "goodsBox"})
    all_li = brand_container.find_all("li")
    for li in all_li:
        link = li.find("a")["href"]
        title = li.find("a").find("span", {"class": "company"})

        if title:
            title = title.string
        else:
            continue
        all_pairs.append([title, link])

    return all_pairs


def extract_jobs(url):
    jobs = []

    if url.find("/job/brand/"):
        result = requests.get(f"{url}?pagesize = 10000")
    else:
        result = requests.get(f"{url}job/brand/?pagesize = 10000")

    soup = BeautifulSoup(result.text, "html.parser")
    print(f"This time it is {url}")

    results = soup.find("div", {"class", "goodsJob"}).find("tbody").find_all("tr", {"class": ""})

    job_number = 0
    if len(results) <= 1:
        return None
    else:
        for result in results:
            print(url, job_number)
            job = extract_job(result)
            jobs.append(job)
            job_number += 1
        return jobs


def extract_job(result):
    try:
        location = result.find("td", {"class": "local first"}).get_text().replace(u'\xa0', u' ')
    except:
        location = result.find("td", {"class": "local first "}).get_text().replace(u'\xa0', u' ')

    try:
        time = result.find("td", {"class": "data"}).find("span", {"class": "time"}).get_text()
    except:
        time = result.find("td", {"class": "data"}).find("span", {"class": "consult"}).get_text()

    try:
        last_reg = result.find("td", {"class": "regDate last"}).find("strong").get_text()
    except:
        last_reg = result.find("td", {"class": "regDate last"}).get_text()

    title = result.find("td", {"class": "title"}).find("span", {"class": "title"}).get_text(strip=True)
    pay_period, pay = result.find("td", {"class": "pay"}).find_all("span")
    pay = pay_period.string + pay.string

    return {
        "location": location,
        "title": title,
        "time": time,
        "pay": pay,
        "last_reg": last_reg
    }


def main():
    all_pairs = get_brand_links()

    for pair in all_pairs:
        title = pair[0]
        link = pair[1]
        jobs = extract_jobs(link)

        if jobs is None:
            pass
        else:

            if "/" in title:
                title = title.replace("/", " ")

            save_to_file(title, jobs)


main()

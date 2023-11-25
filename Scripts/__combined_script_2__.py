from data import my_data 
from bs4 import BeautifulSoup
import os 
import time
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
}
REQUEST_DELAY = 0 
REFERENCE_HTML = "reference.html"
HREF_TXT = "hrefs.txt"

def make_request(REQUEST_URL, set_headers):
    time.sleep(REQUEST_DELAY)
    headers = HEADERS if set_headers else None
    response = requests.get(url=REQUEST_URL, headers=headers)
    
    if response.status_code == 200: 
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Request to {REQUEST_URL} failed with status code {response.status_code}")
        return None

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

def create_reference_html(dir_name, container):
    create_directory(dir_name)
    PATH_FOR_REF_HTML = os.path.join(dir_name, REFERENCE_HTML)
    with open(PATH_FOR_REF_HTML, "wb") as file:
        file.write(container.prettify().encode("utf-8"))
    print(f"Successfully created reference.html file for {dir_name}")

def write_hrefs_to_file(dir_name, href_list):
    PATH_FOR_HREF_TXT = os.path.join(dir_name, HREF_TXT)
    with open(PATH_FOR_HREF_TXT, "w") as file:
        file.writelines("\n\n".join(href_list))
    print(f"Successfully created hrefs.txt file for {dir_name}")

def scrape_content(name, url, ctn, subCtn, set_headers):
    SOUP = make_request(REQUEST_URL=url, set_headers=set_headers)

    if SOUP:
        main_article_ctn = SOUP.find("div", {"class": ctn})

        if main_article_ctn:
            create_reference_html(name, main_article_ctn)

            anchor_elements = main_article_ctn.find_all("a")
            href_list = [a.get("href") for a in anchor_elements]
            write_hrefs_to_file(name, href_list)

        else:
            print(f"Unable to create reference.html file for {name}, class {ctn}")

def main():
    for entry in my_data:
        name = entry['name']
        url = entry['url']
        ctn = entry['container']
        subCtn = entry['subContainer']
        set_headers = entry['header']

        scrape_content(name, url, ctn, subCtn, set_headers)
                
if __name__ == "__main__":
    os.system('clear')
    main()

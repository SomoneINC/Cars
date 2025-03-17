import requests
from bs4 import BeautifulSoup

url = "https://www.ss.com/lv/transport/cars/"

response = requests.get(url)
if response.status_code == 200: 

    soup = BeautifulSoup(response.content, "html.parser")
    car_table = soup.find('div', attrs={'align': 'right'})
    links = car_table.find_all('a')
    for link in links:
        print(link.get('href'))

else:
    print("Error:", response.status_code)
import requests
import json
from bs4 import BeautifulSoup
import concurrent.futures
import time

link_list = []
url = "https://www.ss.com/lv/transport/cars/"
nosukumu_holder = ["Marka", "Model", "Virsbūve", "Gads", "Cena", "Tekniskā apskate", "Transmition", "Motors", "Krāsa", "Nobraukums", "Links"]
saved_data = []
saved_data.append(nosukumu_holder)
start_time = time.time()



#Link proccesing 
def Process_link(link,Type):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")

        # Getting data
        try:
            Marka = link.split("/")[7].capitalize()
        except IndexError:
            Marka = None

        try:
            Model = soup.find('td', class_='ads_opt', id="tdo_31").get_text().strip()
        except AttributeError:
            Model = None

        try:
            Virsbūve = soup.find("td", class_="ads_opt", id="tdo_32").get_text().strip()
        except AttributeError:
            Virsbūve = None

        try:
            Gads = soup.find("td", class_="ads_opt", id="tdo_18").get_text().strip().split(" ")[0]
        except (AttributeError, IndexError):
            Gads = None

        try:
            Price = soup.find('span', id='tdo_8', class_='ads_price').get_text().strip().replace(" ", "").replace("€", "")
        except AttributeError:
            Price = None

        try:
            Tehn_aps = soup.find("td", class_="ads_opt", id="tdo_223").get_text().strip()
        except AttributeError:
            Tehn_aps = None

        try:
            Transmition = soup.find("td", class_="ads_opt", id="tdo_35").get_text().strip()
        except AttributeError:
            Transmition = None

        try:
            Motors = soup.find("td", class_="ads_opt", id="tdo_15").get_text().strip()
        except AttributeError:
            try:
                Motors = soup.find("td", class_="ads_opt", id="tdo_34").get_text().strip()
            except AttributeError:
                Motors = None

        try:
            Krāsa = soup.find("td", class_="ads_opt", id="tdo_17").get_text().strip().replace("  ", " ")
            Krāsa = ' '.join(Krāsa.split())
        except AttributeError:
            Krāsa = None

        try:
            Nobraukums = soup.find("td", class_="ads_opt", id="tdo_16").get_text().strip().replace(" ", "")
        except (AttributeError, IndexError):
            Nobraukums = None

        try:
            img_holder = soup.find('div', id='tr_foto', class_="ads_photo_label")
            img = img_holder.find_all('img')[0].get('src')
            list_img = requests.get(img).content
        except (AttributeError, IndexError):
            Nobraukums = None
        
        holder = [Marka, Model, Virsbūve, Gads, Price, Tehn_aps, Transmition, Motors, Krāsa, Nobraukums, link]
        if holder.count(None) <= 3:
            holder = ["None" if x is None else x for x in holder]
            if Marka == Type or Type == None: 
                saved_data.append(holder)

    except Exception as exc:
        print(f"Error processing {link}: {exc}")


#Get links from page

def Process_Page(url,Type):
    try:
        # Get links
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        links = []

        car_table = soup.find('table', attrs={'cellpadding': '2'})
        tr_table = car_table.find_all('tr')
        tr_table = tr_table[1:]
        tr_table = tr_table[:-1]

        for tr in tr_table:
            td_link = tr.find('td', class_='msg2')
            Cars_link = td_link.find('a').get('href')
            links.append("https://www.ss.com" + Cars_link)

        # Lunch worker
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(links)) as executor:
            futures = {executor.submit(Process_link, link, Type): link for link in links}
            for future in concurrent.futures.as_completed(futures):
                link = futures[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f"Error processing {link}: {exc}")

    except Exception as exc:
        print(f"Error processing {url}: {exc}")



def Scraping(base_url,Type):
    counter = 1
    
    while True:
        page_url = base_url + "page" + str(counter) + ".html"
        response = requests.get(page_url)
        if response.url == base_url and counter >= 2:  # Check if the URL ends with the base URL
            break
        Process_Page(page_url, Type)
        counter += 1
        print(f"Next page {Type}")

    
    # Save the data to a JSON file
    
    end_time = time.time()
    print("Program execution time for : {:.2f} seconds".format(end_time - start_time) + f" {Type}")

#Get all car types
def Car_types():
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        car_table = soup.find('div', attrs={'align': 'right'})
        links = car_table.find_all('a')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(Scraping, "https://www.ss.com" + link.get('href'), link.text.lower().capitalize() if link.text.lower().capitalize() != "Citas markas" else None): link for link in links}
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")
        
        with open('Holder.json', 'w') as f:
            json.dump(saved_data, f)

        print("Saved =========================")
    except :
        print("Failed")

if __name__ == "__main__":
    Car_types()



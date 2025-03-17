import requests
import json
from bs4 import BeautifulSoup


link_list = []
nosukumu_holder = ["Marka", "Model", "Virsbūve", "Gads", "Cena", "Tekniskā apskate", "Transmition", "Motors", "Krāsa", "Nobraukums", "Links"]
saved_data = []
saved_data.append(nosukumu_holder)

base_url = "https://www.ss.com/lv/transport/cars/lexus/"

# Save the data to a JSON file

response = requests.get(base_url)
if response.status_code == 200: 
    counter= 2
    setted_link = base_url
    #getting links
    while True :
        try:
            response = requests.get(setted_link)
        except requests.exceptions.Timeout:
            print("Timeout error: the request took too long")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        soup = BeautifulSoup(response.content, "html.parser")
        car_table = soup.find('table', attrs={'cellpadding': '2'})
        tr_table = car_table.find_all('tr')
        tr_table = tr_table[1:]
        tr_table = tr_table[:-1]
        for tr in tr_table:
            td_link = tr.find('td', class_='msg2')
            link = td_link.find('a')
            link_list.append("https://www.ss.com" + link.get('href'))

        #going to new link
        new_link = link_list[0]
        for link in link_list:

            new_link = link
            new_link_site = requests.get(new_link)
            soup = BeautifulSoup(new_link_site.content, "html.parser")


            # Getting data
            try:
                Marka = link_list[0].split("/")[7].capitalize()
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
                try :
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

            

            holder = [Marka, Model, Virsbūve, Gads, Price, Tehn_aps, Transmition, Motors, Krāsa, Nobraukums, new_link,]
            if holder.count(None) <= 3:
                holder = ["None" if x is None else x for x in holder]
                saved_data.append(holder)
            
        setted_link = base_url + "page" + str(counter) + ".html"
        response = requests.get(setted_link)
        if response.url == base_url :
            print("Page  finished: " + str(counter-1))
            break
        else :
            print("Page  finished: " + str(counter-1))
            counter += 1
            
            

    with open('data.json', 'w') as f:
        json.dump(saved_data, f)

else:
    print("Error:", response.status_code)
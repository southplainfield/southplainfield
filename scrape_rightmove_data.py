# importing our libraries

import random
import time
from datetime import date, timedelta
import pandas as pd
import requests
from bs4 import BeautifulSoup

BOROUGHS = {
    "Blaenau Gwent": "5E61249",
    "Bridgend": "5E61250",
    "Caerphilly": "5E93473",
    "Cardiff": "5E93482",
    "Carmarthenshire": "5E61292",
    "Ceredigion": "5E93470",
    "Conwy": "5E91980",
    "Denbighshire": "5E61295",
    "Flintshire": "5E61300",
    "Gwynedd": "5E61523",
    "Isle of Anglesey": "5E61553",
    "Merthyr Tydfil": "5E93479",
    "Monmouthshire": "5E61312",
    "Neath Port Talbot": "5E61453",
    "Newport": "5E93476",
    "Pembrokeshire": "5E61318",
    "Powys": "5E61454",
    "Rhondda Cynon Taf": "5E61254",
    "Swansea": "5E92947",
    "Torfaen": "5E61456",
    "Vale of Glamorgan": "5E61255",
    "Wrexham": "5E93467"
}


def main():
    # initialise index, this tracks the page number we are on. every additional page adds 24 to the index

    # create lists to store our data
    all_apartment_links = []
    all_description = []
    all_address = []
    all_price = []
    # added dbocq 06/07
    all_note = []
    today = date.today().strftime("%m/%d/%Y")
    yesterday = (date.today() - timedelta(1)).strftime("%m/%d/%Y")

    # apparently the maximum page limit for rightmove is 42
    # for borough in list(BOROUGHS.values()):
    for borough in ["5E61523"]:
        # initialise index, this tracks the page number we are on. every additional page adds 24 to the index
        index = 0

        key = [key for key, value in BOROUGHS.items() if value == borough]
        print(f"We are scraping the borough named: {key}")
        for pages in range(41):

            # define our user headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }

            if index == 0:
                rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            elif index != 0:
                rightmove = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{borough}&sortType=6&index={index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

            # request our webpage
            res = requests.get(rightmove, headers=headers)

            # check status
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")

            # This gets the list of apartments
            apartments = soup.find_all("div", class_="l-searchResult is-list")

            # This gets the number of listings
            number_of_listings = soup.find(
                "span", {"class": "searchHeader-resultCount"}
            )
            number_of_listings = number_of_listings.get_text()
            number_of_listings = int(number_of_listings.replace(",", ""))

            for i in range(len(apartments)):
                # tracks which apartment we are on in the page
                first_var = apartments[i]

                # append link
                apartment_info = first_var.find("a", class_="propertyCard-link")
                # print(apartment_info)
                link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]
                all_apartment_links.append(link)

                # append address, including the county for better geocoding later
                address = (
                    apartment_info.find("address", class_="propertyCard-address")
                    .get_text()
                    .strip()
                )
                address = address + ', ' + key[0]
                all_address.append(address)

                # append description
                description = (
                    apartment_info.find("h2", class_="propertyCard-title")
                    .get_text()
                    .strip()
                )
                all_description.append(description)

                # append price
                price = (
                    first_var.find("div", class_="propertyCard-priceValue")
                    .get_text()
                    .strip()
                )
                all_price.append(price)

                # append note. interesting field added dboc 06/07
                note = (
                    first_var.find("span", class_ ="propertyCard-branchSummary-addedOrReduced")
                    .get_text()
                    .strip()
                )

                note = note.replace("today", str(today))
                note = note.replace("yesterday", str(yesterday))

                all_note.append(note)

            print(f"You have scrapped {pages + 1} pages of apartment listings.")
            print(f"You have {number_of_listings - index} listings left to go")
            print("\n")

            # code to make them think we are human
            time.sleep(random.randint(1, 3))
            index = index + 24

            if index >= number_of_listings:
                break

    # convert data to dataframe
    data = {
        "Links": all_apartment_links,
        "Address": all_address,
        "Description": all_description,
        "Price": all_price,
        "Notes": all_note,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(r"sales_data.csv", encoding="utf-8", header="true", index=False)


if __name__ == "__main__":
    main()

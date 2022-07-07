import pandas as pd
from get_coordinates import get_coordinates
import clean

def main():
    # load in  lr_sales_data
    lr_sales_data = pd.read_csv('landregistry_data.csv')

    # clean
    clean.drop_junk_columns(lr_sales_data)
    clean.drop_columns(lr_sales_data, "unique_id")
    clean.replace_abbr(lr_sales_data, 'new_build', {'N': 'No', 'Y': 'Yes'})
    clean.replace_abbr(lr_sales_data, 'property_type',
                       {'F': 'flat/maisonette', 'O': 'other', 'T': 'terrace', 'D': 'detached',
                                     'S': 'semi-detached'})
    clean.replace_abbr(lr_sales_data, 'estate_type', {'F': 'freehold', 'L': 'leasehold'})
    #contruct single address field
    clean.concatanate_columns(lr_sales_data, ['saon', 'paon', 'street', 'locality', 'town', 'district', 'postcode'], 'address')

    # get long and lat
    coordinates =  lr_sales_data['address'].apply(lambda x: pd.Series(get_coordinates(x), index=['Latitude', 'Longitude']))

    lr_sales_data = pd.concat([lr_sales_data[:], coordinates[:]], axis="columns")

     # return to csv
    lr_sales_data.to_csv(r"landregistry_data.csv", encoding="utf-8", header="true", index=False)

if __name__ == "__main__":
    main()

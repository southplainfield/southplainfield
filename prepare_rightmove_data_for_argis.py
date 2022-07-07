import pandas as pd
from get_coordinates import get_coordinates
import clean
from get_bedrooms_from_desc import get_bedrooms

def main():
    # load in sales data
    rm_sales_data = pd.read_csv('sales_data.csv')

    # Get the number of bedrooms
    rm_sales_data['Number of bedrooms'] = rm_sales_data['Description'].apply(get_bedrooms)

    # clean
    clean.clean_NaN(rm_sales_data,'Number of bedrooms')
    clean.clean_price(rm_sales_data)

    # get long and lat
    coordinates = rm_sales_data['Address'].apply(lambda x: pd.Series(get_coordinates(x), index=['Latitude', 'Longitude']))

    rm_sales_data = pd.concat([rm_sales_data[:], coordinates[:]], axis="columns")

    rm_sales_data.to_csv(r"rm_sales_data.csv", encoding="utf-8", header="true", index=False)

if __name__ == "__main__":
    main()

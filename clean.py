#import

#define

# columns with no data/all None
def drop_junk_columns(data):
    data.dropna(how='all', axis=1, inplace=True)

# columns with data
def drop_columns(data,column):
    data.drop([column], axis=1, inplace=True)

# columns with flags. The replace values are in a dict e.g.  {'F': 'freehold', 'L': 'leasehold'})
def replace_abbr(data,column,replace_values):
    data.replace({column: replace_values}, inplace=True)

#combine column removing null and added a separator (bug:first separator will appear at position zero)
def concatanate_columns(data: object, source_columns: object, column: object) -> object:
    data[source_columns] = data[source_columns].fillna('')
    data[column] = data[source_columns].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

#remove nulls
def clean_NaN(data,column):
    # remove 'Land for Sale'
    data.dropna(subset=[column], inplace=True)

#specific clean for rightmove price data
def clean_price(data):
    # remove POA
    data.drop(data[data['Price'] == 'POA'].index, inplace=True)
    # convert currency to integer
    data['Price'] = data['Price'].str.replace(',', '')
    data['Price'] = data['Price'].str.replace('£', '')
    data['Price'] = data['Price'].astype('int')


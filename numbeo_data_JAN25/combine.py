import pandas as pd
import numpy as np
from functools import reduce
from regions_mapping import regions2countries, continents2regions

filenames = [
    'Average Monthly Net Salary (After Tax) (Salaries And Financing) by City.tsv',
    'Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate (Salaries And Financing) by City.tsv',
    'Prices by City of Apartment (1 bedroom) in City Centre (Rent Per Month).tsv',
    'Prices by City of Apartment (1 bedroom) Outside of Centre (Rent Per Month).tsv',
    'Prices by City of Apartment (3 bedrooms) in City Centre (Rent Per Month).tsv',
    'Prices by City of Apartment (3 bedrooms) Outside of Centre (Rent Per Month).tsv', 
    'Prices by City of Price per Square Meter to Buy Apartment in City Centre (Buy Apartment Price).tsv',
    'Prices by City of Price per Square Meter to Buy Apartment Outside of Centre (Buy Apartment Price).tsv'
]

def get_df(filename):
    return pd.read_csv(filename, sep='\t', header=0).drop(columns=['Rank'])

cities = [set(get_df(fn)['City']) for fn in filenames]
all_cities = list(reduce(lambda a,b: a | b, cities, cities[0]))
all_cities_df = pd.DataFrame(data={'City': all_cities})
all_cities_df.to_csv("all_cities.tsv", sep = "\t", index=False)
# complete_data_cities = list(reduce(lambda a,b: a & b, cities, cities[0]))
# print(len(all_cities), len(complete_data_cities))

out_df = get_df(filenames[0])
for filename in filenames[1:]:
    out_df = out_df.merge(get_df(filename), how='inner', on=['City'])

# enhance cities with regions (country, region, continent)
def get_city_regions(city):
    country = city.split(',', 1)[1].strip()
    region, continent = None, None
    for k,v in regions2countries.items():
        if country in v:
            region = k
    if region:
        for k,v in continents2regions.items():
            if region in v:
                continent = k
    return country, region, continent


out_df['Region'] = out_df['City'].map(lambda x: get_city_regions(x)[1])
out_df['Continent'] = out_df['City'].map(lambda x: get_city_regions(x)[2])

out_df.to_csv("combined_data.tsv", sep = "\t", index=False)

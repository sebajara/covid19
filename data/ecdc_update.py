import wget

wget.download('https://opendata.ecdc.europa.eu/covid19/casedistribution/csv',
              'ecdc/ecdc_data.csv')


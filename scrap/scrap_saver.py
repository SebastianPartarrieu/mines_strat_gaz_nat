from table_scraper import Browser as Browser_forward
from graph_scraper import Browser as Browser_spot # to change
import datetime
import csv
import pandas as pd
import sys
import argparse
import os 



def filename_constructor(directory,info,active, price_type):
    """ Function that construct the path to the file depending on the GNL type
    """
    active = active.replace(' ','_')
    unit = info.split(' ')[-1].replace('/', '_')
    filename = directory + '/' + price_type + '_' + unit +'_'+active+'.csv'
    return filename

def list_csv_dir( directory):
    """
    Sparse all the csv files present in the active directory
    """
    files = list(map(lambda x : directory +'/'+ x, filter(lambda x : x[-4:]=='.csv',os.listdir(directory))))
    return files 


def data_initializer(directory, price_type, specific_type = False):
    """Sparse as much data as possible supposing that there is no one existing before
    Create the data base architecture
    """
    functions= {"forward": Browser_forward, "spot" : Browser_spot }
    browser = functions[price_type]()

    for info, active, table in browser.scraper_iterator( specific_type): 
        table['Trading Day'] = pd.to_datetime(table['Trading Day'],format = '%Y-%m-%d')
        table = table.sort_values('Trading Day')
        filename = filename_constructor(directory, info, active,price_type)
        table.to_csv(filename, index = False)        

def data_updater(directory, price_type, specific_type = False ):
    """Read the daily data and add to the existing DB only the missing one 
        If the data do not exist, it will creat a table
    """
    functions= {"forward": Browser_forward, "spot" : Browser_spot }
    browser = functions[price_type]()
    list_csv = list_csv_dir(directory)
    print(list_csv)
    for info, active, table in browser.scraper_iterator( specific_type): 
        table['Trading Day'] = pd.to_datetime(table['Trading Day'],format = '%Y-%m-%d')
        table = table.sort_values('Trading Day')
        filename = filename_constructor(directory, info, active,price_type)
        if filename in list_csv:
            existing_data = pd.read_csv(filename)
            existing_data = existing_data.sort_values('Trading Day')
            existing_data['Trading Day'] = pd.to_datetime(existing_data['Trading Day'],format = '%Y-%m-%d')
            last_date  = max(existing_data['Trading Day'])
            print(' last_recorded_date', last_date)
            table = table[ table['Trading Day'] > last_date ]
            existing_data = existing_data.append(table, sort = False)
            existing_data.to_csv(filename, index = False)
        else : 
            table.to_csv(filename, index = False) 
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--directory", help="where to update files")
    parser.add_argument("-p","--product", help =" Prodct type required default = ['spot','forward]")
    parser.add_argument("-s","--specific", help = "Specific market desired")
    args = parser.parse_args()
    if not args.directory :
        directory  = './scrap/last_save'
    else : 
        directory = args.directory
    
    if args.product == 'spot':
        data_updater(directory,'spot', args.specific)
    elif args.product == 'forward':
        data_updater(directory,'forward',args.specific)
    else : 
        data_updater('./scrap/last_save','forward',args.specific)
        data_updater('./scrap/last_save','spot', args. specific)

if __name__ == '__main__':
    sys.exit(main())
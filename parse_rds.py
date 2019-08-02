from appstore_dom_selectors import *
from bs4 import BeautifulSoup
import os, sys
import pprint
import pyreadr
import csv
import logging

logging.basicConfig(filename='logs/log.txt', level=logging.DEBUG)

## Allocate list to hold all app's data
## Should chunk this?
apps = []

## Get the documents
## Loop through the directory of RDS files
for filename in os.listdir('/Users/bjg/r_html/rds_input'):

    try:
        file = os.path.abspath(os.path.join('rds_input', filename))
        app_rds = pyreadr.read_r(file)

        app_df = app_rds[None]
        app_html = app_df.iloc[0,0]

        app_soup = BeautifulSoup(app_html, 'lxml')

        apps.append(get_app_data(app_soup, filename))


    except:
        logging.warning(f'File: {file} failed to read.')
        pass


fieldnames = list(apps[0].keys())

with open('output/first_output.tsv', 'w') as tsvfile:

    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for app in apps:
        writer.writerow(app)






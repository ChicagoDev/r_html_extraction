from appstore_dom_selectors import *
from bs4 import BeautifulSoup
import os, sys
import pprint
import pyreadr
import csv
import logging

rds_directory_full_path = '/Users/bjg/r_html/rds_input'

rds_directory = rds_directory_full_path.split('/')[-1]
logging.basicConfig(filename='logs/log.txt', level=logging.DEBUG)

## Allocate list to hold all app's data
## Should chunk this?
apps = []

## Configure The Batch
for root, dirs, files in os.walk(rds_directory_full_path):

    for file in files:

        f_name = os.path.join(rds_directory_full_path, file)
        app_rds = pyreadr.read_r(f_name)
        app_df = app_rds[None]
        app_html = app_df.iloc[0, 0]

        app_soup = BeautifulSoup(app_html, 'lxml')

        apps.append(get_app_data(app_soup, f_name))


fieldnames = list(apps[0].keys())

with open('output/first_output.tsv', 'w') as tsvfile:

    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for app in apps:
        writer.writerow(app)






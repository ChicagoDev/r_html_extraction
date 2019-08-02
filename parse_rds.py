from appstore_dom_selectors import *
from bs4 import BeautifulSoup
import os, sys
import pprint
import pyreadr
import csv

## Allocate variable for app data
apps = []
# or df?

## Get the documents

for filename in os.listdir('/Users/bjg/r_html/rds_input'):

    file = os.path.abspath(os.path.join('rds_input', filename))
    app_rds = pyreadr.read_r(file)
    app_df = app_rds[None]
    app_html = app_df.iloc[0,0]
    app_soup = BeautifulSoup(app_html, 'lxml')

    apps.append(get_app_data(app_soup))

fieldnames = list(apps[0].keys())

with open('output/first_output.tsv', 'w') as tsvfile:

    writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

    for app in apps:
        writer.writerow(app)






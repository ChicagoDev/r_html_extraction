from appstore_dom_selectors import *
from bs4 import BeautifulSoup
import os, sys
import pyreadr
import csv
import logging

rds_directory_full_path = '/Users/bjg/r_html/big_rds_input/appdescription'

output_filename = 'output/appstore_data'
output_filenum = 0
tsv_outfile = open(output_filename + '.tsv', 'w')

#Value at which apps in memory should be appended to the tsv file
#Or dumped to a new tsv file
dump_threshold = 500
apps_read = 0

stop_number = 5

rds_directory = rds_directory_full_path.split('/')[-1]

logging.basicConfig(filename='logs/log.txt', level=logging.DEBUG)

## Open RDS File Convert to HTML
def rds_to_html(file):

    f_name = os.path.join(rds_directory_full_path, file)
    app_rds = pyreadr.read_r(f_name)
    app_df = app_rds[None]
    app_html = app_df.iloc[0, 0]

    return app_html

# Obtain the Field Names for TSV file
# Just gets the first file
fieldnames = []
for root, dirs, files in os.walk(rds_directory_full_path):
    for file in files:
        f_name = os.path.join(rds_directory_full_path, file)
        app_rds = pyreadr.read_r(f_name)
        app_df = app_rds[None]
        app_html = app_df.iloc[0, 0]
        app_soup = BeautifulSoup(app_html, 'lxml')

        #Get the field names
        fieldnames = list(get_app_data(app_soup, f_name).keys())
        break
    break

# Create the TSV file
tsv_chunk_writer = csv.DictWriter(tsv_outfile, fieldnames=fieldnames, delimiter='\t')
tsv_chunk_writer.writeheader()

## Allocate list to hold all apps' data
##
apps = []



#Parse the data
for root, dirs, files in os.walk(rds_directory_full_path):

    for file in files:


        # f_name = os.path.join(rds_directory_full_path, file)
        # app_rds = pyreadr.read_r(f_name)
        # app_df = app_rds[None]
        # app_html = app_df.iloc[0, 0]

        app_html = rds_to_html(file)

        app_soup = BeautifulSoup(app_html, 'lxml')

        apps.append(get_app_data(app_soup, f_name))

        apps_read = apps_read + 1

        ## File Writing Portion
        ##
        ## When we have accumulated a lot of files, Append them to the TSV.
        if apps_read == dump_threshold:
            print(f'Met Dump Threshold')
            #Do Dump to TSV
            for app in apps:

                # Need to create new file with updated headers
                try:
                    tsv_chunk_writer.writerow(app)


                # Need to create new file with updated headers
                except:
                    print(f'HEADER MISMATCH')
                    tsv_outfile.close()
                    output_filenum += 1
                    tsv_outfile = open(output_filename + '_' + str(output_filenum) + '.tsv', 'w')

                    fieldnames = list(app.keys())
                    tsv_chunk_writer = csv.DictWriter(tsv_outfile, fieldnames=fieldnames, delimiter='\t')
                    tsv_chunk_writer.writeheader()
                    tsv_chunk_writer.writerow(app)



            #reset apps_read
            del apps[:]
            apps_read = 0

            stop_number -= 1

            if stop_number == 0:
                sys.exit('Read in enough files')


## Dump the remaining files
for app in apps:
    tsv_chunk_writer.writerow(app)

tsv_outfile.close()






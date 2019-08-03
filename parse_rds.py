from appstore_dom_selectors import *
from bs4 import BeautifulSoup
import os, sys
import pyreadr
import csv
from pathlib import Path

# The directory where your .rds files are stored
rds_directory_full_path = Path('/Users/bjg/r_html/big_rds_input/appdescription')

# The desired output directory. Relative path.
output_filename = Path('output/appstore_data.tsv')

#Alter this variable to change the batch size
dump_threshold = 40

# Alter this variable to increase or decrease the sample size for testing.
# If you do not want to test, and want to run on a full data-set,
# Comment-out lines 102-106
stop_number = 20

############################################################################################
### File-Configurations
output_filenum = 0
tsv_outfile = open(output_filename, 'w')


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

        ## Add the app identifier as a field
        fieldnames.insert(0, 'app_id')

        break
    break # I think this is legacy, but don't want to try removing it now

# Create the TSV file
tsv_chunk_writer = csv.DictWriter(tsv_outfile, fieldnames=fieldnames, delimiter='\t')
tsv_chunk_writer.writeheader()

## Allocate list to hold all apps' data
##
apps = []

#Parse the data
iterations = 1
for root, dirs, files in os.walk(rds_directory_full_path):

    for file in files:
        app_identifier = file[1:]

        app_html = rds_to_html(file)

        app_soup = BeautifulSoup(app_html, 'lxml')

        apps.append(get_app_data(app_soup, f_name))

        ## File Writing Portion
        ##
        ## When we have accumulated a lot of files, Append them to the TSV.
        if len(apps) == dump_threshold:

            print(f'Processed Batch {iterations}, writing to file ...')

            #Do Dump to TSV
            for app in apps:

                # Assign the App Identifier
                app['app_id'] = app_identifier

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

                    ## Add app identifier to fields
                    fieldnames.insert(0, 'app_id')

                    tsv_chunk_writer = csv.DictWriter(tsv_outfile, fieldnames=fieldnames, delimiter='\t')
                    tsv_chunk_writer.writeheader()
                    tsv_chunk_writer.writerow(app)


            print(f'\n{len(apps)} apps written to .tsv file.\n{dump_threshold*iterations} apps written in total.')
            iterations += 1



            #reset apps_read
            del apps[:]

            #print(f'Decrementing stop number')
            stop_number -= 1

            if stop_number == 0:
                sys.exit('Read in enough files')


## Dump the remaining files
for app in apps:
    tsv_chunk_writer.writerow(app)

tsv_outfile.close()






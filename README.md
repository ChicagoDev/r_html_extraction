# App Store .rds to .tdf conversion script

## Install 
With your python package manager, ensure you have the following installed:
* BeautifulSoup
* pyreadr

## Place things in the right place
From here, copy:
* parse_rds.py
* appstore_dom_selectors.py

To the directory you have your RDS files in. And in that directory execute: 

`mkdir output logs`

<br>

## Edit Settings
In `parse_rds.py` you need to edit the value of one variable. Assign the full file-system path of your rds-file
 directory to `rds_directory_full_path`
 
<br>

## Run Script
In the shell:
 
 `python parse_rds.py`
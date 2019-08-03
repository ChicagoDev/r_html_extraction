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
 
 Also, note the other variables at the top of the script. `dump_threshold` determines how many processed .rds files
  to maintain in memory before being written to the csv file. Increasing the variable may increase performance, to a
   point. 
   
   `stop_number` can be used for testing different sample sizes. Number of samples processed are equal to
    `stop_number` * `dump_threashold`
    
   To run the script on the entire data-set, comment out the lines (102-106) in parse_rds.py:
    
            print(f'Decrementing stop number')
            stop_number -= 1
            
            if stop_number == 0:
                sys.exit('Read in enough files')
 
<br>

## Run Script
In the shell:
 
 `python parse_rds.py`
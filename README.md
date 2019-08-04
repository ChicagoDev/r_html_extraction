# Converting HTML saved in .rds files into .tsv and Pands DataFrames

The single function to convert a .rds file to a Pandas DataFrame is in `utils/rds_to_pandas_df.py`. 

The script that utilizes the function is in this root directory. `rds_html_to_tsv.py`. Change the Pandas output .to_feather, or .to_pickle here if you desire different saving formats. 

The script that batch-processed 175,000 .rds files is located in `big_script/parse_rds.py`. See running on large datasets for where to customize input-output paths. 

## Install 
With your python package manager, ensure you have the following installed:
* BeautifulSoup
* pyreadr

`git clone`

`mkdir output logs`

### To Convert one RDS file to a tsv File
Run the script rds_html_to_tsv.py 

`rds_html_to_tsv.py   .rds_infile    outfile.tsv`

### The single RDS conversion function is in `utils/rds_to_pandas_df.py`
It has a long file name, but I alias it on import. Ex:

`from utils.rds_to_pandas_df import 
parse_one_rds_file_to_html_extracted_pandas_df 
as convert_rds`

Then `convert_rds(filename)` will convert a .rds file to a pandas DataFrame.

**On lines 10-11 in this file are platform-specific Path code that may need to be changed on Windows**

## Running on a Large Data Set
### Edit Settings
In `big_script/parse_rds.py` you need to edit the value of one variable. Assign the full file-system path of your rds-file
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

#### Run Script
In the shell:
 
 `python parse_rds.py`
 
## Overall Structure

If you want data fields extracted from the embedded web pages that aren't yet in the code, the first step is building a BeautifulSoup selector to find your data. 

* Create a function in appstore_dom_selectors.py that encapsulates your BeautifulSoup function and returns a piece of data. Ex: `get_app_description(beautiful_soup_root_object)`
* * This function should use a try-except block, and the except block should return either `float('nan')` or `False`
* In appstore_dom_selectors.py, there is a function `get_app_data(app_soup, fs_identifier)`
* * In the `app_features` dictionary create a new key-value-pair with the key being a field-name and the value being the return value of your BeautifulSoup funciton
* * * Ex: `app_features['cool_new_extracted_feature'] = get_new_feature(bs_app_object)

Retrieving single pieces of data with Beautiful Soup requires no further changes in the code. But getting nested data requires flattenning and an example of how to integrate a complex BeautifulSoup result into the parser can be seen in the `get_app_info_fields_dict()` method and all its related data, like `supported_info_fields`. 

## Platform Issues

I have added WindowsPath options wherever paths occur in the code. In `parse_rds.py` and `rds_to_pandas_df.py`:
* Currently lines 10-16 in `parse_rds.py` and 14-15 in `rds_to_pandas_df.py`

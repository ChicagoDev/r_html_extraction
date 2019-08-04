import pandas as pd
from utils.rds_file_reader import rds_to_html
from utils.appstore_dom_selectors import get_app_data
from bs4 import BeautifulSoup
from pathlib import Path, WindowsPath


def parse_one_rds_file_to_html_extracted_pandas_df(file_name):



    rds_file_path = Path(file_name)

    #WINDOWS PATH UNTESTED
    #rds_file_path = WindowsPath(file_name)

    # The last part of the filename, ignoring the prefix-dot.
    app_identifier = rds_file_path.parts[-1]

    #Get HTML as string from RDS file
    app_html = rds_to_html(str(rds_file_path))

    #Convert HTML to a BeautifulSoup object for DOM DataSelection
    app_soup = BeautifulSoup(app_html, 'lxml')

    app_data_dict = {'app_id': app_identifier}

    # get_app_data() contains custom DOM selectors that retrieve the desired data from App Store HTML pages
    app_data = get_app_data(app_soup, app_identifier)

    app_data_dict.update(app_data)


    ## Need to place data in arrays in order to pass directly into pandas
    app_data_dict_pandas_compatible = { k: [v] for k, v in app_data_dict.items() }

    app_df = pd.DataFrame.from_dict(app_data_dict_pandas_compatible)

    return app_df


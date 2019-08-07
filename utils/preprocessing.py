from bs4 import BeautifulSoup
import os
import pyreadr
from pathlib import Path

def rds_to_html(file_path):

    f_name = str(Path(file_path))
    app_rds = pyreadr.read_r(f_name)
    app_df = app_rds[None]
    app_html = app_df.iloc[0, 0]

    return app_html

def html_to_beautiful_soup(html):
    return BeautifulSoup(html, 'lxml')
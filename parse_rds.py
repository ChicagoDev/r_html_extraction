from appstore_dom_selectors import *
from bs4 import BeautifulSoup
import pprint

finra_app_soup = BeautifulSoup(open('html/finra7.html'), 'lxml')

app_features = {}

app_features['app_name'] = get_app_name(finra_app_soup)
app_features['app_rating'] = get_app_rating(finra_app_soup)
app_features['app_description'] = get_app_description(finra_app_soup)
app_features['privacy_policy'] = get_app_privacy_policy(finra_app_soup)
app_features['info_fields'] = get_app_info_fields_dict(finra_app_soup)
app_features['ratings_hist'] = get_app_ratings_histogram(finra_app_soup)

pprint.pprint(app_features)

from bs4 import BeautifulSoup, Tag
import re

num_re = re.compile('[0-9]+')
hist_keys = ['percent_5_star', 'percent_4_star', 'percent_3_star', 'percent_2_star', 'percent_1_star']
hist_nans = [float('nan') for _ in range(4)]

## Get all the App Data into one object
def get_app_data(app_soup):
    app_features = {}
    app_features['app_name'] = get_app_name(app_soup)
    app_features['app_rating'] = get_app_rating(app_soup)
    app_features['app_description'] = get_app_description(app_soup)
    app_features['privacy_policy'] = get_app_privacy_policy(app_soup)

    for k, v in get_app_ratings_histogram(app_soup).items():
        app_features[k] = v

    for k, v in get_app_info_fields_dict(app_soup).items():
        app_features[k] = v

    return app_features




def get_app_name(app_store_soup):
    try:
        return app_store_soup.find('h1').text.strip().split('\n')[0]
    except:
        return float('nan')

def get_app_rating(app_store_soup):
    try:
        return app_store_soup.find('span', class_='we-customer-ratings__averages__display').get_text()
    except:
        return float('nan')

def get_app_description(app_store_soup):
    try:
        return app_store_soup.find('h2', text='Description').parent.find('p').get_text()
    except:
        return float('nan')

def get_app_privacy_policy(app_store_soup):
    return app_store_soup.find('a', text='Privacy Policy')['href']

def get_app_info_fields_dict(app_store_soup):
    information_dl = app_store_soup.find('dl', attrs={'class': 'information-list information-list--app medium-columns'})
    info_fields = [ _.get_text() for _ in information_dl.find_all('dt')]
    info_values = [_.get_text().strip() for _ in information_dl.find_all('dd')]
    return dict(zip(info_fields, info_values))

def get_app_ratings_histogram(app_store_soup):

    try:
        ratings_bar_graph = app_store_soup.find('figure', { 'class': 'we-star-bar-graph' })
        ratings_bars = ratings_bar_graph.find_all('div', { 'class': 'we-star-bar-graph__bar__foreground-bar' })

        bar_attributes = [_.attrs for _ in ratings_bars]

        star_rating_percentages = [re.search(num_re, _['style']).group(0) for _ in bar_attributes]
        return dict(zip(hist_keys, star_rating_percentages))

    except:
        return dict(zip(hist_keys, hist_nans))

def are_tags(potential_tags):
    return [_ if type(_) is Tag else None for _ in potential_tags]

def get_developer_response(app_store_soup):

    dev_response_locators = app_store_soup.find_all('h3', {
        'class': 'we-customer-review__header we-customer-review__header--response' })

    dev_response_blockquotes = [are_tags(_.next_siblings) for _ in dev_response_locators]

    reviews = []

    for bs4_item_list in dev_response_blockquotes:
        reviews += list(filter(lambda tag: (tag != None), bs4_item_list))

    reviews_text = [_.find('p').get_text() for _ in reviews]

    return reviews_text


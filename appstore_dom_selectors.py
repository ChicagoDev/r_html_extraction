from bs4 import BeautifulSoup, Tag
import re

num_re = re.compile('[0-9]+')
hist_keys = ['5-Star', '4-Star', '3-Star', '2-Star', '1-Star']

def get_app_name(app_store_soup):
    return app_store_soup.find('h1').text.strip().split('\n')[0]

def get_app_rating(app_store_soup):
    try:
        return app_store_soup.find('span', class_='we-customer-ratings__averages__display').get_text()
    except:
        return float('nan')

def get_app_description(app_store_soup):
    return app_store_soup.find('h2', text='Description').parent.find('p').get_text()

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
        return float('nan')

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


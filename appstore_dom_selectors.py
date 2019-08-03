from bs4 import BeautifulSoup, Tag
import re
import logging

logging.basicConfig(filename='logs/dom_selecting_log.txt', level=logging.DEBUG)


num_re = re.compile('[0-9]+')


hist_keys = ['percent_5_star', 'percent_4_star', 'percent_3_star', 'percent_2_star', 'percent_1_star']
hist_nans = [float('nan') for _ in range(5)]

nan_info_fields = {'Seller': float('nan'),
                           'Size': float('nan'),
                           'Category': float('nan'),
                           'Compatibility': float('nan'),
                           'Languages': float('nan'),
                           'Age': float('nan'),
                           'Rating': float('nan'),
                           'Copyright': float('nan'),
                           'Price': float('nan'),
                           'In - App Purchases': float('nan')}

"""
    This function aggregates all the app data using Beautiful Soup DOM traversal. 
"""
def get_app_data(app_soup, fs_identifier):

    logging.debug('----------------------------------------')
    logging.info(f'Retrieving Dom Elements for {fs_identifier}')


    app_features = {}

    app_features['app_name'] = get_app_name(app_soup)
    app_features['app_rating'] = get_app_rating(app_soup)
    app_features['app_description'] = get_app_description(app_soup)
    app_features['privacy_policy'] = get_app_privacy_policy(app_soup)

    # Need to unpack the results here to maintain a flat app_features dictionary
    #
    for k, v in get_app_ratings_histogram(app_soup).items():
        app_features[k] = v

    for k, v in get_app_info_fields_dict(app_soup).items():
        app_features[k] = v

    return app_features

"""
    Below are all selectors using Beautiful Soup to extract AppStore information from the
    supplied HTML
"""

def get_app_name(app_store_soup):
    try:
        return app_store_soup.find('h1').text.strip().split('\n')[0]
    except:
        logging.warning(f'App-Name NOT FOUND in DOM')
        return float('nan')

def get_app_rating(app_store_soup):
    try:
        return app_store_soup.find('span', class_='we-customer-ratings__averages__display').get_text()
    except:
        logging.warning(f'Rating NOT FOUND in DOM')
        return float('nan')

def get_app_description(app_store_soup):
    try:
        return app_store_soup.find('h2', text='Description').parent.find('p').get_text()
    except:
        logging.warning(f'App-Description NOT FOUND in DOM')
        return float('nan')

def get_app_privacy_policy(app_store_soup):
    try:
        return app_store_soup.find('a', text='Privacy Policy')['href']
    except:
        logging.warning(f'Privacy Policy NOT FOUND in DOM')
        return float('nan')

def get_app_info_fields_dict(app_store_soup):
    try:
        information_dl = app_store_soup.find('dl', attrs={'class': 'information-list information-list--app '
                                                                'medium-columns'})

        info_fields = [ _.get_text() for _ in information_dl.find_all('dt')]
        info_values = [_.get_text().strip() for _ in information_dl.find_all('dd')]
        return dict(zip(info_fields, info_values))

    except:
        """
            I am not sure of what the behavior should be here. Because I know a dictionary of the exact same type
            i.e. same keys, needs to be returned every time. In this case if something is missing, it may need 
            more sophistocated error handling, or just need to implement float(nans) here and haven't had the chance 
            yet. 
        """

        logging.warning(f'Not all Info-Fields found in DOM')
        return nan_info_fields

def get_app_ratings_histogram(app_store_soup):
    # Selector is not picking up one one star!
    try:
        ratings_bar_graph = app_store_soup.find('figure', { 'class': 'we-star-bar-graph' })
        ratings_bars = ratings_bar_graph.find_all('div', { 'class': 'we-star-bar-graph__bar__foreground-bar' })

        bar_attributes = [_.attrs for _ in ratings_bars]

        star_rating_percentages = [re.search(num_re, _['style']).group(0) for _ in bar_attributes]
        return dict(zip(hist_keys, star_rating_percentages))

    except:
        logging.warning(f'Histogram-Ratings NOT FOUND in DOM')
        return dict(zip(hist_keys, hist_nans))

# Helper function
def are_tags(potential_tags):
    return [_ if type(_) is Tag else None for _ in potential_tags]



def get_developer_response(app_store_soup):

    """

    """

    try:
        dev_response_locators = app_store_soup.find_all('h3', {
            'class': 'we-customer-review__header we-customer-review__header--response' })

        dev_response_blockquotes = [are_tags(_.next_siblings) for _ in dev_response_locators]

        reviews = []

        for bs4_item_list in dev_response_blockquotes:
            # Only html tags, not BS4 Navigable Strings
            reviews += list(filter(lambda tag: (tag != None), bs4_item_list))

        reviews_text = [_.find('p').get_text() for _ in reviews]

        return reviews_text

    except:
        logging.warning(f'Developer-Response NOT FOUND in DOM')
        return float('nan')


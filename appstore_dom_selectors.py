from bs4 import BeautifulSoup, Tag
import re
import logging
import copy

logging.basicConfig(filename='logs/dom_selecting_log.txt', level=logging.DEBUG)

## Toggle to disable logging and increase performance
#logging.disable(level=logging.CRITICAL)

num_re = re.compile('[0-9]+')


hist_keys = ['percent_5_star', 'percent_4_star', 'percent_3_star', 'percent_2_star', 'percent_1_star']
hist_nans = [float('nan') for _ in range(5)]

no_reviews = {'review_1': float('nan'),
                           'review_2': float('nan'),
                           'review_3': float('nan')}

review_keys = ['review_1', 'review_2', 'review_3']
review_rating_keys = ['review_rating_1', 'review_rating_2', 'review_rating_3']

supported_info_fields = {'Seller': float('nan'),
                           'Size': float('nan'),
                           'Category': float('nan'),
                           'Compatibility': float('nan'),
                           'Languages': float('nan'),
                           'Age Rating': float('nan'),
                           'Copyright': float('nan'),
                           'Price': float('nan'),
                           ### I made a mistake, the following should not be here. But it is working... because it is
                         # forcing
                         # the header... that is all this code really does
                           'has_in_app_purchases': False,
                           'review_1': float('nan'),
                           'review_2': float('nan'),
                           'review_3': float('nan'),
                           'review_rating_1': float('nan'),
                           'review_rating_2': float('nan'),
                           'review_rating_3': float('nan')}

"""
    This function aggregates all the app data using Beautiful Soup DOM traversal. 
"""
def get_app_data(app_soup, fs_identifier):

    logging.debug('\n----------------------------------------')
    logging.info(f'Retrieving Dom Elements for {fs_identifier}')


    app_features = {}

    app_features['app_name'] = get_app_name(app_soup)
    app_features['app_rating'] = get_app_rating(app_soup)
    app_features['count_rating'] = get_rating_count(app_soup)
    app_features['app_description'] = get_app_description(app_soup)
    app_features['privacy_policy'] = get_app_privacy_policy(app_soup)

    # Need to unpack the results here to maintain a flat app_features dictionary
    #
    for k, v in get_app_ratings_histogram(app_soup).items():
        app_features[k] = v


    for k, v in get_app_info_fields_dict(app_soup).items():

       app_features[k] = v

    for k, v in get_app_reviews(app_soup).items():
        app_features[k] = v

    app_features['has_in_app_purchases'] = has_in_app_purchases(app_soup)

    review_ratings = get_featured_review_ratings(app_soup)

    for i, rating in enumerate(review_ratings):
        app_features[review_rating_keys[i]] = rating

    return app_features

"""
    Below are all selectors using Beautiful Soup to extract AppStore information from the
    supplied HTML
"""

def get_app_name(app_store_soup):
    try:
        #h1 = app_store_soup.find('h1').text
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

def get_rating_count(app_store_soup):
    try:
        num_rating = app_store_soup.find('figcaption', { 'class': 'we-rating-count star-rating__count' }).get_text(

        ).split(',')[1].strip()
        return re.search(num_re, num_rating).group(0)

    except:
        logging.warning(f'App not rated')
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

        info_not_all_fields = dict(zip(info_fields, info_values))
        #return info_not_all_fields

        app_info = copy.deepcopy(supported_info_fields)

        for key in app_info.keys():

            if key in info_not_all_fields.keys():

                app_info[key] = info_not_all_fields[key]

        return app_info

    except:
        """
            I am not sure of what the behavior should be here. Because I know a dictionary of the exact same type
            i.e. same keys, needs to be returned every time. In this case if something is missing, it may need 
            more sophistocated error handling, or just need to implement float(nans) here and haven't had the chance 
            yet. 
        """

        logging.warning(f'Not all Info-Fields found in DOM')
        return supported_info_fields

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


def get_app_reviews(app_store_soup):

    try:
        reviews = [_.p.get_text() for _ in app_store_soup.find_all('blockquote', { 'class': 'we-truncate '
                                                                                   'we-truncate--multi-line '
                                                                                            'we-truncate--interactive ember-view we-customer-review__body' })]

        the_reviews = {}

        for i, rev in enumerate(reviews):
            the_reviews[review_keys[i]] = rev

        return the_reviews

    except:
        return no_reviews


def get_featured_review_ratings(app_store_soup):

    try:
        featured_review_ratings = app_store_soup.find_all('figure', {
            'class': 'we-star-rating ember-view we-customer-review__rating we-star-rating--large' })
        featured_review_ratings = [_.attrs['aria-label'][0] for _ in featured_review_ratings]

        return featured_review_ratings

    except:
        logging.warning(f'Review Ratings not Found')
        return []

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

def has_in_app_purchases(app_store_soup):

    try:
        purchased_li_tag = app_store_soup.find('li', { 'class': 'app-header__list__item--in-app-purchase' })

        if type(purchased_li_tag) == Tag:
            return True
        else:
            return False

    except:
        logging.warning(f'Exception when searching for in-app purchases')
        return float('nan')


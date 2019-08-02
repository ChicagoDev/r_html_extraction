# Just A Reference File To Keep Tabs of All Current Selectors

# App Title
# find('h1').text.strip().split('\n')[0]

# App Rating
# .find('span', class_='we-customer-ratings__averages__display').get_text()

# Description
# .find('h2', text='Description').parent.find('p').get_text()

# Privacy Policy
# .find('a', text='Privacy Policy')['href']

# Information Field Data
# information_dl = .find('dl', attrs={'class': 'information-list information-list--app medium-columns'})
# info_fields = [ _.get_text() for _ in information_dl.find_all('dt')]
# info_values = [_.get_text().strip() for _ in information_dl.find_all('dd')]

# Version History: Url may be tied up within some JavaScript

# """
# Obtaining the rating histogram info.
# """
# import re
# num_re = re.compile('[0-9]+')
# stars = [5, 4, 3, 2, 1]
#
# ratings_bar_graph = parsed_church.find('figure', {'class': 'we-star-bar-graph'})
# ratings_bars = ratings_bar_graph.find_all('div', {'class': 'we-star-bar-graph__bar__foreground-bar'})
#
# bar_attributes = [_.attrs for _ in ratings_bars]
#
# star_rating_percentages = [re.search(num_re, _['style']).group(0) for _ in bar_attributes]
#
# print(star_rating_percentages)
# zip(stars, star_rating_percentages)


##
# User Reviews
#
## User Names
#
# users = [_.get_text().strip() for _ in finra_app.find_all('span', {'class': 'we-customer-review__user'})]
#
## Review Body
#
# reviews = [_.p.get_text() for _ in finra_app.find_all('blockquote', {'class': 'we-truncate we-truncate--multi-line
# we-truncate--interactive ember-view we-customer-review__body'})]
#
## Featured Review Stars
#
#featured_review_stars = finra_app.find_all('figure', {'class': 'we-star-rating ember-view we-customer-review__rating we-star-rating--large'})
# stars = [_.attrs['aria-label'][0] for _ in featured_review_stars]
#
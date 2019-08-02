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

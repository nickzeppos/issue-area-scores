# Issue Area Codes
# Scraping policy areas and bill numbers for all bills from 93rd - 115th
# Nick Zeppos
# Summer 2020

# Imports
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from pprint import pprint
import numpy as np
import math

# Defining a function, scrape.


def scrape():

    # Store our url. This url goes to a congress.gov page which contains a list of all policy areas. Each policy area on this page is a link to an
    # advanced search of that policy area, the results of which are all legislative items on congress.gov of that policy area
    url = 'https://www.congress.gov/browse/policyarea/all-congresses'

    # Let's request that url
    page = requests.get(url)

    # And go from a requests object to a parsed page using beautiful soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # We need a few things from this page
    # All of the subject areas, which are contained in an unordered list with class plain little_margin
    ul = soup.find('ul', class_='plain little_margin')

    # From this ul, get the subject area texts, corresponding search links, and the counts of legislative items
    areas = [i.text for i in ul.find_all("li")]
    links = [i['href'] for i in ul.find_all('a', href=True)]
    counts = [i.text for i in ul.find_all('span', class_='count')]

    # Pretty up the subject area values, which just involves removing bracketed numbers and trimming resulting whitespace
    areas = [re.sub(r'\[.*\]', '', i).strip() for i in areas]

    # Pretty up counts, which just involves removing brackets and converting to ints
    counts = [int(re.sub('[^0-9]', '', i)) for i in counts]

    # Now, the actual information we want from these counts is a page number count. We'll be scraping pages that display 100
    # items at a time, so let's divide our count by 100, rounded up if there is any remainder
    last_pages = [math.ceil(i/100) for i in counts]

    # Now we're going to loop through our list of links. This is going to be the first of two for loops.
    for link in links:

        # Create empty list, that we're going to populate with data
        d = []

        # Let's split up our link string, so we can construct proper urls
        base_url = link.split('documentNumber')[0]
        base_url = base_url + 'documentNumber&page='

        # Use index to get the proper value from the last pages list
        last_page = last_pages[links.index(link)]
        print(base_url)

        # And now begin our second loop, where we're going through each page of the subject area specified by our
        # link variable.
        for i in range(1, last_page):

            page = requests.get(base_url + str(i))
            soup = BeautifulSoup(page.content, 'html.parser')

            # Get all the results on the page.
            results = soup.find_all('li', class_='expanded')

            # Get the bill type and number
            bill_info = [r.find('span', class_='result-heading')
                         for r in results]
            bill_info = [bi.text for bi in bill_info]

            # Remove the parentheses and inner contents
            bill_info = [re.sub(r'\([^()]*\)', '', bi) for bi in bill_info]

            # Separate bill and congress values
            bills = [b.split('—')[0] for b in bill_info]
            congresses = [c.split('—')[1].strip() for c in bill_info]

            # Further separate bills into bill type and bill number
            bill_types = [b.rsplit('.', 1)[0] for b in bills]
            bill_numbers = [b.rsplit('.', 1)[1].strip() for b in bills]

            # Now create a vector of policy areas value with the same length as our other stuff
            policy_area = areas[links.index(link)]
            policy_areas = np.repeat(policy_area, len(bill_numbers))

            # Now we're going to zip up our values into a dict, and add it to our d
            d2 = [[bill_type,  bill_number,
                   congress, policy_area] for bill_type, bill_number, congress, policy_area in zip(bill_types, bill_numbers, congresses, policy_areas)]

            # Combine the two lists
            d = d + d2

            pprint(len(d))

        # Convert list to df
        df = pd.DataFrame(
            d, columns=['bill_type', 'bill_number', 'congress', 'policy_area'])
        file_name = "./data/" + policy_area + ".csv"
        pprint("Writing" + file_name)
        df.to_csv(file_name)


scrape()

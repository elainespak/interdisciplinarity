
import re
import time
import requests
import pandas as pd
from tqdm import tqdm
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def category2(s, all_list):
    for name, link in all_list:
        if name[:5] == s[:5]:
            return name

def category1(s, all_list):
    for name, link in all_list:
        if name[:2] == s[:2]:
            return name


### Major List Page
url = 'https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=56'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(2)
htmlSource = driver.page_source
driver.quit()

soup = BeautifulSoup(htmlSource, 'html.parser')

maincontent = soup.find_all('ul', {'id': 'tree_ul_section_0'})[0]

common_url = 'https://nces.ed.gov/ipeds/cipcode/'
all_list = []
for item in maincontent.find_all('a'):
    all_list.append( (item.text, common_url + item['href']) )

all_df = pd.DataFrame(all_list, columns=['category', 'url'])
all_df.to_csv('./data/nces_majors.csv', index=False)

category3_list = []
for name, link in all_list:
    if re.match('\d{2}.\d{4}', name) is not None:
        category3_list.append(name)

key_df = pd.DataFrame(category3_list, columns=['category3'])
key_df['category2'] = key_df['category3'].apply(lambda x: category2(x, all_list))
key_df['category1'] = key_df['category2'].apply(lambda x: category1(x, all_list))
key_df.to_csv('./data/nces_majors_key.csv', index=False)


### Major Page Example

df = pd.read_csv('./data/nces_majors.csv')

d = {'definition': [],
     'see_also': [],
     'change': [],
     'text_change': [],
     'examples': [],
     'code_2020': [],
     'title_2020': [],
     'code_2010': [],
     'title_2010': []
     }

# TODO: Fix the following error: requests.exceptions.SSLError: HTTPSConnectionPool(host='chromedriver.storage.googleapis.com', port=443): Max retries exceeded with url: /LATEST_RELEASE_90.0.4430 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1123)')))
for i in tqdm(range(678, len(df))): # TODO: remove 678
    url = df['url'][i]
    """
    n = randint(1, 10) / randint(2, 4)

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(n)
    htmlSource = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(htmlSource, 'html.parser')
    """
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Definition
    cipdetail = soup.find('div', {'class': 'cipdetail'})
    definition_p = cipdetail.find_all('p')[1]
    definition = re.findall('(?<=<p><strong>Definition:</strong>).*?(?=.\s?<)', str(definition_p))[0]
    definition = definition.strip()

    # See also
    try:
        seealso_span = definition_p.find('span').text
        seealso = re.findall('(?<=See also:).*', seealso_span)[0]
        seealso = seealso.strip()
    except:
        seealso = 'None available'

    # Change
    change_p = cipdetail.find_all('p')[2]
    change = re.findall('(?<=<p><strong>Action:</strong>).*?(?=</p>)', str(change_p))[0]
    change = change.strip()

    # Text Change
    textchange_p = cipdetail.find_all('p')[3]
    try:
        textchange = re.findall('(?<=<p><strong>Text Change: </strong>).*?(?=</p>)', str(textchange_p))[0]
        textchange = textchange.strip()
    except:
        textchange = 'None available'

    # Examples
    summary_examples = soup.find('div', {'class': 'summary_examples'})
    codesummary = summary_examples.find('ul', {'class': 'codesummary'})
    examples = ':::::'.join([li.text.strip() for li in codesummary.find_all('li')])

    # Summary Crosswalk (2010 vs. 2020)
    summary_crosswalk = soup.find('div', {'class': 'summary_crosswalk'})
    table = summary_crosswalk.find_all('tr')[2]
    codes = [code.text.strip() for code in table.find_all('td', {'class': 'code'})]
    titles = [title.text.strip() for title in table.find_all('td', {'class': 'titledesc'})]

    # Append
    d['definition'].append(definition)
    d['see_also'].append(seealso)
    d['change'].append(change)
    d['text_change'].append(textchange)
    d['examples'].append(examples)
    d['code_2020'].append(codes[1])
    d['title_2020'].append(titles[1])
    d['code_2010'].append(codes[0])
    d['title_2010'].append(titles[0])

all_df = pd.DataFrame(data=d)
all_df.to_csv('./data/nces_majors_all_rest.csv', index=False)



### Example
url = 'https://nces.ed.gov/ipeds/cipcode/cipdetail.aspx?y=56&cipid=90509'
req = requests.get(url, headers, verify=False)
soup = BeautifulSoup(req.content, 'html.parser')

url = 'https://nces.ed.gov/ipeds/cipcode/cipdetail.aspx?y=56&cipid=90509'#'https://nces.ed.gov/ipeds/cipcode/cipdetail.aspx?y=56&cipid=91089'
n = randint(1, 10) / randint(2, 4)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(n)
htmlSource = driver.page_source
driver.quit()

# HTML parse
soup = BeautifulSoup(htmlSource, 'html.parser')

# Definition
cipdetail = soup.find('div', {'class': 'cipdetail'})
definition_p = cipdetail.find_all('p')[1]
definition = re.findall('(?<=<p><strong>Definition:</strong>).*?(?=.\s?<)', str(definition_p))[0]
definition = definition.strip()

# See also
seealso_span = definition_p.find('span').text
seealso = re.findall('(?<=See also:).*', seealso_span)[0]
seealso = seealso.strip()

# Change
change_p = cipdetail.find_all('p')[2]
change = re.findall('(?<=<p><strong>Action:</strong>).*?(?=</p>)', str(change_p))[0]
change = change.strip()

# Text Change
textchange_p = cipdetail.find_all('p')[3]
try:
    textchange = re.findall('(?<=<p><strong>Text Change: </strong>).*?(?=</p>)', str(textchange_p))[0]
    textchange = textchange.strip()
except:
    textchange = 'None available'

# Examples
summary_examples = soup.find('div', {'class': 'summary_examples'})
codesummary = summary_examples.find('ul', {'class': 'codesummary'})
examples = ':::::'.join([li.text.strip() for li in codesummary.find_all('li')])

# Summary Crosswalk (2010 vs. 2020)
summary_crosswalk = soup.find('div', {'class': 'summary_crosswalk'})
table = summary_crosswalk.find_all('tr')[2]
codes = [code.text.strip() for code in table.find_all('td', {'class': 'code'})]
titles = [title.text.strip() for title in table.find_all('td', {'class': 'titledesc'})]


# All
definition_list.append(definition)
seealso_list.append(seealso)
change_list.append(change)
textchange_list.append(textchange)
examples_list.append(examples)
code2020_list.append(codes[1])
title2020_list.append(titles[1])
code2010_list.append(codes[0])
title2010_list.append(titles[0])



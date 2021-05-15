
import re
import time
import pandas as pd
from tqdm import tqdm
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


### Major List Page
url = 'https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=56'
n = randint(1, 10) / randint(2, 4)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(n)
htmlSource = driver.page_source
driver.quit()

soup = BeautifulSoup(htmlSource, 'html.parser')

maincontent = soup.find_all('ul', {'id': 'tree_ul_section_0'})[0]

# example
all_list = []
for item in maincontent.find_all('a'):
    all_list.append( (item.text, item['href']) )

category3_list = []
for name, link in all_list:
    if re.match('\d{2}.\d{4}', name) is not None:
        category3_list.append( (name, link) )

df = pd.DataFrame(category3_list, columns=['category3', 'url'])


### Major Page Example
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
definition_p = str(cipdetail.find_all('p')[1])
definition = re.findall('(?<=<p><strong>Definition:</strong>).*?(?=</p>)', definition_p)[0]

# Change
change_p = str(cipdetail.find_all('p')[2])
change = re.findall('(?<=<p><strong>Action:</strong>).*?(?=</p>)', change_p)[0]

# Summary Crosswalk (2010 vs. 2020)
summary_crosswalk = soup.find('div', {'class': 'summary_crosswalk'})
table = summary_crosswalk.find_all('tr')[2]

codes = [code.text for code in table.find_all('td', {'class':'code'})]
titles = [title.text for title in table.find_all('td', {'class':'titledesc'})]
#action = table.find('td', {'class':'action'}).find('img')['alt']

# Examples
summary_examples = soup.find('div', {'class': 'summary_examples'})
codesummary = summary_examples.find('ul', {'class': 'codesummary'})
examples = [li.text for li in codesummary.find_all('li')]

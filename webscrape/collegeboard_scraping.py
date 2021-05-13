
import time
import pandas as pd
from tqdm import tqdm
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver


def reformat(s):
    s = s.lower()
    s = s.replace("'", "").replace(",", "")    
    s = s.replace(' and ', '-').replace(' ','-')
    return s

def make_url(str1, str2, str3):

    str1 = reformat(str1)
    str2 = reformat(str2)
    str3 = reformat(str3)
    common = 'https://bigfuture.collegeboard.org/majors/'
    
    if str2=='none':
        url = common + str1 + '-' + str3
    else:
        url = common + str1 + '-' + str2 + '-' + str3
    
    return url

def get_link(soup, category):
    info = soup.find('div', {'id': 'majorCareerProfile_'+ category})
    categoryLink = info.find_all('a')[0]['href']
    return 'https://bigfuture.collegeboard.org' + categoryLink

def get_list(soup, category):
    items = soup.find('div', {'id': 'majorCareerProfile_'+ category}).find_all('li')
    items_text = [item.text for item in items]
    return ':::::'.join(items_text)

def get_paragraph(soup, category):
    p = soup.find('div', {'id': 'majorCareerProfile_'+ category})
    return p.text


# For Loop

info_paragraph = ['introduction', 'definition', 'help', 'spotlight', 'degreeType',
                  'pullQuoteOne', 'pullQuoteTwo']
info_list = ['readyList', 'collegeList','highSchoolCourseList', 'majorCourseList',
             'relatedMajors', 'relatedCareers']
info_link = ['collegeSearch']
info_all = ['url'] + info_paragraph + info_list + info_link

final_list = []
df = pd.read_csv('../data/collegeboard_majors.csv')

for i in tqdm(range(len(df))):
    
    temp = {info:'' for info in info_all}
    major = df['category4'][i]
    n = randint(1,10)/randint(2,4)
    
    # Open website
    url = make_url(df['category2'][i], df['category3'][i], df['category4'][i])
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(n)
    htmlSource = driver.page_source
    driver.quit()
    
    # HTML parse
    soup = BeautifulSoup(htmlSource, 'html.parser')
    
    # Get info and save it in 'temp'
    for c in info_paragraph:
        try:
            temp[c] = get_paragraph(soup, c)
        except:
            pass#print(f'No {c} for {major}')

    for c in info_list:
        try:
            temp[c] = get_list(soup, c)
        except:
            pass#print(f'No {c} for {major}')

    for c in info_link:
        try:
            temp[c] = get_link(soup, c)
        except:
            pass#print(f'No {c} for {major}')
    
    temp['url'] = url
    
    # Append 'temp'
    final_list.append(temp)


# Save
final_df = pd.DataFrame(final_list)
merged_df = pd.concat([df, final_df], axis=1)
merged_df.to_csv('collegeboard_majors_all.csv', index=False)

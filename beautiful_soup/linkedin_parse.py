import math
from bs4 import BeautifulSoup
import json
import re
import os
from settings import *

file_path = 'company.html'

base_name = os.path.splitext(file_path)[0]
json_filename = f"{base_name}.json"

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

#url of the logo, slogan, linkedin url
script_tag = soup.find('script', type=logo_url_tag)
json_data = json.loads(script_tag.string)

logo_url = json_data.get('logo', {}).get('contentUrl', "Not Found")
url = json_data.get('url', "Not Found")
slogan = json_data.get('slogan', "Not Found").replace('\n', ' ').strip()

#universal name
universal_name = url.split('/')[-1]

#name
name_tag = soup.find('h1')
name = name_tag.text.strip() if name_tag and name_tag.text.strip() else "Not Found"

#sector
sector_tag = soup.find('h2')
sector = sector_tag.text.strip() if sector_tag and sector_tag.text.strip() else "Not Found"

#address
address = soup.find('h3').text if soup.find('h3').text.strip() else "Not Found"

#number of employee
employee_count_tag = soup.find('a', class_=employee_count_tag_settings)
employee_count_text = employee_count_tag.text if employee_count_tag else "Not Found"
employee_count = re.findall(r'\d[\d,.]*', employee_count_text)
employee_count = employee_count[0].replace('.', '').replace(',', '') if employee_count else "Not Found"

#number of employees range
employee_count_tag = soup.find('a', class_=employee_count_tag_settings)
employee_count_text = employee_count_tag.text if employee_count_tag else "Not Found"
employee_count_range = re.findall(r'\d[\d,.]*', employee_count_text)
employee_count_range = employee_count_range[0].replace('.', '').replace(',', '') if employee_count_range else "Not Found"

if employee_count_range != "Not Found":
    employee_count_range = int(employee_count_range)
    if employee_count_range > 1000:
        lower = math.floor(employee_count_range / 1000) * 1000
        upper = math.ceil(employee_count_range / 1000) * 1000
    elif employee_count_range > 100:
        lower = math.floor(employee_count_range / 100) * 100
        upper = math.ceil(employee_count_range / 100) * 100
    else:
        lower = 1
        upper = 100
    employee_count_range = f"{lower} - {upper}"
else:
    employee_count_range = "Not Found"

#about title
about_title = soup.find('h2', class_=about_title_tag).text.strip() if soup.find('h2', class_=about_title_tag) else "Not Found"

#description
description = soup.find('p', class_=description_tag).text.strip() if soup.find('p', class_=description_tag) else "Not Found"

#finding dl tag
dl_content = soup.find('dl', class_=dl_tag)

#website
website_div = dl_content.find('div', {'data-test-id': website_tag})
website = website_div.find('a').text.strip() if website_div and website_div.find('a') else "Not Found"

#industry name
industry_name_div = dl_content.find('div', {'data-test-id': industry_name_tag})
industry_name = industry_name_div.find('dd').text.strip() if industry_name_div and industry_name_div.find('dd') else "Not Found"

#company size
company_size_div = dl_content.find('div', {'data-test-id': company_size_tag})
company_size_text = company_size_div.find('dd').text.strip() if company_size_div and company_size_div.find('dd') else "Not Found"
company_size_match = re.findall(r'\d+', company_size_text.replace('.', ''))

if len(company_size_match) == 2:
    company_size = {
        "start": int(company_size_match[0]),
        "end": int(company_size_match[1])
    }
else:
    company_size = {
        "start": int(company_size_match[0]),
        "end": "null"
    }

#headquarters
headquarters_div = dl_content.find('div', {'data-test-id': headquarters_tag})
headquarters = headquarters_div.find('dd').text.strip() if headquarters_div and headquarters_div.find('dd') else "Not Found"

#organization type
organization_type_div = dl_content.find('div', {'data-test-id': organization_type_tag})
organization_type = organization_type_div.find('dd').text.strip() if organization_type_div and organization_type_div.find('dd') else "Not Found"

#founded on
founded_on_div = dl_content.find('div', {'data-test-id': founded_on_tag})
founded_on = founded_on_div.find('dd').text.strip() if founded_on_div and founded_on_div.find('dd') else "Not Found"

#specialities
specialties_div = dl_content.find('div', {'data-test-id': specialities_tag})
specialties_all = specialties_div.find('dd').text.strip() if specialties_div and specialties_div.find('dd') else "Not Found"

specialties = specialties_all.split(',')
if 've' in specialties[-1]:
    last = specialties.pop().split('ve')
    specialties.extend(last)

#finding location title tag
title_loc = soup.find('h2', class_=title_loc_tag).text.strip() if soup.find('h2', class_=title_loc_tag) else "Not Found"

#finding ul tag
location_list = soup.find('ul', class_=location_list_tag)

#locations
locations = []
if location_list:
    for li in location_list.find_all('li'):
        address_parts = li.find('div').find_all('p')
        address = ' '.join([part.text.strip() for part in address_parts])
        locations.append(address)

#convert to json file
data = {
    "logo_link": logo_url,
    "url": url,
    "slogan": slogan,
    "universal_name": universal_name,
    "name": name,
    "sector": sector,
    "address": address,
    "employee_count": employee_count,
    "employee_count_range": employee_count_range,
    "title": about_title,
    "description": description,
    "website": website,
    "industry": {
        "industry_name": industry_name
        },
    "company_size": company_size,
    "headquarters": headquarters,
    "organization_type": organization_type,
    "founded_on": founded_on,
    "specialties": specialties,
    "locations": locations
}

#printing in json format
json_output = json.dumps(data, ensure_ascii=False, indent=4)
print(json_output)

with open(json_filename, 'w', encoding='utf-8') as json_file:
    json_file.write(json_output)

print(f'Information printed to file "{json_filename}".')


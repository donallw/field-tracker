import requests
import time, datetime
import sys, os
import json
from bs4 import BeautifulSoup

# find set of physics subfields
def get_physics_subfields(url):
    print('Pulling physics subfields...')
    start_time = time.time()
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    dropdown = soup.find('select',{"id": "classification-physics_archives"})
    physics_subfield_codes = []
    for option in dropdown.find_all('option'):
        if option.string != 'all':
            physics_subfield_codes.append(option.string)
    print(f'found {len(physics_subfield_codes)} subfields in {str(round(time.time() - start_time, 3))} seconds.')
    return(physics_subfield_codes)

# collect main arXiv page
def get_field_vals(url, phys_subfields, reg_subfields):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    fields = {}

    # populate fields into dictionary
    for header in soup.find_all('h2'):
        if header.string not in ['quick links', 'About arXiv']:
            fields[header.string] = {}

    for link in soup.find_all('a'):
        subfield_href = link.get('href')
        if subfield_href.find('/list/') >= 0:
            end_main_field = subfield_href.find('.')
            if end_main_field != -1:
                print('\nhref: ',subfield_href)
                end_sub_field = subfield_href.find('/', end_main_field)
                main_field = subfield_href[6:end_main_field]
                try: 
                    rel_field = reg_subfields[main_field]
                except KeyError: # is a physics field 
                    continue
                print(rel_field)
                subfield_code = subfield_href[end_main_field + 1:end_sub_field]
                subfield_value = link.string
                print(f'code : {subfield_code}, subfield: {subfield_value}')
                num_papers = get_num_papers(url + subfield_href[1:])
                fields[rel_field][subfield_value] = num_papers
    return fields
                

def get_num_papers(subfield_url):
    print(f'querying {subfield_url}...')
    subfield_r = requests.get(subfield_url)
    subfield_soup = BeautifulSoup(subfield_r.content, 'html.parser')
    subfield_recent_pubs = ''.join(filter(str.isdigit, subfield_soup.small.contents[0]))
    return subfield_recent_pubs 

# disable printing
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# restore printing
def enablePrint():
    sys.stdout = sys.__stdout__

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'false':
        blockPrint()
        
    # URL's
    arxiv = 'https://arxiv.org/'
    arxiv_adv_search = 'https://arxiv.org/search/advanced'

    physics_subfields = get_physics_subfields(arxiv_adv_search)
    print(f'found fields: {physics_subfields}')

    reg_subfields = {'math' : 'Mathematics', 
                     'cs' : 'Computer Science',
                     'q-bio' : 'Quantitative Biology',
                     'q-fin' : 'Quantitative Finance',
                     'stat' : 'Statistics',
                     'eess' : 'Electrical Engineering and Systems Science',
                     'econ' : 'Economics'}

    fields = get_field_vals(arxiv, physics_subfields, reg_subfields)
    
    fname = 'data/' + datetime.date.today().strftime('%b-%d-%Y') + '.json'
    print(f'Saving to {fname}.')
    with open(fname, 'w') as outfile:
        json.dump(fields, outfile)

    enablePrint()
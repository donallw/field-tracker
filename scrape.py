import requests
import time
import sys, os
import matplotlib.pyplot as plt
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
        
    # # URL's
    # arxiv = 'https://arxiv.org/'
    # arxiv_adv_search = 'https://arxiv.org/search/advanced'

    # physics_subfields = get_physics_subfields(arxiv_adv_search)
    # print(f'found fields: {physics_subfields}')

    # reg_subfields = {'math' : 'Mathematics', 
    #                  'cs' : 'Computer Science',
    #                  'q-bio' : 'Quantitative Biology',
    #                  'q-fin' : 'Quantitative Finance',
    #                  'stat' : 'Statistics',
    #                  'eess' : 'Electrical Engineering and Systems Science',
    #                  'econ' : 'Economics'}

    # fields = get_field_vals(arxiv, physics_subfields, reg_subfields)
    
    test = {'Physics': {}, 'Mathematics': {'Algebraic Geometry': '58', 'Algebraic Topology': '25', 'Analysis of PDEs': '100', 'Category Theory': '13', 'Classical Analysis and ODEs': '25', 'Combinatorics': '71', 'Commutative Algebra': '14', 'Complex Variables': '17', 'Differential Geometry': '49', 'Dynamical Systems': '58', 'Functional Analysis': '39', 'General Mathematics': '9', 'General Topology': '11', 'Geometric Topology': '25', 'Group Theory': '26', 'History and Overview': '6', 'Information Theory': '85', 'K-Theory and Homology': '5', 'Logic': '15', 'Mathematical Physics': '82', 'Metric Geometry': '11', 'Number Theory': '43', 'Numerical Analysis': '71', 'Operator Algebras': '9', 'Optimization and Control': '94', 'Probability': '62', 'Quantum Algebra': '9', 'Representation Theory': '28', 'Rings and Algebras': '24', 'Spectral Theory': '11', 'Statistics Theory': '40', 'Symplectic Geometry': '15'}, 'Computer Science': {'Artificial Intelligence': '428', 'Computation and Language': '347', 'Computational Complexity': '14', 'Computational Engineering, Finance, and Science': '21', 'Computational Geometry': '8', 'Computer Science and Game Theory': '29', 'Computer Vision and Pattern Recognition': '407', 'Computers and Society': '42', 'Cryptography and Security': '88', 'Data Structures and Algorithms': '36', 'Databases': '12', 'Digital Libraries': '8', 'Discrete Mathematics': '17', 'Distributed, Parallel, and Cluster Computing': '54', 'Emerging Technologies': '11', 'Formal Languages and Automata Theory': '10', 'General Literature': '5', 'Graphics': '19', 'Hardware Architecture': '13', 'Human-Computer Interaction': '37', 'Information Retrieval': '53', 'Information Theory': '85', 'Logic in Computer Science': '37', 'Machine Learning': '748', 'Mathematical Software': '5', 'Multiagent Systems': '17', 'Multimedia': '13', 'Networking and Internet Architecture': '37', 'Neural and Evolutionary Computing': '44', 'Numerical Analysis': '71', 'Operating Systems': '7', 'Other Computer Science': '5', 'Performance': '12', 'Programming Languages': '15', 'Robotics': '69', 'Social and Information Networks': '28', 'Software Engineering': '43', 'Sound': '32', 'Symbolic Computation': '5', 'Systems and Control': '87'}, 'Quantitative Biology': {'Biomolecules': '7', 'Cell Behavior': '7', 'Genomics': '7', 'Molecular Networks': '8', 'Neurons and Cognition': '23', 'Other Quantitative Biology': '6', 'Populations and Evolution': '16', 'Quantitative Methods': '19', 'Subcellular Processes': '5', 'Tissues and Organs': '7'}, 'Quantitative Finance': {'Computational Finance': '8', 'Economics': '11', 'General Finance': '4', 'Mathematical Finance': '7', 'Portfolio Management': '7', 'Pricing of Securities': '6', 'Risk Management': '8', 'Statistical Finance': '9', 'Trading and Market Microstructure': '6'}, 'Statistics': {'Applications': '33', 'Computation': '13', 'Machine Learning': '143', 'Methodology': '63', 'Other Statistics': '6', 'Statistics Theory': '40'}, 'Electrical Engineering and Systems Science': {'Audio and Speech Processing': '35', 'Image and Video Processing': '82', 'Signal Processing': '95', 'Systems and Control': '87'}, 'Economics': {'Econometrics': '17', 'General Economics': '10', 'Theoretical Economics': '16'}}

    comp_sci = test['Computer Science']
    print(comp_sci)
    
    labels, values = list(comp_sci.keys()), list(comp_sci.values())

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


    enablePrint()
from bs4 import BeautifulSoup
from collections import OrderedDict
import csv

def parse_tag(tag,data_tag='Code_Summary',message_tag='Messages'):
    """A function for parsing tags read by BeautifulSoup from RCC files"""
    # use case-insensitive match because html parser forces tags to lowercase
    if tag.name.casefold() == data_tag.casefold():
        data = list(csv.DictReader(tag.contents[0].strip().splitlines()))
    elif tag.name.casefold() == message_tag.casefold():
        data = tag.contents[0]
        if data == '\n':
            data = ''
    else:
        data = dict(csv.reader(tag.contents[0].strip().splitlines()))
        # Rename ID to match the lane or sample where applicable.
        if 'ID' in data:
            data[tag.name.split('_')[0].capitalize() + 'ID'] = data['ID']
            data.pop('ID')
    return((tag.name,data))

def parse_rcc_file(file):
    """RCC file parsing function; calls parse_tag on each tag in the file"""
    with open(file) as f:
        soup = BeautifulSoup(f,'html.parser')
    soup = filter(lambda x: x!='\n',soup.contents)
    data = [parse_tag(tag) for tag in soup]
    data = dict(data)
    # Convert the count value from str to float
    counts = dict(
        (d['Name'],float(d.pop('Count'))) for d in data['code_summary']
    )
    genes = data.pop('code_summary')
    sample_data = OrderedDict(
        **data['header'],
        **data['sample_attributes'],
        **data['lane_attributes'],
        **{'messages':data['messages']},
        **counts,
    )
    return(sample_data,genes)
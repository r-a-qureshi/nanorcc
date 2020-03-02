from bs4 import BeautifulSoup
import csv

# def parse_tag(tag):
#     """A function for parsing tags read by BeautifulSoup from RCC files"""
#     return(None,None)

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
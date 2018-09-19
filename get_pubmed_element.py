#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gzip
import sys
import re
import glob
import argparse
import xml.etree.ElementTree as ET


def extract_sentences(in_xml):#, folder):
    tree = ET.parse(gzip.open(in_xml))
    docs = tree.getroot() # get root element
    num = 0 # number of documents
    for doc in docs.findall('.//MedlineCitation'):
        num += 1

        # for list in doc.findall('.//AuthorList'):
        #     name = list.get('LastName')
        #     print(name)

    # tags = [elem.tag for elem in docs.iter()]

        # text = ''
        # authors = [a.text for a in doc.findall('Article/AuthorList/Author/LastName')]
        # print(authors)

        # for article in doc.iter('Author'): # the attributes of 'Author'
        #     print(article.attrib)

    print('Number of documents: ',str(num))

### THESE WORK ###
        # for item in doc.findall('PMID'):
        #     print(item.text)

        # text = ''
        # doc_id = [item.text for item in doc.findall('PMID')][0]
        # print(doc_id)

def argument_parser():
    parser = argparse.ArgumentParser(description="extract sentence and title from pubmed elements")
    parser.add_argument("-i", "--xml_folder", type=str, help="xml folder in gzip format")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = argument_parser()
    for in_xml in glob.glob(args.xml_folder + '*.xml.gz'):
        extract_sentences(in_xml)#, folder_name)

# documents ?
# no affiliation ?
# first author has affiliation ?

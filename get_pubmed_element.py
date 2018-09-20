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

    numDocuments = 0 # number of documents
    numAuthors = 0 # number of authors
    numCollectives = 0 # number of collectives
    numAffiliations = 0 # number of affiliations

    authors = [] # list of authors
    collectives = [] # list of collectives

    for doc in docs.findall('.//MedlineCitation'):
        numDocuments += 1
        # lastnames of the authors:
        # WHAT IF TWO WITH SAME LASTNAME :(
        text = ''
        for a in doc.findall('Article/AuthorList/Author/LastName'):
            if a.text not in authors:
                authors.append(a.text)
                numAuthors += 1

        # collective names:
        for col in doc.findall('Article/AuthorList/Author/CollectiveName'):
            if col.text not in collectives:
                collectives.append(col.text)
                numCollectives += 1

# printing out the results:

    print('Number of documents: ',str(numDocuments))
    print('Number of authors: ',str(numAuthors))
    print('Number of collectives: ',str(numCollectives))

    # print(collectives)

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


        # collectives = [a.text for a in doc.findall('Article/AuthorList/Author/CollectiveName')]
        # if collectives != '':
        #     print(collectives)

        # for list in doc.findall('.//AuthorList'):
        #     name = list.get('LastName')
        #     print(name)

    # tags = [elem.tag for elem in docs.iter()]

        # for article in doc.iter('Author'): # the attributes of 'Author'
        #     print(article.attrib)


            # authors = [a.text for a in doc.findall('Article/AuthorList/Author/LastName')]
            # print(authors)

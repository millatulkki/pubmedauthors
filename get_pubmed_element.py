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
    firstHasAffiliation = [] # when only the first author has affiliation
    noAffiliations = [] # when does not have affiliation at all

    for doc in docs.findall('.//MedlineCitation'):
        numDocuments += 1
        first = 0 # tells when it's time for the first author: after every author is appended by 1

        text = ''

# collect author information from document to tuple:
# (Initials, Lastname, Affiliation)
# append the information to proper list

        for a in doc.findall('Article/AuthorList/'):
            initials = a.find('Initials')
            lastname = a.find('LastName')
            affiliation = a.find('AffiliationInfo/Affiliation')

            # first has to check what information the author list contains
            if isinstance(lastname,ET.Element) and isinstance(initials,ET.Element) and isinstance(affiliation,ET.Element):
                author = (initials.text,lastname.text,affiliation.text)
                authors.append(author)
                #print(author)
                if first == 0: # if author is first one in authorlist
                    firstHasAffiliation.append(author)
                    #print(author)
                first += 1 # shows that next one is not the first author

            elif isinstance(lastname,ET.Element) and isinstance(initials,ET.Element):
                #authors.append((initials.text,lastname.text)) # appends to a list
                author = (initials.text,lastname.text)
                authors.append(author)
                if first == 0:
                    noAffiliations.append(author)
                first += 1
                #print(author)
            elif isinstance(lastname,ET.Element):
                author = lastname.text
                authors.append(author)
                first += 1
                #print(author)

        # collective names:
        for col in doc.findall('Article/AuthorList/Author/CollectiveName'):
            if col.text not in collectives:
                collectives.append(col.text)
                numCollectives += 1

# remove duplicates from lists:
    authors = list(set(authors))
    firstHasAffiliation = list(set(firstHasAffiliation))
    noAffiliations = list(set(noAffiliations))

# printing out the results:
    print('Number of documents: ',str(numDocuments))
    print('Number of authors: ',len(authors))
    print('Number of collectives: ',str(numCollectives))
    print('Only first author has affiliation (nr of documents): ',len(firstHasAffiliation))
    print('No affiliation at all (nr of documents): ',len(noAffiliations))
    # print(collectives)


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

# how to save the info..? author + affiliation + what else?


        # for item in doc.findall('PMID'):
        #     print(item.text)

        # text = ''
        # doc_id = [item.text for item in doc.findall('PMID')][0]
        # print(doc_id)

        # for a in doc.findall('Article/AuthorList/Author/LastName'):
        #     if a.text not in authors:
        #         authors.append(a.text)
        #         numAuthors += 1

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

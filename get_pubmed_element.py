#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gzip
import sys
import re
import glob
import argparse
import xml.etree.ElementTree as ET
import json
import pstats

# { "PMID":
#   {"country": "Countryname",
#   "authorlist":[(Initials,Lastname,Affiliation),],
#   "collectives":[Collective]}
#}


def extract_sentences(in_xml,output_folder):#, folder):
    tree = ET.parse(gzip.open(in_xml))
    docs = tree.getroot() # get root element

    numDocuments = 0 # number of documents
    numAuthors = 0 # number of authors
    numCollectives = 0 # number of collectives
    numAffiliations = 0 # number of affiliations

    firstHasAffiliation = [] # when only the first author has affiliation
    noAffiliations = [] # when does not have affiliation at all

    fullDict = {}


### NEW DOCUMENT STARTS HERE ###
    for doc in docs.findall('.//MedlineCitation'):
        numDocuments += 1
        first = 0 # tells when it's time for the first author: after every author is appended by 1

        text = ''

        id = doc.find('PMID').text
        infoDict = {}
        authors = []
        collectives = []

### collect author information from document to tuple ###
# (Initials, Lastname, Affiliation)
# append the information to proper list

        for a in doc.findall('Article/AuthorList/'):
            initials = a.find('Initials')
            lastname = a.find('LastName')
            affiliation = a.find('AffiliationInfo/Affiliation')


        # first has to check what information the author list contains
            # if has full information, collects it to list
            if isinstance(lastname,ET.Element) and isinstance(initials,ET.Element) and isinstance(affiliation,ET.Element):
                affiliation_list = affiliation.text.split()
                country = affiliation_list[-1]
                author = (initials.text,lastname.text,affiliation.text,country)
                authors.append(author)

                #if first == 0: # if author is first one in authorlist
                    #firstHasAffiliation.append(author)
                #first += 1 # shows that next one is not the first author

            # if has only author initials and lastname, collects it
            elif isinstance(lastname,ET.Element) and isinstance(initials,ET.Element):
                #authors.append((initials.text,lastname.text)) # appends to a list
                author = (initials.text,lastname.text)
                authors.append(author)
                #if first == 0:
                #    noAffiliations.append(author)
                #first += 1

            # if has only lastname, collects it
            elif isinstance(lastname,ET.Element):
                author = lastname.text
                authors.append(author)
                #first += 1

        # collective names:
        for col in doc.findall('Article/AuthorList/Author/CollectiveName'):
            if col.text not in collectives:
                collectives.append(col.text)
                #numCollectives += 1

        # countries:
        for c in doc.findall('MedlineJournalInfo/Country'):
            country = c.text
            infoDict["Country"] = country

#        infoDict["Country"] = country
        infoDict["Collectives"] = collectives
        infoDict["Authors"] = authors

# add full information of document to dictionary:
        fullDict[id] = infoDict

### FEATURES OF DICTIONARY PRINTED OUT
## remove duplicates from lists:
#    authors = list(set(authors))
#    firstHasAffiliation = list(set(firstHasAffiliation))
#    noAffiliations = list(set(noAffiliations))

# printing out the results:
    # print('Number of documents: ',str(numDocuments))
    # print('Number of authors: ',len(authors))
    # print('Number of collectives: ',str(numCollectives))
    # print('Only first author has affiliation (nr of documents): ',len(firstHasAffiliation))
    # print('No affiliation at all (nr of documents): ',len(noAffiliations))
    # print(collectives)

    s = json.dumps(fullDict)
    return s

def argument_parser():
    parser = argparse.ArgumentParser(description="extract sentence and title from pubmed elements")
    parser.add_argument("-i", "--xml_folder", type=str, help="xml folder in gzip format")
    parser.add_argument("-o", "--output_folder", type=str, help="output folder")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = argument_parser()
    print(args.xml_folder)
    for in_xml in glob.glob(args.xml_folder + '*.xml.gz'):
        print(in_xml)
        as_json = in_xml.replace(".xml.gz",".json")
        js = extract_sentences(in_xml,args.output_folder)#, folder_name)
        with open(as_json,"w") as f:
            f.write(js)

        file = os.path.basename(os.path.normpath(in_xml))
        file = file + ".json"

        if not os.path.exists(args.output_folder):
            os.makedirs(args.output_folder)
        with open(os.path.join(args.output_folder,file),"w") as f:
            f.write(js)

### PROFILING ###

    stats = pstats.Stats("profiling_results")
    stats.sort_stats("tottime")
    stats.print_stats(10)

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
    for doc in docs.findall('.//MedlineCitation'):
        text = ''
        doc_id = [item.text for item in doc.findall('PMID')][0]
        print(doc_id)


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

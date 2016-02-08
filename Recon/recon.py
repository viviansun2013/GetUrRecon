from argparse import ArgumentParser
import requests
from lxml import etree
import constants
import json
import pymarc


class MARC:
    """Base class for binary MARC21 record."""
    def __init__(self, args):
        datafile = args.datafile
        queryField = args.queryField

    def matchField(self):
        data = open(self.dataFile, 'rb')
        reader = pymarc.MARCReader(data)
        for record in reader:
            print(record[self.queryField]['a'])


class XMLmetadata:
    """Base class for XML record."""


class JSONmetadata:
    """Base class for JSON (not LD) record."""


class RDFmetadata:
    """Base class for RDF graph."""

#   1. record type assessment
#   2. record feed import
#   3. field parsing
#   4. recon obj prelim creation with fields, query
#   5. recon obj expansion with calls
#   6. present results back
#   7. update records


if __name__ == "__main__":
    parser = ArgumentParser(usage='%(prog)s [options] data_filename')
    parser.add_argument("-f", "--format", dest="format",
                        help="Enter 1: csv, json, jsonld, mrc, nt, ttl, xml")
    parser.add_argument("-m", "--match", dest="match", help="match confidence",
                        default=80)
    parser.add_argument("-q", "--queryField", dest="queryField",
                        help="field to be matched")
    parser.add_argument("-r", "--record", dest="record",
                        help="record delimiter")
    parser.add_argument("-s", "--sparql", dest="sparql",
                        help="sparql endpoint for graph generation")
    parser.add_argument("-t", "--queryType", dest="queryType",
                        help="Enter 1: PersonalName, CorporateName, Name, \
                        Topic, GeographicName, GenreForm, Title")
    parser.add_argument("-u", "--uri", dest="uri", help="resource URI")
    parser.add_argument("datafile", help="metadata file to be matched")

    args = parser.parse_args()
    print(args.datafile)

    if args.datafile and args.queryType == 'PersonalName':
        if args.format == 'csv':
            print('csv')
        elif args.format == 'json':
            print('json')
        elif args.format == 'jsonld':
            print('jsonld')
        elif args.format == 'mrc':
            with open(args.dataFile) as data:
                reader = pymarc.MARCReader(data, to_unicode=True, force_utf8=True)
                for record in reader:
                    rec = MARC(record, args)
                    recordID = rec['001']
                    print(recordID)
        elif args.format == 'nt':
            print('nt')
        elif args.format == 'ttl':
            print('ttl')
        elif args.format == 'xml':
            for event, elem in etree.iterparse(args.datafile):
                if elem.tag == args.record:
                    r = XMLRecord(elem)
                    for entity in elem.iter(args.queryField):
                        reso = r.buildReso()
                        #external calls
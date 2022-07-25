import argparse
import logging
import sys


def run():
    parser = argparse.ArgumentParser(description='Harvest Projects and Dataset information from the ACDH-CH Redmine instance')
    parser.add_argument('--timeout', type=int, default=60, help='HTTP request timeout')
    parser.add_argument('--redmineUrl', default='https://redmine.acdh.oeaw.ac.at')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if args.verbose else logging.INFO)

    redmine = Redmine(args.redmineUrl)
    redmine.harvest()

class Redmine:
    baseUrl = None

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def harvest(self):
        pass

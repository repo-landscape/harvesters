import argparse
import logging
import re
import requests
import sys
import traceback
import yaml
from acdh.resourceCatalog.harvester.Person import Person
from acdh.resourceCatalog.harvester.DatasetInstance import DatasetInstance
from acdh.resourceCatalog.harvester.Dataset import Dataset
from acdh.resourceCatalog.harvester.Project import Project


def run():
    parser = argparse.ArgumentParser(description='Harvest Projects and Dataset information from the ACDH-CH Redmine instance')
    parser.add_argument('--timeout', type=int, default=60, help='HTTP request timeout')
    parser.add_argument('--redmineUrl', default='https://redmine.acdh.oeaw.ac.at')
    parser.add_argument('--queryId', type=int, help='Redmine issues query id. If provided, a given query is used to fetch Redmine issues of tracker "Resource".')
    parser.add_argument('--resourceId', type=int, help='Redmine issues id. If provided, only this resource is being processed (takes precedense over --queryId).')
    parser.add_argument('--limit', type=int, default=999999, help='Limit number of processed Redmine resources. Usefull for testing.')
    parser.add_argument('--resCatUrl', default='https://???')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--dumpTo', help='If provided, dumps the harvested data serialized as yaml into a given file.')
    parser.add_argument('redmineUser')
    parser.add_argument('redminePswd')
    args = parser.parse_args()

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(stream=sys.stdout, format='%(levelname)s:%(asctime)s: %(message)s', level=logging.DEBUG if args.verbose else logging.INFO)

    redmine = Redmine(args.redmineUrl, (args.redmineUser, args.redminePswd))
    data = redmine.harvest(args.limit, args.queryId, args.resourceId)
    logging.info('Creating/updating resource catalog')
    for entities in data.values():
        for entity in entities:
            entity.updateOrCreate(args.resCatUrl)
    #TODO temporary solution - drop dataset instances to a file
    if args.dumpTo is not None:
        with open(args.dumpTo, 'w') as f:
            f.write(yaml.dump(data))

    logging.info('Finished')

class Redmine:
    baseUrl = None
    session = None
    projects = None
    persons = None

    def __init__(self, baseUrl, auth):
        self.baseUrl = baseUrl
        self.session = requests.Session()
        self.session.auth = auth

    def harvest(self, limit=999999, queryId=None, resourceId=None):
        self.projects = {}
        self.persons = {}

        resp = requests.get(f"{self.baseUrl}/trackers.json")
        trackers = resp.json()['trackers']
        trackers = dict(zip([x['name'] for x in trackers], [x['id'] for x in trackers]))

        logging.info('Fetching dataset instance Redmine resources')
        if resourceId is not None:
            issues = [self.session.get(f'{self.baseUrl}/issues/19514.json?include=relations').json()['issue']]
        elif queryId is not None:
            issues = self.getWithPaging(f"{self.baseUrl}/issues.json", {'status_id': '*', 'query_id': queryId}, limit)
        else:
            issues = self.getWithPaging(f"{self.baseUrl}/issues.json", {'status_id': '*', 'tracker_id': trackers['Resource']}, limit)
        logging.info(f'  {len(issues)} issue(s) fetched')

        logging.info('Dropping issues without location_path')
        issues = [x for x in issues if len([y for y in x['custom_fields'] if y['name'] == 'location_path' and y['value'] != '']) > 0]
        logging.info(f'  {len(issues)} valid issue(s) kept')

        logging.info('Finding projects issues belong to')
        for i in issues:
            i['ProjectId'] = self.findProject(i)

        logging.info('Casting issues to resource catalog objects')
        datasets = []
        datasetInstances = []
        for i in issues:
            if i['ProjectId'] is None:
                continue
            try:
                dataset = Dataset.fromRedmine(i, self.getPersonId)
                datasets.append(dataset)
                locationPaths = [x['value'] for x in i['custom_fields'] if x['name'] == 'location_path' and x['value'] != ''][0]
                for locationPath in re.split('[,; \n]', locationPaths):
                    locationPath = locationPath.strip()
                    if locationPath == '':
                        continue
                    try:
                        datasetInstances.append(DatasetInstance.fromRedmine(i, locationPath, dataset.id))
                    except Exception as e:
                        logging.error(str(e))
                        logging.debug(traceback.format_exc())
            except Exception as e:
                logging.error(str(e))
                logging.debug(traceback.format_exc())
        logging.info(f'  {len(datasets)} dataset and {len(datasetInstances)} dataset instance objects created')

        return {
            'persons': list(self.persons.values()),
            'projects': list(self.projects.values()),
            'datasets': datasets,
            'datasetInstances': datasetInstances
        }
    
    def getWithPaging(self, url, param, limit):
        key = re.sub('^.*/([^.]+)[.].*$', '\\1', url)
        param['include'] = 'relations'
        param['limit'] = 1000
        results = []
        while len(results) < limit:
            param['offset'] = len(results)
            logging.debug(f'{url} {param}')
            resp = self.session.get(url, data=param)
            resp = resp.json()
            if len(resp[key]) == 0:
                break
            results += resp[key]
        return results[0:limit]

    def findProject(self, issue):
        parent = issue
        while 'parent' in parent and parent['tracker']['name'] != 'Project':
            if parent["parent"]["id"] in self.projects:
                return parent["parent"]["id"]
            resp = self.session.get(f'{self.baseUrl}/issues/{parent["parent"]["id"]}.json')
            parent = resp.json()['issue']
        if parent['tracker']['name'] == 'Project':
            self.projects[parent['id']] = Project.fromRedmine(parent, self.getPersonId)
            return self.projects[parent['id']].id
    
        if 'relations' not in issue:
            return None
        for rel in [x for x in issue['relations'] if x['relation_type'] == 'relates']:
            id = rel["issue_id"] if rel["issue_id"] != issue['id'] else rel["issue_to_id"]
            if id in self.projects:
                return self.projects[id]
            resp = self.session.get(f'{self.baseUrl}/issues/{id}.json')
            parent = resp.json()['issue']
            if parent['tracker']['name'] == 'Project':
                self.projects[id] = Project.fromRedmine(parent, self.getPersonId)
                return self.projects[id].id
        
        return None

    def getPersonId(self, redmineId):
        if redmineId not in self.persons:
            resp = self.session.get(f"{self.baseUrl}/users/{redmineId}.json")
            self.persons[redmineId] = Person.fromRedmine(resp.json()['user'])
        return self.persons[redmineId].id


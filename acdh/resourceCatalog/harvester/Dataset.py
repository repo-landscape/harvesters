class Dataset:
    N = 0

    @staticmethod
    def fromRedmine(issue, getPersonIdFn):
        Dataset.N += 1

        d = Dataset()
        d.id = Dataset.N
        d.redmineIssueId = issue['id']
        d.projectId = issue['ProjectId']
        d.name = issue['subject']
        d.description = issue['description']
        d.actors = []
        d.actors.append({'role': 'ContactPerson', 'personId': issue['author']['id']})
        if 'assinged_to' in issue:
            d.actors.append({'role': 'DataCurator', 'personId': harverster.getPersonIdFn(issue['assigned_to']['id'])})
        for i in [x for x in issue['custom_fields'] if x['name'] == 'Assignees']:
            for j in i['value']:
                d.actors.append({'role': 'Editor', 'personId': getPersonIdFn(j)})
        return d

    @staticmethod
    def fromResourceCatalog(baseUrl, id):
        #TODO
        pass
    
    id = None
    redmineIssueId = None
    projectId = None
    name = None
    description = None
    actors = None

    def __init__(self):
        pass

    # Updates or creates the dataset instance in the resource catalog
    def updateOrCreate(self, baseUrl):
        #TODO
        pass


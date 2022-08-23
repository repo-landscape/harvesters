class Project:
    N = 0

    @staticmethod
    def fromRedmine(issue, getPersonIdFn):
        Project.N += 1

        d = Project()
        d.id = Project.N
        d.redmineIssueId = issue['id']
        d.name = issue['subject']
        d.startDate = issue['start_date']
        d.endDate = issue['due_date']
        drupalUser = getPersonIdFn(issue['assigned_to']['id'] if 'assinged_to' in issue else issue['author']['id'])
        d.drupalUser = f"user{drupalUser}"
        d.actors = []
        d.actors.append({'role': 'ProjectLeader', 'personId': getPersonIdFn(issue['author']['id'])})
        if 'assinged_to' in issue:
            d.actors.append({'role': 'DataCurator', 'personId': getPersonIdFn(issue['assigned_to']['id'])})
        for i in [x for x in issue['custom_fields'] if x['name'] == 'Assignees']:
            for j in i['value']:
                d.actors.append({'role': 'Editor', 'personId': getPersonIdFn(j)})
        return d

    id = None
    redmineIssueId= None
    name = None
    startDate = None
    endDate = None
    dataSteward = None
    projectLeader = None
    actors = None

    @staticmethod
    def fromResourceCatalog(baseUrl, id):
        #TODO
        pass

    def __init__(self):
        pass

    # Updates or creates the dataset instance in the resource catalog
    def updateOrCreate(self, baseUrl):
        #TODO
        pass


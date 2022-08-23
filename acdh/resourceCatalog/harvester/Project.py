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
        d.projectLeader = issue['author']['id']
        d.actors = []
        if 'assinged_to' in issue:
            d.actors.append({'role': 'DataCurator', 'id': harverster.getPersonId(issue['assigned_to']['id'])})
        for i in [x for x in issue['custom_fields'] if x['name'] == 'Assignees']:
            for j in i['value']:
                d.actors.append({'role': 'Editor', 'id': getPersonIdFn(j)})
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

    def __iter__(self):
        return {
            'id': self.locationPath,
            'redmineIssueId': self.redmineIssueId,
            'name': self.name,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'dataSteward': self.dataSteward,
            'projectLeader': self.projectLeader,
            'actors': self.actors
        }


class DatasetInstance:
    @staticmethod
    def fromRedmine(issue):
        di = DatasetInstance()
        di.locationPath = [x['value'] for x in issue['custom_fields'] if x['name'] == 'location_path' and x['value'] != ''][0]
        di.name = issue['subject']
        di.project = {
            'id': issue['project']['id'], 
            'name': issue['project']['name'],
        }
        di.owner = {
            'id': issue['author']['id'], 
            'identifiers': [{
                'type': 'redmine', 
                'id': f"https://redmine.acdh.oeaw.ac.at/users/{issue['author']['id']}", 
                'label': issue['author']['name']
            }]
        }
        di.contributors = [{
            'id': issue['assigned_to']['id'],
            'identifiers': [{
                'type': 'redmine', 
                'id': f"https://redmine.acdh.oeaw.ac.at/users/{issue['assigned_to']['id']}", 
                'label': issue['assigned_to']['name']
            }]
        }]
        
        return di

    locationPath = None
    name = None
    project = None
    owner = None
    contributors = None

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
            'locationPath': self.locationPath,
            'name': self.name,
            'project': self.project,
            'owner': self.owner,
            'contributors': self.contributors
        }


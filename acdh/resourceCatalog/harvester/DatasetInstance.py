class DatasetInstance:
    @staticmethod
    def fromRedmine(issue):
        di = DatasetInstance()
        di.locationPath = [x['value'] for x in issue['custom_fields'] if x['name'] == 'location_path' and x['value'] != ''][0]
        di.project = issue['Project']['id']
        return di

    locationPath = None
    project = None

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

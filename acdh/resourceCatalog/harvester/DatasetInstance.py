class DatasetInstance:
    N = 0

    @staticmethod
    def fromRedmine(issue, locationPath, datasetId):
        DatasetInstance.N += 1

        d = DatasetInstance()
        d.id = DatasetInstance.N
        d.datasetId = datasetId
        d.locationPath = locationPath
        d.state = 'To be filled in by a harvester'
        return d

    id = None
    datasetId = None
    locationPath = None
    description = None
    state = None

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
            'datasetInstanceId': self.id,
            'datasetId': self.datasetId,
            'locationPath': self.locationPath,
            'description': self.description,
            'state': self.state
        }


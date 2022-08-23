class Person:
    N = 0

    @staticmethod
    def fromRedmine(data):
        Person.N += 1

        d = Person()
        d.id = Person.N
        d.identifiers = [
            {
                'type': 'redmine',
                'id': f"https://redmine.acdh.oeaw.ac.at/users/{data['id']}",
                'label': f"{data['firstname']} {data['lastname']}".strip()
            },
            {
                'type': 'email',
                'id': data['mail'].lower(),
                'label': f"{data['firstname']} {data['lastname']}".strip()
            }
        ]

        return d

    id = None
    identifiers = None

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


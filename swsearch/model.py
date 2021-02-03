import logging
import requests
import json

logger = logging.getLogger(__name__)


def get_resource_class_by_type(resource_type):
    """
    Resources are entries received from ResourceCollections
    {
        "films": "https://swapi.dev/api/films/",
        "people": "https://swapi.dev/api/people/",
        "planets": "https://swapi.dev/api/planets/",
        "species": "https://swapi.dev/api/species/",
        "starships": "https://swapi.dev/api/starships/",
        "vehicles": "https://swapi.dev/api/vehicles/"
    }
    """
    if resource_type == Person.resource_type:
        return Person
    elif resource_type == Film.resource_type:
        return Film
    elif resource_type == Starship.resource_type:
        return Starship
    elif resource_type == Species.resource_type:
        return Species
    elif resource_type == Planet.resource_type:
        return Planet
    elif resource_type == Vechicle.resource_type:
        return Vechicle
    else:
        raise Exception("Unknown Resource Type: {}".format(resource_type))


class ResourceEndpoints:

    def __init__(self, endpoints):
        self.endpoints = endpoints

    def get(self, resource_type):
        return self.endpoints.get(resource_type)

    @classmethod
    def load(cls, data):
        # Setup the endpoints
        endpoints = {}
        for resource_type, url in data.items():
            if resource_type in endpoints:
                logger.warning("ResourceEndpoint already seen: {} in {}".format(resource_type, endpoints))
            endpoints[resource_type] = ResourceEndPoint(resource_type, url)
        return cls(endpoints=endpoints)

    def get_resources_by_url(self, resource_type, url):
        endpoint = self.endpoints[resource_type]
        return endpoint.get_resource_by_url(url)

    def search(self, search_term):
        results = {}
        for resource_type, endpoint in self.endpoints.items():
            results[resource_type] = endpoint.search(search_term=search_term)
        return results


class BasicApi:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.url)

    @staticmethod
    def get(url, params=None):
        logger.debug("Querying: {}".format(url))
        response = requests.get(url, params=params)
        if response.status_code != 200:
            logger.error('Error: {message}'.format(message=response.message()))
            raise Exception('Resource not found: {url}'.format(url=url))
        return json.loads(response.content)


class ResourceEndPoint(BasicApi):

    def __init__(self, resource_type, url, resources=None):
        super().__init__(url)
        self.resource_type = resource_type
        self.resources = resources if resources else {}

    def get_resources(self):
        response = self.get(self.url)
        resources = {}
        next_page = True
        while next_page:
            for result in response["results"]:
                resource = self.load_data_as_resource(result)
                resources[result["url"]] = resource
            next_results = response["next"]
            if next_results:
                response = self.get(next_results)
            else:
                next_page = False
        return resources

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.resource_type)

    def search(self, search_term):
        """
        Searching: Taken from https://swapi.dev/documentation
        All resources support a search parameter that filters the set of resources returned.
        This allows you to make queries like:
        https://swapi.dev/api/people/?search=r2
        All searches will use case-insensitive partial matches on the set of search fields.
        """

        params = {
            'search': search_term
        }
        response = self.get(self.url, params)
        if response is None:
            raise Exception("Received No response from {}".format(self.url))

        resources = []
        for data in response.get('results'):
            resources.append(self.get_as_resource(data=data))
        return resources

    def get_as_resource(self, data):
        url = data["url"]
        if url in self.resources:
            return self.resources[url]

        resource = self.load_data_as_resource(data)
        self.resources[url] = resource
        return resource

    def get_resource_by_url(self, url):
        # import pdb;pdb.set_trace()
        if url in self.resources:
            return self.resources[url]
        data = self.get(url)
        return self.load_data_as_resource(data=data)

    def load_data_as_resource(self, data):
        return get_resource_class_by_type(self.resource_type).load(self.resource_type, data=data)


class Resource:
    resource_type_key = "__resource_type__"

    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def load(cls, resource_type, data):
        if cls.resource_type_key in data:
            raise Exception("Unexpected key {} found in data {}".format(cls.resource_type_key, data))
        data[cls.resource_type_key] = resource_type
        return cls(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.url)


class Film(Resource):
    resource_type = 'films'

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.title)

    def get_associated_people(self, endpoints):
        characters = []
        for c in self.characters:
            characters.append(endpoints.get_resources_by_url(Person.resource_type, c))
        return characters


class Person(Resource):
    resource_type = 'people'

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.name)

    def get_associated_people(self, endpoints):
        return []


class Planet(Resource):
    resource_type = 'planets'

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.name)

    def get_associated_people(self, endpoints):
        residents = []
        for resident in self.residents:
            resident.append(endpoints.get_resources_by_url(Person.resource_type, resident))
        return residents


class Species(Resource):
    resource_type = 'species'

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.name)

    def get_associated_people(self, endpoints):
        people = []
        for p in self.people:
            people.append(endpoints.get_resources_by_url(Person.resource_type, p))
        return people


class Starship(Resource):
    resource_type = 'starships'

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.name)

    def get_associated_people(self, endpoints):
        people = []
        for p in self.pilots:
            people.append(endpoints.get_resources_by_url(Person.resource_type, p))
        return people


class Vechicle(Resource):
    resource_type = 'vehicles'

    def __init__(self, data):
        super().__init__(data)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.name)

    def get_associated_people(self, endpoints):
        people = []
        for p in self.pilots:
            people.append(endpoints.get_resources_by_url(Person.resource_type, p))
        return people

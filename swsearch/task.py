import logging
from swsearch.model import BasicApi, ResourceEndpoints

logger = logging.getLogger(__name__)


def search(config, search_term):
    sw_search = StarWarsSearch.load(config=config)
    result_set = sw_search.search(search_term=search_term)
    results = sw_search.associated_people(items=[r for resources in result_set.values() for r in resources])
    for resource, people in results:
        print("{} -> {}".format(resource, people if people else None))


class StarWarsSearch:

    def __init__(self, endpoints):
        self.endpoints = endpoints

    @classmethod
    def load(cls, config):
        api_root = config.get('swapi', 'api_root')
        # Fetch the api endpoints from the api root
        data = BasicApi.get(api_root)
        endpoints = ResourceEndpoints.load(data)
        return cls(endpoints=endpoints)

    def search(self, search_term):
        logger.debug("Search: search string is \"{}\"".format(search_term))
        search_results = self.endpoints.search(search_term=search_term)
        return search_results

    def associated_people(self, items):
        results = []
        for item in items:
            results.append((item, item.get_associated_people(self.endpoints)))
        return results

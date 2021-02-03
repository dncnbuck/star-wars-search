import unittest
import swsearch.model


class TestModel(unittest.TestCase):

    def setUp(self) -> None:
        self.data = {
            "films": "https://swapi.dev/api/films/",
            "people": "https://swapi.dev/api/people/",
            "planets": "https://swapi.dev/api/planets/",
            "species": "https://swapi.dev/api/species/",
            "starships": "https://swapi.dev/api/starships/",
            "vehicles": "https://swapi.dev/api/vehicles/"
        }
        self.url_response = {
            "https://swapi.dev/api/films/1": {"title": "foo", "characters": ["https://swapi.dev/api/people/1"]},
            "https://swapi.dev/api/people/1": {"name": "foo"},
            "https://swapi.dev/api/planets/1": {"name": "foo", "resident": ["https://swapi.dev/api/people/1"]},
            "https://swapi.dev/api/species/1": {"name": "foo", "people": ["https://swapi.dev/api/people/1"]},
            "https://swapi.dev/api/starships/1": {"name": "foo", "pilot": ["https://swapi.dev/api/people/1"]},
            "https://swapi.dev/api/vehicles/1": {"name": "foo", "pilot": ["https://swapi.dev/api/people/1"]},
            "https://swapi.dev/api/planets/": {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "name": "foo",
                        "residents": [
                            "http://swapi.dev/api/people/1/",
                        ],
                        "films": [
                            "http://swapi.dev/api/films/1/",
                        ],
                        "url": "http://swapi.dev/api/planets/1/"
                    }
                ]
            },
        }

    def mock_get(self, url, params=None):
        return self.url_response.get(url)

    def test_load_endpoints(self):
        endpoints = swsearch.model.ResourceEndpoints.load(data=self.data)
        self.assertTrue(len(endpoints.endpoints), 6)
        self.assertTrue(endpoints.get("films").url, "https://swapi.dev/api/films/")

    def test_load_resources(self):
        endpoints = swsearch.model.ResourceEndpoints.load(data=self.data)

        for resource_type, endpoint in endpoints.endpoints.items():
            endpoint.get = self.mock_get
            repsonse_url = "https://swapi.dev/api/{}/1".format(resource_type)
            resource = endpoints.get_resources_by_url(
                resource_type,
                repsonse_url
            )
            self.assertTrue(resource, self.url_response[repsonse_url])

    def test_search_resources(self):
        endpoints = swsearch.model.ResourceEndpoints.load(data=self.data)

        for resource_type, endpoint in endpoints.endpoints.items():
            endpoint.get = self.mock_get

        result = endpoints.get("planets").search("foo")
        print(result)
        self.assertIsNotNone(result)
        self.assertEquals(len(result), 1)
        self.assertEquals(type(result[0]), swsearch.model.Planet)

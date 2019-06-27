from SWAPI.SWAPI import SWAPI
from pprint import pprint
from enum import Enum
import inspect
import utils

import pytest

class TestSwapi(object):

    # test_obiwanInNewHope,
    THE_PHANTOM_MENACE = 1
    ATTACK_OF_THE_CLONES = 2
    REVENGE_OF_THE_SITH = 3
    A_NEW_HOPE = 4
    THE_EMPIRE_STRIKES_BACK = 5
    RETURN_OF_THE_JEDI = 6
    THE_FORCE_AWAKENS = 7
    THE_LAST_JEDI = 8
    THE_RISE_OF_SKYWALKER = 9

    # test_enterpriseIsAStarship
    ENTERPRISE_IS_A_STARSHIP = 1

    # test_chewbaccaIsAWookie
    EXPECTED_SPECIES_WOOKIE = 'Wookiee'

    #test_verifyStarshipsFields
    EXPECTED_STARSHIP_FIELDS = ['name', 'model', 'crew', 'hyperdrive_rating', 'pilots', 'films']


    # Constants
    RESULTS = 'results'
    SPECIES = 'species'
    COUNT = 'count'
    FILMS = 'films'
    NAME = 'name'
    NEXT = 'next'

    VALUEERROR = "No JSON Object could be decoded."
    KEYERROR = "An incorrect key was used toread the json content."

    @pytest.fixture
    def swapi(self):
        swapi = SWAPI()
        return swapi


#  Tests
    def test_obiwanInNewHope(self, swapi):
        # Assert that Obi-Wan was in the film A New Hope
        person = 'Obi-Wan Kenobi'
        response_obi = swapi.fetchPerson(person)

        films_urls = self.parseFilmUrlsFromPerson(response_obi)

        utils.log("Is Obi-Wan Kenobi in A NEW HOPE? " + str(self.isInFilm(self.A_NEW_HOPE, films_urls)))

        assert self.isInFilm(self.A_NEW_HOPE, films_urls), "Unable to verify that " + person + " is in A New Hope."



    def test_enterpriseIsAStarship(self, swapi):
    #  Assert that the Enterprise is a starship (yes, this should fail)
        starship = 'Enterprise'
        response_enterprise = swapi.fetchStarship(starship)

        utils.logjson(response_enterprise.json())

        number_of_results = self.parseCount(response_enterprise)

        assert number_of_results == self.ENTERPRISE_IS_A_STARSHIP, starship + " is not a starship."


    def test_chewbaccaIsAWookie(self, swapi):
    #  Assert that Chewbacca is a Wookie
        person = 'Chewbacca'
        person_response = swapi.fetchPerson(person)
        utils.logjson(person_response.json())

        species_list = self.parseSpeciesUrlsFromPerson(person_response)
        species_response = swapi.fetchByUrl(species_list[0])
        utils.logjson(species_response.json())

        species_name = self.parseName(species_response)

        assert species_name == self.EXPECTED_SPECIES_WOOKIE

    def test_verifyStarshipsFields(self, swapi):
        #Assert that the /starships endpoint returns the fields below:
        ##name, model, crew, hyperdrive_rating, pilots, films
        utils.log()
        starships_response = swapi.fetchStarships()
        first_result = self.parseResultsZero(starships_response)
        actual_fields = self.parseActualFields(first_result)
        utils.log(str(actual_fields))


        assert self.doesListContainAllElementsOfList(self.EXPECTED_STARSHIP_FIELDS, actual_fields)


    def test_verifyStarshipCount(self, swapi):
    # Assert that the /starships count returned is correct by paging through the results
        utils.log()
        starships_response = swapi.fetchStarships()

        starship_expected_count = self.parseCount(starships_response)
        starship_next_page_url = self.parseNext(starships_response)

        starship_all_results = self.parseResultsAll(starships_response)
        starship_current_count = len(starship_all_results)


        while str(starship_next_page_url) != 'None':
            utils.log("starship_next_page_url " + str(starship_next_page_url))
            starships_response_current = swapi.fetchByUrl(starship_next_page_url)
            starship_next_page_url = self.parseNext(starships_response_current)
            starship_current_count = len(self.parseResultsAll(starships_response_current)) + starship_current_count
            utils.log(str(starship_current_count))


        assert starship_expected_count == starship_current_count, "The starships count is incorrect. " \
                                                                  "The starships count is " + starship_expected_count\
                                                                  + ", but the actual count is " + starship_current_count


    # Parse JSON methods
    def parseActualFields(self, json):
        utils.log()
        actual_fields = []
        try:
            for x in json:
                actual_fields.append(x)

            utils.log('actual keys: ' + str(actual_fields))
            utils.log('actual keys length: ' + str(len(actual_fields)))

            return actual_fields
        except ValueError:
            assert 0, self.VALUEERROR
        except KeyError:
            assert 0, self.KEYERROR

    def parseResultsZero(self, response):
        #Parses json and returns the "results" data.
        try:
            results = response.json()[self.RESULTS][0]
            utils.log("parse Results: ")
            utils.logjson(results)
            return results
        except ValueError:
            assert 0, self.VALUEERROR
        except KeyError:
            assert 0, self.KEYERROR

    def parseResultsAll(self, response):
        utils.log()
        try:
            results = response.json()[self.RESULTS]
            #utils.log("Parse Results All: ")
            #utils.logjson(results)
            return results
        except ValueError:
            assert 0, self.VALUEERROR
        except KeyError:
            assert 0, self.KEYERROR


    def parseName(self, response):
        name = response.json()[self.NAME]
        utils.log(name)
        return name

    def parseSpeciesUrlsFromPerson(self, person_response):
        #Parses json and returns a list of the species urls.
        results = self.parseResultsZero(person_response)
        species = results[self.SPECIES]
        utils.log("Species URLs: ")
        utils.logjson(species)
        return species

    def parseFilmUrlsFromPerson(self, person_response):
        #Parses json and returns a list of film urls.
        results = self.parseResultsZero(person_response)
        films = results[self.FILMS]
        utils.log("Film URLs: ")
        utils.logjson(films)
        return films

    def parseCount(self, response):
        #Parses json for the "count" property which represents the number of results.
        try:
            count = response.json()[self.COUNT]
            utils.log(str(count))
            return int(count)
        except ValueError:
            assert 0, self.VALUEERROR
        except KeyError:
            assert 0, self.KEYERROR

    def parseNext(self, response):
        #Parses the next field which gives the URL for the next page of results.
        try:
            next_page = response.json()[self.NEXT]
            utils.log('next page ' + str(next_page))
            return next_page
        except ValueError:
            assert 0, self.VALUEERROR
        except KeyError:
            assert 0, self.KEYERROR


    # Boolean Functions
    def isInFilm(self, film_to_check, films_urls):
        # Returns True or False if the film in contained in the list of film urls
        utils.log("Film to check: " + str(film_to_check))
        film_numbers = self.extractFilmNumber(films_urls)
        for film in film_numbers:
            if int(film) == film_to_check:
                return True

        return False

    def doesListContainAllElementsOfList(self, small_list, large_list):
        result = all(elem in large_list for elem in small_list)

        return result






#  Other helper methods
    def extractFilmNumber(self, film_urls):
        film_numbers = []

        for film in film_urls:
            end = len(film)
            end_minus_one = end - 1
            end_minus_two = end - 2
            film_number = film[end_minus_two:end_minus_one]
            film_numbers.append(film_number)
        return film_numbers


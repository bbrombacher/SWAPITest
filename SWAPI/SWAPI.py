import requests
import utils


class SWAPI():
    def __init__(self):
        self.base_url = 'https://swapi.co/api/'

        #Test / API Required
        #Done - Assert that Obi-Wan was in the film A New Hope / '/people/id/
        #Done - Assert that the Enterprise is a starship (yes, this should fail)
        #Done - Assert that Chewbacca is a Wookie
        #Done - Assert that the /starships endpoint returns the fields below:
        ##name, model, crew, hyperdrive_rating, pilots, films
        #Done - Assert that the /starships count returned is correct by paging through the results


## Generic API Call

    def fetchByUrl(self, url):
        #Return details from a provided url
        utils.log(url)
        r = requests.get(url)
        return r

##  Film API Calls
    def fetchFilm(self, film):
        #Return a specific film by name
        url = self.base_url + 'films/?search=' + film
        utils.log(url)
        r = requests.get(url)
        return r

    def fetchFilmById(self, id):
        #Return a specific film by film id
        url = self.base_url + 'films/' + id
        utils.log(url)
        r = requests.get(url)
        return r


##  People API Calls
    def fetchPerson(self, person):
        #Return a specific person/character by name.
        url = self.base_url + 'people/?search=' + person
        utils.log(url)
        r = requests.get(url)
        return r

    def fetchPeople(self):
        #Return all people/characters.
        url = self.base_url + 'people/'
        utils.log(url)
        r = requests.get(url)
        return r

    def fetchPeopleSchema(self):
        #Returns the JSON schema of the people endpoint
        url = self.base_url + 'people/schema/'
        utils.log(url)
        r = requests.get(url)
        return r

##  Species API Calls
    def fetchSpeciesById(self, id):
        #Return the species information for a specific species id
        url = self.base_url + 'species/?search=' + id
        utils.log(url)
        r = requests.get(url)
        return r




##  Starship API Calls
    def fetchStarship(self, starship):
        #Return a specific starship
        url = self.base_url + 'starships/?search=' + starship
        utils.log(url)
        r = requests.get(url)
        return r

    def fetchStarships(self):
        #return all starships
        url = self.base_url + 'starships/'
        utils.log(url)
        r = requests.get(url)
        return r




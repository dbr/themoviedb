#!/usr/bin/env python2.5
#encoding:utf-8
#author:dbr/Ben
#project:themoviedb
#forked by ccjensen/Chris
#http://github.com/ccjensen/themoviedb

"""An interface to the themoviedb.org API
"""

__author__ = "dbr/Ben"
__version__ = "0.2b"

config = {}
config['apikey'] = "a8b9f96dde091408a03cb4c78477bd14"

config['urls'] = {}
config['urls']['movie.search'] = "http://api.themoviedb.org/2.1/Movie.search/en/xml/%(apikey)s/%%s" % (config)
config['urls']['movie.getInfo'] = "http://api.themoviedb.org/2.1/Movie.getInfo/en/xml/%(apikey)s/%%s" % (config)

import urllib

import xml.etree.cElementTree as ElementTree

from collections import defaultdict 

class TmdBaseError(Exception): pass
class TmdHttpError(TmdBaseError): pass
class TmdXmlError(TmdBaseError): pass

class XmlHandler:
    """Deals with retrieval of XML files from API
    """
    def __init__(self, url):
        self.url = url

    def _grabUrl(self, url):
        try:
            urlhandle = urllib.urlopen(url)
        except IOError, errormsg:
            raise TmdHttpError(errormsg)
        return urlhandle.read()

    def getEt(self):
        xml = self._grabUrl(self.url)
        try:
            et = ElementTree.fromstring(xml)
        except SyntaxError, errormsg:
            raise TmdXmlError(errormsg)
        return et

class recursivedefaultdict(defaultdict): 
    def __init__(self): 
        self.default_factory = type(self)

class SearchResults(list):
    """Stores a list of Movie's that matched the search
    """
    def __repr__(self):
        return "<Search results: %s>" % (list.__repr__(self))

class MovieResult(dict):
    """A dict containing the information about a specific search result
    """
    def __repr__(self):
        return "<MovieResult: %s (%s)>" % (self.get("name"), self.get("released"))


class Movie(dict):
    """A dict containing the information about the film
    """
    def __repr__(self):
        return "<MovieResult: %s (%s)>" % (self.get("name"), self.get("released"))

class Categories(recursivedefaultdict):
    """Stores category information
    """
    def set(self, category_et):
        """Takes an elementtree Element ('category') and stores the url,
        using the type and name as the dict key.
        
        For example:
       <category type="genre" url="http://themoviedb.org/encyclopedia/category/80" name="Crime"/> 
        
        ..becomes:
        categories['genre']['Crime'] = 'http://themoviedb.org/encyclopedia/category/80'
        """
        _type = category_et.get("type")
        name = category_et.get("name")
        url = category_et.get("url")
        self[_type][name] = url

class Studios(recursivedefaultdict):
    """Stores category information
    """
    def set(self, studio_et):
        """Takes an elementtree Element ('studio') and stores the url,
        using the name as the dict key.
        
        For example:
       <studio url="http://www.themoviedb.org/encyclopedia/company/20" name="Miramax Films"/> 
        
        ..becomes:
        studios['name'] = 'http://www.themoviedb.org/encyclopedia/company/20'
        """
        name = studio_et.get("name")
        url = studio_et.get("url")
        self[name] = url

class Countries(recursivedefaultdict):
    """Stores country information
    """
    def set(self, country_et):
        """Takes an elementtree Element ('country') and stores the url,
        using the name and code as the dict key.
        
        For example:
       <country url="http://www.themoviedb.org/encyclopedia/country/223" name="United States of America" code="US"/> 
        
        ..becomes:
        countries['code']['name'] = 'http://www.themoviedb.org/encyclopedia/country/223'
        """
        code = country_et.get("code")
        name = country_et.get("name")
        url = country_et.get("url")
        self[code][name] = url

class Images(recursivedefaultdict):
    """Stores image information
    """
    def set(self, image_et):
        """Takes an elementtree Element ('image') and stores the url,
        using the type, id and size as the dict key.
        
        For example:
       <image type="poster" size="original" url="http://images.themoviedb.org/posters/4181/67926_sin-city-02-color_122_207lo.jpg" id="4181"/> 
        
        ..becomes:
        images['poster']['4181']['original'] = 'http://images.themoviedb.org/posters/4181/67926_sin-city-02-color_122_207lo.jpg'
        """
        _type = image_et.get("type")
        _id = image_et.get("id")
        size = image_et.get("size")
        url = image_et.get("url")
        self[_type][_id][size] = url

    def __repr__(self):
        return "<%s with %s posters and %s backdrops>" % (
            self.__class__.__name__, 
            len(self['poster'].keys()), 
            len(self['backdrop'].keys())
        )

    def largest(self, _type, _id):
        """Attempts to return largest image of a specific type and id
        """
        if(isinstance(_id, int)):
            _id = str(_id)
        for cur_size in ["original", "mid", "cover", "thumb"]:
            for size in self[_type][_id]:
            	if cur_size in size:
                	return self[_type][_id][cur_size]

class Cast(recursivedefaultdict):
    """Stores cast information
    """
    def set(self, person_et):
        """Takes an elementtree Element ('person') and stores the information as a Person,
        using the job and id as the dict key.
        
        For example:
       <person url="http://www.themoviedb.org/person/2293" name="Frank Miller" job="Director" character="" id="2293"/>
        
        ..becomes:
        people['Director']['2293'] = Person
        people['Director']['2293']['name'] = 'Frank Miller'
        """
        job = person_et.get("job")
        _id = person_et.get("id")
        name = person_et.get("name")
        character = person_et.get("character")
        url = person_et.get("url")
        self[job][_id] = Person(job, _id, name, character, url)

class Person(dict):
    """Stores information about a specific person"""
    def __init__(self, job, _id, name, character, url):
        self['job'] = job
        self['id'] = _id
        self['name'] = name
        self['character'] = character
        self['url'] = url

class MovieDb:
    """Main interface to www.themoviedb.com

    The search() method searches for the film by title.
    The getMovieInfo() method retrieves information about a specific movie using themoviedb id.
    """
    def _parseSearchResults(self, movie_element):
        cur_movie = MovieResult()
        cur_images = Images()
        for item in movie_element.getchildren():
                if item.tag.lower() == "images":
                    for subitem in item.getchildren():
                        cur_images.set(subitem)
                else:
                    cur_movie[item.tag] = item.text
        cur_movie['images'] = cur_images
        return cur_movie

    def _parseMovie(self, movie_element):
        cur_movie = Movie()
        cur_categories = Categories()
        cur_studios = Studios()
        cur_countries = Countries()
        cur_images = Images()
        cur_cast = Cast()
        for item in movie_element.getchildren():
            if item.tag.lower() == "categories":
                for subitem in item.getchildren():
                    cur_categories.set(subitem)
            elif item.tag.lower() == "studios":
                for subitem in item.getchildren():
                    cur_studios.set(subitem)
            elif item.tag.lower() == "countries":
                for subitem in item.getchildren():
                    cur_countries.set(subitem)
            elif item.tag.lower() == "images":
                for subitem in item.getchildren():
                    cur_images.set(subitem)
            elif item.tag.lower() == "cast":
                for subitem in item.getchildren():
                    cur_cast.set(subitem)
            else:
                cur_movie[item.tag] = item.text

        cur_movie['categories'] = cur_categories
        cur_movie['studios'] = cur_studios
        cur_movie['countries'] = cur_countries
        cur_movie['images'] = cur_images
        cur_movie['cast'] = cur_cast
        return cur_movie

    def search(self, title):
        """Searches for a film by its title.
        Returns SearchResults (a list) containing all matches (Movie instances)
        """
        title = urllib.quote(title.encode("utf-8"))
        url = config['urls']['movie.search'] % (title)
        etree = XmlHandler(url).getEt()
        search_results = SearchResults()
        for cur_result in etree.find("movies").findall("movie"):
            cur_movie = self._parseSearchResults(cur_result)
            search_results.append(cur_movie)
        return search_results

    def getMovieInfo(self, id):
        """Returns movie info by from its tmdb id.
        Returns a Movie instance
        """
        url = config['urls']['movie.getInfo'] % (id)
        etree = XmlHandler(url).getEt()
        return self._parseMovie(etree.find("movies").findall("movie")[0])


def search(name = None):
    """Convenience wrapper for MovieDb.search - so you can do..

    >>> import tmdb
    >>> tmdb.search("Fight Club")
    <Search results: [<MovieResult: Fight Club>]>
    """
    mdb = MovieDb()
    return mdb.search(name)

def getMovieInfo(id = None):
    """Convenience wrapper for MovieDb.search - so you can do..

    >>> import tmdb
    >>> tmdb.getMovieInfo(187)
    <Search results: [<Movie: Fight Club>]>
    """
    mdb = MovieDb()
    return mdb.getMovieInfo(id)

def main():
    results = search("Fight Club")
    searchResult = results[0]
    movie = getMovieInfo(searchResult['id'])
    print movie['name']
    print movie['cast']['Producer']['7474']['name']
    print movie['images']
    for genreName in movie['categories']['genre']:
        print "%s (%s)" % (genreName, movie['categories']['genre'][genreName])
    

if __name__ == '__main__':
    main()
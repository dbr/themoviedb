#!/usr/bin/env python2.5
#encoding:utf-8
#author:dbr/Ben
#project:themoviedb

import unittest

import tmdb

class test_search(unittest.TestCase):
    def setUp(self):
        self.m = tmdb.MovieDb()

    def test_simple_search(self):
        """Simple test search
        """
        self.assertEquals(
            type(
                self.m.search("Fight Club")
            ),
            tmdb.SearchResults
        )

    def test_search_results(self):
        """Check SearchResults are usable
        """
        results = self.m.search("Fight Club")
        first_result = results[0]

        self.assertEquals(
            type(first_result),
            tmdb.Movie
        )

        self.assertEquals(
            first_result['title'],
            'Fight Club'
        )

        self.assertEquals(
            first_result['release'],
            '1999-09-16'
        )

        self.assertEquals(
            first_result['imdb'],
            'tt0137523'
        )

class test_wrappers(unittest.TestCase):
    def test_search_wrapper(self):
        """Tests tmdb.search() wrapper works correctly
        """
        r = tmdb.search("The Matrix")
        self.assertEquals(
            type(r),
            tmdb.SearchResults
        )

class test_artwork(unittest.TestCase):
    def setUp(self):
        self.film = tmdb.MovieDb().search("Fight Club")[0]

    def test_poster_urls(self):
        """Checks posters are valid looking URLs
        """
        for size, url in self.film['poster'].items():
            self.assertTrue(
                url.startswith("http://")
            )

    def test_backdrop_urls(self):
        """Checks backdrop images are valid looking URLs
        """
        for size, url in self.film['backdrop'].items():
            self.assertTrue(
                url.startswith("http://")
            )

    def test_artwork_repr(self):
        """Checks artwork repr looks sensible
        """
        self.assertTrue(
            repr(self.film['poster']).startswith(
                "<Poster with sizes "
            )
        )


if __name__ == '__main__':
    unittest.main()
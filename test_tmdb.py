#!/usr/bin/env python2.5
#encoding:utf-8
#author:dbr/Ben
#project:themoviedb
#repository:http://github.com/dbr/tvdb_api
#license: LGPLv2 http://www.gnu.org/licenses/lgpl.html

import tmdb


def test_simple_search():
    """Simple test search
    """
    t = tmdb.MovieDb()
    sr = t.search("Fight Club")
    assert isinstance(sr, tmdb.SearchResults)
    assert sr[0]['name'] == "Fight Club"


def test_search_results():
    """Check SearchResults are usable
    """
    t = tmdb.MovieDb()
    results = t.search("Fight Club")
    first_result = results[0]

    assert isinstance(first_result, tmdb.MovieResult)

    assert first_result['name'] == 'Fight Club'

    assert first_result['released'] == '1999-09-16'

    assert first_result['imdb_id'] == 'tt0137523'


def test_info_from_search():
    """Get info from first search result
    """
    t = tmdb.MovieDb()
    results = t.search("Fight Club")
    first_result = results[0]
    info = first_result.info()
    assert info['name'] == "Fight Club"


def test_search_to_info():
    """Gets a movie ID via search helper, then calls getMovieInfo using this
    """
    sr = tmdb.search("fight club")[0]
    movie = tmdb.getMovieInfo(sr['id'])
    assert sr['name'] == movie['name']


def test_get_director():
    """Checks you can get the director of a film
    """
    mid = tmdb.search("Inglourious Basterds")[0]['id']
    movie = tmdb.getMovieInfo(mid)

    assert len(movie['cast']['director']) == 1
    assert movie['cast']['director'][0]['name'] == "Quentin Tarantino"


def test_search_wrapper():
    """Tests tmdb.search() wrapper works correctly
    """
    r = tmdb.search("The Matrix")
    assert isinstance(r, tmdb.SearchResults)


def test_getmovieinfo_wrapper():
    """Tests tmdb.getMovieInfo() wrapper works correctly
    """
    r = tmdb.getMovieInfo(550)
    assert isinstance(r, tmdb.Movie)


def test_artwork_generator():
    """Generates several tests posters/backdrops

    Uses test generator to prevent multiple requests for the movie info
    """
    filmId = tmdb.MovieDb().search("Fight Club")[0]['id']
    film = tmdb.MovieDb().getMovieInfo(filmId)

    def test_poster_urls():
        """Checks posters are valid looking URLs
        """
        for poster in film['images'].posters:
            for key, value in poster.items():
                if key not in ['id', 'type']:
                    assert value.startswith("http://")

    yield test_poster_urls

    def test_backdrop_urls():
        """Checks backdrop images are valid looking URLs
        """
        for poster in film['images'].posters:
            for key, value in poster.items():
                if key not in ['id', 'type']:
                    assert value.startswith("http://")

    yield test_backdrop_urls

    def test_artwork_repr():
        """Checks artwork repr looks sensible
        """
        poster_repr = repr(film['images'].posters[0])
        assert poster_repr.startswith("<Image (poster for ID")

        backdrop_repr = repr(film['images'].backdrops[0])
        assert backdrop_repr.startswith("<Image (backdrop for ID")

    yield test_artwork_repr

    def test_posters():
        """Check retrieving largest artwork
        """
        assert len(film['images'].posters) > 1
        assert len(film['images'].backdrops) > 1
        print film['images'].posters[0]['cover']
        url = film['images'].posters[0]['cover']
        assert url.startswith('http://hwcdn.themoviedb.org/posters/')
        assert url.endswith('/fight-club-cover.jpg')

    yield test_posters


def test_mediagetinfo():
    """Tests searching by file hash
    """
    t = tmdb.MovieDb()
    films = t.mediaGetInfo(hash = '907172e7fe51ba57', size = 742086656)
    film = films[0]
    print film['name']
    assert film['name'] == 'Sin City'


if __name__ == '__main__':
    unittest.main()
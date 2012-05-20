#!/usr/bin/env python2

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

    assert first_result['released'] == '1999-10-15'

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

def test_get_movie_from_imdb():
    """Checks that a movie can be retrieved via its IMDb ID
    """
    movie = tmdb.getMovieInfo('tt0079023')

    assert len(movie['cast']['director']) == 2
    assert movie['cast']['director'][0]['name'] == "Jean-Marie Straub"
    print repr(movie['cast']['director'][1]['name'])
    assert movie['cast']['director'][1]['name'] == u"Dani\xe8le Huillet"


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
        assert url.startswith('http://')
        assert url.endswith('.jpg')

    yield test_posters


def test_mediagetinfo():
    """Tests searching by file hash
    """

    import nose
    raise nose.SkipTest("Finding reliable hash to test with is difficult..")

    t = tmdb.MovieDb()
    films = t.mediaGetInfo(hash = '907172e7fe51ba57', size = 742086656)
    film = films[0]
    print film['name']
    assert film['name'] == 'Sin City'


def test_castthumbnails():
    """Tests actors have thumbnails
    """
    t = tmdb.MovieDb()
    film = t.getMovieInfo(950)
    assert film['cast']['actor'][0].has_key('thumb')
    assert film['cast']['actor'][0]['thumb'].startswith('http://')

def test_doctest():
    import doctest
    doctest.testmod(tmdb, raise_on_error = True)


if __name__ == '__main__':
    import nose
    nose.main()

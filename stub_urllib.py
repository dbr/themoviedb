"""Stub themoviedb.org API, for use before API key was received
"""

template = {}
template['search'] = """<results for="%(title)s">
<Query searchTerms="%(title)s"/>
<totalResults>1</totalResults>
<moviematches>
    <movie>
        <score>1.0</score>
        <popularity>12</popularity>
        <title>%(title)s</title>
        <type>movie</type>
        <id>1858</id>
        <imdb>tt0418279</imdb>
        <url>http://www.themoviedb.org/movie/1858</url>
        <short_overview>2007 film based based on...</short_overview>
        <release>2007-07-04</release>
        <poster size="original">http://www.example.com/poster_original.jpg</poster>
        <poster size="thumb">http://www.example.com/poster_thumb.jpg</poster>
        <poster size="mid">http://www.example.com/poster_mid.jpg</poster>
        <poster size="cover">http://www.example.com/poster_cover.jpg</poster>
        <backdrop size="original">http://www.example.com/backdrop_original.jpg</backdrop>
        <backdrop size="thumb">http://www.example.com/backdrop_thumb.jpg</backdrop>
        <backdrop size="mid">http://www.example.com/backdrop_mid.jpg</backdrop>
    </movie>
</moviematches>
</results>"""

class stub_urllib:
    from StringIO import StringIO
    import re
    def urlopen(self, url):
        if url.startswith("http://api.themoviedb.org/2.0/Movie.search"):
            r = self.re.findall("\?title=(.+)&", url)
            title = r[0]
            retxml = template['search'] % {'title': title}
            return self.StringIO(retxml)
        raise IOError("Stub cannot handle %s" % (url))

from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper('http://localhost:3030/books/')


def get_books(genre):
    query = _get_books_by_genre(genre)

    response = _execute_query(query)

    for result in response:
        print(result["name"]["value"])
    return True


def get_recommendations(read_books):
    genres = []
    writers = []
    publishers = []

    for book in read_books:
        ret_val = _get_book_details(book)

        for item in ret_val[0]:
            if item not in genres:
                genres.append(item)

        for item in ret_val[1]:
            if item not in writers:
                writers.append(item)

        for item in ret_val[2]:
            if item not in publishers:
                publishers.append(item)

    names = []
    for genre in genres:
        names = names + _get_books_by_genre(genre)

    for writer in writers:
        names = names + _get_books_by_writer(writer)

    for publisher in publishers:
        names = names + _get_books_by_publisher(publisher)

    recommended = _remove_read_books(_get_book_names(names), read_books)

    _print_sorted_dictionary(recommended)


def _remove_read_books(recommended, read_books):
    for read_book in read_books:
        del recommended[read_book]
    return recommended


def _get_book_names(names):
    recommended = {}
    for dictionary_name in names:
        for name in dictionary_name.values():
            str_name = name.values()[1]
            if str_name in recommended:
                recommended[str_name] = recommended[str_name] + 1
            else:
                recommended[str_name] = 1
    return recommended


def _print_sorted_dictionary(recommended):
    sorted_books = sorted(recommended.iteritems(), key=lambda x: int(x[1]), reverse=True)
    for book in sorted_books:
        print book


def _get_book_details(book_name):
    query = _get_genre_writer_publisher(book_name)

    response = _execute_query(query)

    genres = []
    writers = []
    publishers = []
    for result in response:
        genres.append(result["genre"]["value"])
        writers.append(result["writer"]["value"])
        publishers.append(result["publisher"]["value"])

    return genres, writers, publishers


def _execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    return response['results']['bindings']


def _get_genres():
    return """
    PREFIX uni1: <http://www.semanticweb.org/mardej/ontologies/2019/6/untitled-ontology-7#>
    SELECT ?name 
    WHERE {{ 
        ?genre a uni1:Genre . ?genre uni1:name ?name .
    }}
    """


def _get_books_by_writer(writer):
    query = """
    PREFIX uni1: <http://www.semanticweb.org/mardej/ontologies/2019/6/untitled-ontology-7#>
    SELECT ?name 
    WHERE {{ 
    ?book a uni1:Book . ?book uni1:title ?name .
    ?book  uni1:hasWriter ?writer . 
    FILTER(str(?writer) = "{writer_film}")
    }}
    """.format(writer_film=writer)
    return _execute_query(query)


def _get_books_by_publisher(publisher):
    query = """
    PREFIX uni1: <http://www.semanticweb.org/mardej/ontologies/2019/6/untitled-ontology-7#>
    SELECT ?name 
    WHERE {{ 
    ?book a uni1:Book . ?book uni1:title ?name .
    ?book  uni1:hasPublisher ?publisher . 
    FILTER(str(?publisher) = "{publisher_film}")
    }}
    """.format(publisher_film=publisher)
    return _execute_query(query)


def _get_books_by_genre(genre):
    query = """
    PREFIX uni1: <http://www.semanticweb.org/mardej/ontologies/2019/6/untitled-ontology-7#>
    SELECT ?name 
    WHERE {{ 
    ?book a uni1:Book . ?book uni1:title ?name .
    ?book  uni1:hasGenre ?genre . 
    FILTER(str(?genre) = "{genre_film}")
    }}
    """.format(genre_film=genre)
    return _execute_query(query)


def _get_genre_writer_publisher(book):
    return """
    PREFIX uni1: <http://www.semanticweb.org/mardej/ontologies/2019/6/untitled-ontology-7#>
        SELECT ?genre ?writer ?publisher
        WHERE {{
          ?book  uni1:hasGenre ?genre .
          ?book  uni1:hasWriter ?writer .
          ?book  uni1:hasPublisher ?publisher .
          ?book uni1:title ?nameBook .
            FILTER(str(?nameBook) = '{book_name}')
        }}
    """.format(book_name=book)



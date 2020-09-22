import csv
from collections import defaultdict, namedtuple
from statistics import mean

MOVIE_DATA = "movie_metadata.csv"
NUM_TOP_DIRECTORS = 21
MIN_MOVIES = 4
MIN_YEAR = 1960

Movie = namedtuple('Movie', 'title year score')
MoviesRatings = namedtuple('Movies', 'info avg')


def get_movies_by_director():
    '''Extracts all movies from csv and stores them in a dictionary
    where keys are directors, and values is a list of movies (named tuples)'''
    # Read the CSV File
    directors = defaultdict(list)

    with open(MOVIE_DATA) as movie_file:
        for row in csv.DictReader(movie_file):
                try:
                    Movie = namedtuple('Movie', 'title year score')
                    Movie.title = row['movie_title']
                    Movie.year = int(row['title_year'])
                    Movie.score = float(row['imdb_score'])
                    director = row['director_name']                
                except ValueError:
                    continue
                if Movie.year >= MIN_YEAR:
                    directors[director].append(Movie)
    return directors


def get_average_scores(directors):
    top_directors = defaultdict(list)
    '''Filter directors with < MIN_MOVIES and calculate averge score'''
    for director, movies in directors.items():
        if len(movies) >= MIN_MOVIES:
            top_directors[director].append(MoviesRatings(info= movies, avg=_calc_mean(movies)))
    return top_directors


def _calc_mean(movies):
    '''Helper method to calculate mean of list of Movie namedtuples'''
    return mean([ movie.score for movie in movies])


def print_results(directors):
    '''Print directors ordered by highest average rating. For each director
    print his/her movies also ordered by highest rated movie.
    See http://pybit.es/codechallenge13.html for example output'''
    fmt_director_entry = '{counter}. {director:<52} {avg}'
    fmt_movie_entry = '[{year}] {title:<50} {score}'
    sep_line = '-' * 60
    counter = 1

    for director, info in sorted(directors.items(), key=lambda x: x[1][0].avg, reverse=True):
        if counter < NUM_TOP_DIRECTORS:
            print(fmt_director_entry.format(counter=counter, director=director,
                                            avg=info[0].avg))
            print(sep_line)
            for movie in info:
                for item in movie[0]:
                    print(fmt_movie_entry.format(year=item.year,
                                                 title=item.title,
                                                 score=item.score))
            counter += 1
            print(sep_line)
        


def main():
    '''This is a template, feel free to structure your code differently.
    We wrote some tests based on our solution: test_directors.py'''
    directors = get_movies_by_director()
    directors = get_average_scores(directors)
    print_results(directors)


if __name__ == '__main__':
    main()
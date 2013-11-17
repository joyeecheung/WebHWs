"""Items passed to templates."""

import os.path
import glob

class MovieInfo(object):
    """Basic information about a movie.

    Fields:
    title -- title of the movie
    year -- release year
    rating -- overall rating
    total -- total number of reviews of the movie
    dirname -- the name of the directory where files of the movie are placed

    """
    def __init__(self, filepath):
        info_file = open(os.path.join(filepath, 'info.txt'))
        (self.title, self.year, self.rating,
            self.total) = info_file.read().splitlines()
        self.dirname = filepath.split(os.sep)[-1]

class ReviewItem(object):
    """Individual reviews of a movie.

    Fields:
    quote -- review quotes
    rating -- general rating: FRESH or ROTTEN
    reviewer -- name of the reviewer
    company -- company the reviewer belongs to, could be an empty string

    """
    def __init__(self, quote, rating, reviewer, company):
        self.quote = quote
        self.rating = rating
        self.reviewer = reviewer
        self.company = company

class Reviews(object):
    """Review information about a movie.

    Fields:
    firstHalf -- list of first half of the reviews,
                             which will be displayed in left column
    secondHalf -- list of second half of the reviews,
                             which will be displayed in right column
    count -- number of reviews

    """
    def __init__(self, filepath):
        self.first_half = []
        self.second_half = []

        # search for review files
        review_file_names = glob.glob(
            os.path.join(filepath, 'review[0-9]*.txt'))
        self.count = len(review_file_names)
        review_file_names.sort()

        for i in range(self.count):
            review_file = open(review_file_names[i])
            (quote, rating, reviewer,
                company) = review_file.read().splitlines()
            item = ReviewItem(quote, rating, reviewer, company)
            # split reviews into two halves
            if i < self.count / 2:
                self.first_half.append(item)
            else:
                self.second_half.append(item)

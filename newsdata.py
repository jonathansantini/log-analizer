#!/usr/bin/env python3
#
# Log analyizer tool used to determine most popular articles, authors and
#   days where errors are over 1%.

import psycopg2

from flask import Flask

app = Flask(__name__)


def queryDatabase(query):
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(query)
    DATA = c.fetchall()
    db.close()
    return DATA


def get_popular_articles():
    query = '''
        SELECT articles.title, count(log.path)
        AS views FROM articles
        LEFT JOIN log ON log.path LIKE concat('%', articles.slug)
        GROUP BY articles.title
        ORDER BY views DESC
        LIMIT 3;
    '''
    results = queryDatabase(query)
    print("\nWhat are the most popular three articles of all time?\n")
    entry = '"%s" -- %s views\n'
    pop_articles = "".join(entry % (title, count) for title, count in results)
    print(pop_articles)


def get_popular_authors():
    query = '''
        SELECT authors.name, count(*) AS views
        FROM authors
        LEFT JOIN articles ON authors.id = articles.author
        LEFT JOIN log ON log.path LIKE concat('%', articles.slug)
        GROUP BY authors.name
        ORDER BY views DESC;
    '''
    results = queryDatabase(query)
    print("\nWho are the most popular article authors of all time?\n")
    entry = '%s -- %s views\n'
    pop_authors = "".join(entry % (author, count) for author, count in results)
    print(pop_authors)


def get_dates_with_errors():
    query = '''
        SELECT requests.time, (
            (errors.error_count * 100.0 / requests.count)
        )
        AS percent
        FROM (
            SELECT to_char(time, 'MM/DD/yyyy') AS time, count(*) AS error_count
            FROM log WHERE status LIKE '%404%'
            GROUP BY to_char(time, 'MM/DD/yyyy')
        ) AS errors
        JOIN (
            SELECT to_char(time, 'MM/DD/yyyy') AS time, count(*) AS count
            FROM log
            GROUP BY to_char(time, 'MM/DD/yyyy')
        ) as requests
        ON errors.time = requests.time
        WHERE (
            (errors.error_count * 100.0 / requests.count) > 1.0
        )
        ORDER BY percent DESC;
    '''
    results = queryDatabase(query)
    print("\nOn which days did more than 1% of requests lead to errors?\n")
    entry = '%s -- %s views\n'
    error_dates = "".join(entry % (date, count) for date, count in results)
    print(error_dates)


if __name__ == '__main__':
    get_popular_articles()
    get_popular_authors()
    get_dates_with_errors()

# Log analyzer

This is the repo for the log analyzer project for Udacity's Full Stack Nanocourse using python and sql.

It uses a set of queries to determine most popular articles, most popular authors and days with a high amount of errors.

## The view the project

This project makes use of the same Linux-based virtual machine (VM) but you can install this locally using python and sql.

### Install data file

If you'd like to view this project on your own, install the following data file.

https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

### Install python dependancies

```
pip3 install --upgrade pip
pip3 install flask packaging oauth2client flask-httpauth
pip3 install sqlalchemy flask-sqlalchemy psycopg2-binary pycodestyle
```

### Run the script

Once dependancies are installed, run the following command.

```
$ python3 newsdata.py
```

You should see a set of three queries run answering what are the most popular articles, most popular
authors and the days where errors for the site were above 1%.

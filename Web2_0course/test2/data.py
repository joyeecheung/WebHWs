#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from collections import namedtuple
import os.path

def get_comments():
    """Retrieve comments from local database."""
    conn = pymongo.Connection("localhost",27017)
    db = conn["paperDB"]
    infoDB = db.infoDB
    record = infoDB.find_one()
    return record['comment']

def get_blog():
    """Retrieve a blog from local database."""
    conn = pymongo.Connection("localhost",27017)
    db = conn["paperDB"]
    infoDB = db.infoDB
    record = infoDB.find_one()

    del record['_id']
    del record['comment']  # reserve space

    # Since there's only one blog per page, use namedtuple
    blog = namedtuple('Blog', record.keys())(*record.values())
    print "Blog loaded."
    return blog

def get_users():
    """Retrieve the user list from local database."""
    conn = pymongo.Connection("localhost",27017)
    db = conn["paperDB"]
    userRecords = db.users

    users = dict()
    for user in userRecords.find():
        users[user['user']] = user['password']

    print "%d users loaded." % (len(users))
    return users

def save_comment(newComment):
    """Save a new comment to local database."""
    conn = pymongo.Connection("localhost",27017)
    db = conn["paperDB"]
    infoDB = db.infoDB
    record = infoDB.find_one()

    record['comment'].append(newComment)
    infoDB.save(record)
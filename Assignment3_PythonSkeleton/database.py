#!/usr/bin/env python3

from modules import pg8000
import configparser
import json

#####################################################
##  Database Connect
#####################################################

'''
Connects to the database using the connection string
'''
def database_connect():
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as e:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(e)
    
    # return the connection to use
    return connection



#####################################################
##  Issue (new_issue, get all, get details)
#####################################################
#Add the details for a new issue to the database - details for new issue provided as parameters
def new_issue(title, creator, resolver, verifier, description):

    # TODO - add an issue
    # Insert a new issue to database

    # return False if adding was unsuccessful 
	# return Ture if adding was successful
    return True

#Update the details of an issue having the provided issue_id with the values provided as parameters
def update_issue(title, creator, resolver, verifier, description, issue_id):

    # TODO - update the issue using db

    # return False if adding was unsuccessful 
	# return Ture if adding was successful
    print(issue_id)
    return True

'''
List all the user associated issues in the database for a given member
See assignment description for how to load user associated issues based on the user id (member_id)
'''
def all_issue(member_id):

    # TODO - list all user associated issues from db using sql
    conn = database_connect()
    cursor = conn.cursor()

    cursor.execute('select title, creator, resolver, verifier, description, ID from A3_ISSUE where ID = %s order by title' %member_id)

    issue_db = cursor.fetchall()

    issue = [{
        'title': row[0],
        'creator': row[1],
        'resolver': row[2],
        'verifier': row[3],
        'description': row[4],
        'issue_id': row[5]
    } for row in issue_db]


    '''
    print(member_id)

    issue_db = [
        ['Division by zero', '1', '1', '1', 'Division by 0 doesn\'t yield error or infinity as would be expected. Instead it results in -1.', '1'],
        ['Factorial with addition anomaly', '1', '1', '1', 'No description', '2']
    ]
    '''

    
    return issue


'''
Find the associated issues for the user with the given userId (member_id) based on the searchString provided as the parameter, and based on the assignment description
'''
def all_issue_find(searchString, member_id):
    n  = '1'

    name, key = search(searchString)

    conn = database_connect()
    cursor = conn.cursor()


    cursor.execute("""
            select title, creator, resolver, verifier, description, ID from AS_ISSUE where ID = (%s) and cretor = (%s) order by title;
        """, (member_id, n))
    issue_db = cursor.fetchall()
    # TODO - find necessary issues using sql database based on search input
    print(member_id)
    print("search string '" + searchString + "'")

    issue = [{
        'title': row[0],
        'creator': row[1],
        'resolver': row[2],
        'verifier': row[3],
        'description': row[4],
		'issue_id': row[5]
    } for row in issue_db]

    return issue

'''
Anaylis string to find name and key words
'''
def search(searchString):
    name = []
    key = []
    switch_n = -1
    n = ''
    k = ''

    for i in searchString:
        if i == '@':
            switch_n = switch_n * -1
            name.append(n)
            n = ''
        elif i == '|':
            key.append(n)
            k = ''
        elif switch_n == 1:
            n += i 
        else:
            k += i 

    """
        leftA = searchString.find('@')
        rightA = searchString.rfind('@')        
        name = searchString[int(leftA+1):int(rightA)]
                
        print(leftA, rightA)
    """    
    return name, key




    		

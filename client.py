# -*- coding: utf-8 -*-
import requests
import getpass

token_url = 'http://localhost:8000/get_access_token/'
token = None

choices = """
-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
-  1. List Books                    -
-  2. Replace Library with New One  -
-  3. Add new Library to Existing   -
-  4. List Authors                  -
-  5. Exit                          -
-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
"""
while not token:
    username = input('Enter your username: ')
    password = getpass.getpass(prompt="Enter your password: ")
    try:
        response = requests.post(token_url, data={'username': username, 'password': password})
    except requests.exceptions.ConnectionError:
        print('connection error!')
        quit()
    if 'token' in response.json():
        token = response.json()['token']
        print('login successful!')
    else:
        print('no such user!')

headers = {'Authorization': 'Token {}'.format(token)}
while True:
    print(choices)
    choice = input('Enter your choice: ')
    if choice == '5':
        print('bye bye..')
        quit()
    elif choice == '1':
        response = requests.get('http://localhost:8000/book/', headers=headers)
        for book in response.json():
            print(50*'-')
            print('{} - {} - {}'.format(book['book_id'], book['title'], book['lc_classification']))
            print('---------- Authors ----------')
            for author in book['authors']:
                print('{} - {}'.format(author['name'] + ' ' + author['surname'], author['birth_date']))

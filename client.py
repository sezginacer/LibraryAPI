# -*- coding: utf-8 -*-
"""You can run below Python commands in project's home directory to initially fill the database...
import requests
headers = {'Authorization': 'Token YOUR_API_ACCESS_TOKEN'}
requests.post('http://127.0.0.1:8000/library/',
              files={'csv': open('random-genrator/records.csv')}, headers=headers)
"""
import requests
import getpass

url = 'http://localhost:8000/'
token_url = url + 'token/'
signup_url = url + 'signup/'

token = None

choices = """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
=  1. Replace Library with New One  =
=  2. Add new Library to Existing   =
=  3. List Books                    =
=  4. List Authors                  =
=  5. View Book                     =
=  6. View Author                   =
=  7. Update Book                   =
=  8. Update Author                 =
=  9. Exit                          =
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""
while not token:
    opt = input('signin (i), signup (u) or exit (e): ')
    if opt == 'i':
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
            print('username or password wrong, try again!')
    elif opt == 'u':
        username = input('Enter username: ')
        password = getpass.getpass(prompt="Enter password: ")
        try:
            resp = requests.post(signup_url, data={'username': username, 'password': password})
        except requests.exceptions.ConnectionError:
            print('connection error!')
            quit()
        if resp.ok:
            token = resp.json()['token']
        print(resp.json()['detail'])
    elif opt == 'e':
        print('bye bye..')
        quit()
    else:
        print('invalid option!')

headers = {'Authorization': 'Token {}'.format(token)}

while True:
    print(choices)
    choice = input('Enter your choice: ')

    if choice == '1':
        file_name = input('Enter the library file path: ')
        try:
            print('it may take long time, please wait..')
            resp = requests.post(url + 'library/', headers=headers, files={"csv_data": open(file_name, 'r')})
            print(resp.json()["detail"])
        except FileNotFoundError:
            print('{} file not found!'.format(file_name))
        except Exception:
            print('an error occurred!')

    elif choice == '2':
        file_name = input('Enter the library file path: ')
        try:
            print('it may take long time, please wait..')
            resp = requests.patch(url + 'library/', headers=headers, files={"csv_data": open(file_name, 'r')})
            print(resp.json()["detail"])
        except FileNotFoundError:
            print('{} file not found!'.format(file_name))
        except Exception:
            print('an error occurred!')

    elif choice == '3':
        resp = requests.get(url + 'book/', headers=headers)
        for book in resp.json():
            print(50 * '-')
            print('{} - {} - {}'.format(book['book_id'], book['title'], book['lc_classification']))
            print('---------- Authors ----------')
            for author in book['authors']:
                print('{} - {}'.format(author['name'] + ' ' + author['surname'], author['birth_date']))

    elif choice == '4':
        resp = requests.get(url + 'author/', headers=headers)
        if len(resp.json()) == 0:
            print('library is empty!')
        else:
            for author in resp.json():
                print(author['name'], author['surname'], author['birth_date'])

    elif choice == '5':
        pk = input('Enter the Book ID: ')
        resp = requests.get(url + 'book/{}/'.format(pk), headers=headers)
        book = resp.json()
        if resp.ok:
            print('{} - {} - {}'.format(book['book_id'], book['title'], book['lc_classification']))
            print('---------- Authors ----------')
            for author in book['authors']:
                print('{} - {}'.format(author['name'] + ' ' + author['surname'], author['birth_date']))
        else:
            print(data['detail'])

    elif choice == '6':
        pk = input('Enter the Author ID: ')
        resp = requests.get(url + 'author/{}/'.format(pk), headers=headers)
        data = resp.json()
        if resp.ok:
            print(data['name'], data['surname'], data['birth_date'])
        else:
            print(data['detail'])

    elif choice == '7':
        pk = input('Enter the ID of the book you want to update: ')
        data = input('Enter the book info seperated by commas: ')
        data = data.strip().split(',')
        data = [d.strip() for d in data]
        data = ','.join(data)
        resp = requests.put(url + 'book/{}/'.format(pk), data={'infos': data}, headers=headers)
        print(resp.json()['detail'])

    elif choice == '8':
        pk = input('Enter the ID of author you want to update: ')
        data = input('Enter the author info seperated by commas: ')
        data = data.strip().split(',')
        data = [d.strip() for d in data]
        data = ','.join(data)
        resp = requests.put(url + 'author/{}/'.format(pk), data={'infos': data}, headers=headers)
        print(resp.json()['detail'])

    elif choice == '9':
        print('bye bye..')
        quit()

    else:
        print('invalid option!')

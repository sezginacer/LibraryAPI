from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

from django.contrib.auth import authenticate, login, logout

from datetime import datetime
from main.models import Book, Author

# Create your views here.


_authentication_classes = (authentication.TokenAuthentication,
                           authentication.SessionAuthentication,
                           authentication.BasicAuthentication)
_permission_classes = (permissions.IsAuthenticated,)


class LoginAPIView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if request.user.is_authenticated():
            return Response({'error': 'already loggedin as {}'.format(request.user.username)},
                            status=status.HTTP_400_BAD_REQUEST)
        if 'username' not in request.POST or 'password' not in request.POST:
            return Response({'error': 'username or password missing!'},
                            status=status.HTTP_401_UNAUTHORIZED)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({'detail': 'login successful!', 'token': user.auth_token.key})
        return Response({'error': 'no such user!'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated():
            logout(request)
            return Response({'detail': 'logout successful!'})
        return Response({'error': 'no logout required'}, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        return Response({'error': 'authentication failed!'}, status=status.HTTP_401_UNAUTHORIZED)


class IndexView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = ()

    def get(self, request):
        endpoints = [
            {
                'endpoint': '/login/',
                'methods': {
                    'POST': {
                        'explanation': 'username and password required parameters',
                        'auth_required': False
                    }
                }
            },
            {
                'endpoint': '/logout/',
                'methods': {
                    'GET': {
                        'explanation': 'logout',
                        'auth_required': False
                    }
                }
            },
            {
                'endpoint': '/library/',
                'methods': {
                    'POST': {
                        'explanation': 'csv file to be uploaded',
                        'auth_required': True
                    },
                    'PATCH': {
                        'explanation': 'csv file to be uploaded',
                        'auth_required': True
                    }
                }
            },
            {
                'endpoint': '/book/',
                'methods': {
                    'GET': {
                        'explanation': 'filter parameter can be used',
                        'auth_required': True
                    },
                    'POST': {
                        'explanation': 'new book data as csv to be uploaded',
                        'auth_required': True
                    }
                }
            },
            {
                'endpoint': '/book/<id>/',
                'methods': {
                    'GET': {
                        'explanation': 'book details',
                        'auth_required': True
                    },
                    'PATCH': {
                        'explanation': 'book update',
                        'auth_required': True
                    },
                    'PUT': {
                        'explanation': 'book replace',
                        'auth_required': True
                    }
                }
            },
            {
                'endpoint': '/author/',
                'methods': {
                    'GET': {
                        'explanation': 'filter parameter can be used',
                        'auth_required': True
                    },
                    'POST': {
                        'explanation': 'new author data as csv to be uploaded',
                        'auth_required': True
                    }
                }
            },
            {
                'endpoint': '/author/<id>/',
                'methods': {
                    'GET': {
                        'explanation': 'author details',
                        'auth_required': True
                    },
                    'PATCH': {
                        'explanation': 'author update',
                        'auth_required': True
                    },
                    'PUT': {
                        'explanation': 'author replace',
                        'auth_required': True
                    }
                }
            }
        ]
        return Response(endpoints)


class LibraryView(APIView):
    """
    POST: CSV file, in the body, removes everything from the database and creates a new one with all books ands authors
    from the database.
    PATCH: CSV file, in the body, adding just these books, with the author.
    * Requires token authentication.
    * Only authenticated users are able to access this view.

    import requests
    url='http://127.0.0.1:8000/library/'
    files={'files': open('csv.csv','rb')}
    values={'upload_file' : 'file.txt' , 'DB':'photcat' , 'OUT':'csv' , 'SHORT':'short'}
    r=requests.post(url,files=files,data=values)
    """
    authentication_classes = _authentication_classes
    permission_classes = _permission_classes

    def post(self, request):
        Author.objects.all().delete()
        Book.objects.all().delete()
        if len(request.FILES) == 0:
            return Response({'error': 'no csv file supplied!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        csv_data = ''
        for f in request.FILES.values():
            csv_data += f.read().decode('utf-8').strip() + '\n'
        csv_lines = csv_data.strip().split('\n')
        for line in csv_lines:
            try:
                infos = line.strip().split(',')
                b, _ = Book.objects.get_or_create(
                    title=infos[0],
                    lc_classification=infos[1]
                )
                index = 2
                while index < len(infos):
                    a, _ = Author.objects.get_or_create(
                        name=infos[index],
                        surname=infos[index + 1],
                        birth_date=datetime.strptime(infos[index + 2], '%Y-%m-%d')
                    )
                    b.authors.add(a)
                    index += 3
                b.save()
            except Exception as err:
                Author.objects.all().delete()
                Book.objects.all().delete()
                return Response({'error': err}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'books and authors created successfully.'})

    def patch(self, request):
        if len(request.FILES) == 0:
            return Response({'error': 'no csv file supplied!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        csv_data = ''
        for f in request.FILES.values():
            csv_data += f.read().decode('utf-8').strip()
        csv_lines = csv_data.strip().split('\n')
        for line in csv_lines:
            try:
                infos = line.strip().split(',')
                b, _ = Book.objects.get_or_create(
                    title=infos[0],
                    lc_classification=infos[1]
                )
                index = 2
                while index < len(infos):
                    a, _ = Author.objects.get_or_create(
                        name=infos[index],
                        surname=infos[index + 1],
                        birth_date=datetime.strptime(infos[index + 2], '%Y-%m-%d')
                    )
                    b.authors.add(a)
                    index += 3
                b.save()
            except Exception as err:
                return Response({'error': err}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'books and authors created successfully.'})


class BookListOrAddView(APIView):
    """
    GET: List of books. Can be filtered with a regex “filter” parameter from the query string
    POST: New book
    """
    authentication_classes = _authentication_classes
    permission_classes = _permission_classes

    def get(self, request):
        book_list = []
        regex = request.GET.get('filter', r'.*')
        for book in Book.objects.filter(title__iregex=regex):
            dc = {
                'book_id': book.id,
                'title': book.title,
                'lc_classification': book.lc_classification
            }
            authors = []
            for author in book.authors.all():
                authors.append({
                    'author_id': author.id,
                    'name': author.name,
                    'surname': author.surname,
                    'birth_date': author.birth_date
                })
            dc['authors'] = authors
            book_list.append(dc)
        return Response(book_list)

    def post(self, request):
        csv_data = request.POST.get('csv_data')
        if not csv_data:
            return Response({'error': 'no csv_data posted!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = csv_data.strip().split(',')
            b, _ = Book.objects.get_or_create(
                title=data[0],
                lc_classification=data[1]
            )
            index = 2
            while index < len(data):
                a, _ = Author.objects.get_or_create(
                    name=data[index],
                    surname=data[index + 1],
                    birth_date=datetime.strptime(data[index + 2], '%Y-%m-%d')
                )
                b.authors.add(a)
                index += 3
            b.save()
        except IndexError:
            return Response({'error': 'csv_data not appropriate!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'csv_data not appropriate!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'book created successfully!'})


class AuthorListOrAddView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = _permission_classes

    def get(self, request):
        regex = request.GET.get('filter', r'.*')
        authors = []
        for author in Author.objects.filter(name__iregex=regex):
            a = {
                'author_id': author.id,
                'name': author.name,
                'surname': author.surname,
                'birth_date': author.birth_date
            }
            book_list = []
            for book in author.books.all():
                book_list.append(
                    {
                        'book_id': book.id,
                        'title': book.title,
                        'lc_classification': book.lc_classification
                    }
                )
            a['books'] = book_list
            authors.append(a)
        return Response(authors)

    def post(self, request):
        csv_data = request.POST.get('csv_data')
        if not csv_data:
            return Response({'error': 'no csv_data posted!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = csv_data.strip().split(',')
            a, _ = Author.objects.get_or_create(
                name=data[0],
                surname=data[1],
                birth_date=data[2]
            )
        except IndexError:
            return Response({'error': 'csv_data not appropriate!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'csv_data not appropriate!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'author created successfully!'})


class BookDetailOrUpdateView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = _permission_classes

    def get(self, request, pk):
        if Book.objects.filter(pk=pk).exists():
            b = Book.objects.get(pk=pk)
            data = {
                'book_id': b.id,
                'title': b.title,
                'lc_classification': b.lc_classification
            }
            authors = []
            for a in b.authors.all():
                authors.append({
                    'author_id': a.id,
                    'name': a.name,
                    'surname': a.surname,
                    'birth_date': a.birth_date
                })
            data['authors'] = authors
            return Response(data)
        return Response({'error': 'no such book'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        pass

    def put(self, request, pk):
        pass


class AuthorDetailOrUpdateView(APIView):

    authentication_classes = _authentication_classes
    permission_classes = _permission_classes

    def get(self, request, pk):
        if Author.objects.filter(pk=pk).exists():
            a = Author.objects.get(pk=pk)
            data = {
                'author_id': a.id,
                'name': a.name,
                'surname': a.surname,
                'birth_date': a.birth_date
            }
            books = []
            for b in a.books.all():
                books.append({
                    'book_id': b.id,
                    'title': b.title,
                    'lc_classification': b.lc_classification,
                })
            data['books'] = books
            return Response(data)
        return Response({'error': 'no such author'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        pass

    def put(self, request, pk):
        pass

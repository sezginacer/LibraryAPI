from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

from datetime import datetime
# from jsonview.decorators import json_view
# from django.utils.decorators import method_decorator
from main.models import Book, Author

# Create your views here.


authentications = (authentication.TokenAuthentication,
                   authentication.SessionAuthentication,
                   authentication.BasicAuthentication)
permissions = (permissions.IsAuthenticated,)


class IndexView(APIView):

    authentication_classes = authentications
    permission_classes = permissions

    def get(self, request):
        endpoints = [
            {
                'endpoint': '/library/',
                'methods': [
                    'POST', 'PATCH'
                ]
            },
            {
                'endpoint': '/book/',
                'methods': [
                    'GET', 'POST'
                ]
            },
            {
                'endpoint': '/book/<id>/',
                'methods': [
                    'GET', 'PATCH', 'PUT'
                ]
            },
            {
                'endpoint': '/author/',
                'methods': [
                    'GET', 'POST'
                ]
            },
            {
                'endpoint': '/author/<id>/',
                'methods': [
                    'GET', 'PATCH', 'PUT'
                ]
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
    authentication_classes = authentications
    permission_classes = permissions

    def post(self, request):
        Author.objects.all().delete()
        Book.objects.all().delete()
        if len(request.FILES) == 0:
            return Response({'error': 'no csv file supplied!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        csv_data = ''
        try:
            for f in request.FILES.values():
                csv_data += f.read().decode("utf-8").strip()
            csv_lines = csv_data.strip().split('\n')
            for line in csv_lines:
                b = Book()
                infos = line.strip().split(',')
                b.title = infos[0]
                b.lc_classification = infos[1]
                index = 2
                b.save()
                while index < len(infos):
                    a, _ = Author.objects.get_or_create(
                        name=infos[index],
                        surname=infos[index + 1],
                        birth_date=datetime.strptime(infos[index + 2], '%Y-%m-%d')
                    )
                    b.authors.add(a)
                    index += 3
                b.save()
        except Exception:
            return Response({'error': 'cannot read file(s) uploaded'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'books and authors created successfully.'})

    def patch(self, request):
        if len(request.FILES) == 0:
            return Response({'error': 'no csv file supplied!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        csv_data = ''
        try:
            for f in request.FILES.values():
                csv_data += f.read().decode("utf-8").strip()
            csv_lines = csv_data.strip().split('\n')
            for line in csv_lines:
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
        except:
            return Response({'error': 'cannot read file(s) uploaded'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({'message': 'books and authors created successfully.'})


class BookListOrAddView(APIView):
    """
    GET: List of books. Can be filtered with a regex “filter” parameter from the query string
    POST: New book
    """
    authentication_classes = authentications
    permission_classes = permissions

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
        pass


class AuthorListOrAddView(APIView):

    authentication_classes = authentications
    permission_classes = permissions

    def get(self, request):
        pass

    def post(self, request):
        pass


class BookDetailOrUpdateView(APIView):

    authentication_classes = authentications
    permission_classes = permissions

    def get(self, request):
        pass

    def patch(self, request):
        pass

    def put(self, request):
        pass


class AuthorDetailOrUpdateView(APIView):

    authentication_classes = authentications
    permission_classes = permissions

    def get(self, request):
        pass

    def patch(self, request):
        pass

    def put(self, request):
        pass
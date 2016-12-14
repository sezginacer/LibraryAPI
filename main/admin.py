from django.contrib import admin
from main.models import Author, Book

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):

    list_display = ('id', 'full_name', 'birth_date')

    def full_name(self, obj):
        return '{} {}'.format(obj.name, obj.surname)


class BookAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'authors_list', 'lc_classification')

    def authors_list(self, obj):
        ls = [a.full_name for a in obj.authors.all()]
        return ' - '.join(ls)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

import csv
from os import stat
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets

from .serializers import BookSerializer
from .models import Book

fs = FileSystemStorage(location='tmp/')

# Create your views here.
class ContentAPIView(viewsets.ViewSet):
    @csrf_exempt
    def content(self, request):
        books = Book.objects.all().order_by('date')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def topContent(self, request):
        books = Book.objects.all().order_by('-numberOfInteractions')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def upload_file(self, request):
        file = request.FILES["file"]
        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader) # assuming headers is present
        book_list = []
        for id_, row in enumerate(reader):
            (title, story, author) = row
            book_list.append(Book(title=title, story=story, author=author))
        
        Book.objects.bulk_create(book_list)

        return Response("Successfully upload the data", status=status.HTTP_201_CREATED)



class BookDetailAPIView(viewsets.ViewSet):
    def get_book(self, pk):
        try:
            book = Book.objects.get(pk=pk)
            return book
        except:
            return False

    def get(self, request, pk):
        book = self.get_book(pk)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response("book is not exist!", status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        book = self.get_book(pk)
        if book:
            serializer = BookSerializer(book, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("book is not exist!", status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, pk):
        book = self.get_book(pk)
        try:
            book.delete()
            return Response("book deleted sucessfully!", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("book is not exist!", status=status.HTTP_404_NOT_FOUND)

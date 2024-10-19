""" from django.shortcuts import render

# Create your views here.
"""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Book, LibraryUser, Transaction
from .serializers import BookSerializer, LibraryUserSerializer, TransactionSerializer
from django.utils import timezone
 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.libraryuser.role == 'admin':
            serializer.save()
        else:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        if self.request.user.libraryuser.role == 'admin':
            serializer.save()
        else:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        if self.request.user.libraryuser.role == 'admin':
            instance.delete()
        else:
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

class LibraryUserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer

class TransactionViewSet(viewsets.ViewSet):

    def checkout(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        user = request.user.libraryuser
        
        if book.copies_available > 0:
            book.copies_available -= 1
            book.save()
            transaction = Transaction.objects.create(book=book, user=user)
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)

    def return_book(self, request, pk=None):
        transaction = Transaction.objects.get(pk=pk)
        transaction.return_date = timezone.now()
        transaction.book.copies_available += 1
        transaction.book.save()
        transaction.save()
        
        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
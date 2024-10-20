""" from django.shortcuts import render

# Create your views here.
"""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, LibraryUser, Transaction
from .serializers import BookSerializer, LibraryUserSerializer, TransactionSerializer, UserRegisterSerializer, UserLoginSerializer
from django.views import View
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from .forms import UserRegisterForm, UserLoginForm

def home(request):
    return HttpResponse("<h1>Welcome to Franklin's Library Management System API!</h1>")
 

# Function-Based View for book_list and user_list
""" def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()  # Fetch all books from the database
        return render(request, 'book_list.html', {'books': books})

def user_list(request):
    if request.method == 'GET':
        users = LibraryUser.objects.all()  # Fetch all library users from the database
        return render(request, 'user_list.html', {'users': users}) """

# Class-Based View for book_list and user_list

class BookListView(View):
    def get(self, request):
        books = Book.objects.all().values()  # Fetch all books as dictionaries
        return JsonResponse(list(books), safe=False)

class UserListView(View):
    def get(self, request):
        users = LibraryUser.objects.all().values()  # Fetch all users as dictionaries
        return JsonResponse(list(users), safe=False)

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
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = TransactionSerializer

    def checkout(self, request):
        book_id = request.data.get('book_id') # Get book_id from request data
        user = request.user.libraryuser # Get the logged-in user
        if not book_id:
            return Response({"error": "Book ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Checkout logic before creating endpoints

        # if book.copies_available > 0:
        #     book.copies_available -= 1
        #     book.save()
        #     transaction = Transaction.objects.create(book=book, user=user)
        #     return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        
        # return Response({"error": "No copies available."}, status=status.HTTP_400_BAD_REQUEST)

        #new checkout logic

        try:
            book = Book.objects.get(id=book_id)

            if book.copies_available <= 0:
                return Response({"error": "No available copies for checkout."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user already has a checked-out book
            if Transaction.objects.filter(user=user, return_date__isnull=True).exists():
                return Response({"error": "User already has a book checked out."}, status=status.HTTP_403_FORBIDDEN)

            # Create transaction
            transaction = Transaction.objects.create(book=book, user=user)
            book.copies_available -= 1
            book.save()

            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)


    def return_book(self, request):
        transaction_id = request.data.get('transaction_id') # Get transaction_id from request data

        try:
            transaction = Transaction.objects.get(id=transaction_id)

            if transaction.return_date is not None:
                return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

            transaction.return_date = timezone.now()
            transaction.book.copies_available += 1
            transaction.book.save()
            transaction.save()
        
            return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
    
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND)



class RegisterView(APIView):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration_success.html', {'username': user.username})
        return render(request, 'register.html', {'form': form})
        
        """ serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

class LoginView(APIView):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)  # Log the user in
                refresh = RefreshToken.for_user(user)
                return render(request, 'login_success.html', {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return render(request, 'login.html', {'form': form, 'error': "Invalid credentials."})
        
        return render(request, 'login.html', {'form': form})
        
        
        """ serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """


# FBV for register and login

""" @api_view(['POST'])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """
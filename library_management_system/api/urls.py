from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, BookViewSet, LibraryUserViewSet, TransactionViewSet, BookListView, UserListView # Import the views I want to include

# Create a router and register my viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet)  # Register BookViewSet
router.register(r'users', LibraryUserViewSet)  # Register LibraryUserViewSet
router.register(r'transactions', TransactionViewSet)  # Register TransactionViewSet

urlpatterns = [
    path('', home, name='home'),  # Home route
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT token obtain route
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT token refresh route
    path('api/', include(router.urls)), # Include router URLs for CRUD operations
    
    # CRUD operations for books and users
    path('books/', BookViewSet.as_view({'get': 'list', 'post': 'create'}), name='book-list') ,  # Example for listing books
    path('books/<int:pk>/', BookViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='book-detail'),  # Example for retrieving, updating, and deleting a book by ID
    path('checkout/', TransactionViewSet.as_view({'post': 'checkout'}), name='checkout-book'),
    path('return/', TransactionViewSet.as_view({'post': 'return_book'}), name='return-book'),  # Example for returning a book
    path('users/', LibraryUserViewSet.as_view({'get': 'list'}), name='user-list'),  # Example for listing users

    # Paths for book list and user list views
    path('view/books/', BookListView.as_view(), name='book_list'),  # Path for viewing all books
    path('view/users/', UserListView.as_view(), name='user_list'),  # Path for viewing all users

    path('transactions/', TransactionViewSet.as_view({'get': 'list'}), name='transaction-list'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, BookViewSet, LibraryUserViewSet, TransactionViewSet # Import any views you want to include

# Create a router and register your viewsets with it.
router = DefaultRouter()
router.register(r'books', BookViewSet)  # Register BookViewSet
router.register(r'users', LibraryUserViewSet)  # Register LibraryUserViewSet
router.register(r'transactions', TransactionViewSet)  # Register TransactionViewSet

urlpatterns = [
    path('', home, name='home'),  # Home route
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT token obtain route
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT token refresh route
    path('api/', include(router.urls)), # Include router URLs for CRUD operations
    path('books/', BookViewSet.as_view({'get': 'list'}), name='book-list'),  # Example for listing books
    path('users/', LibraryUserViewSet.as_view({'get': 'list'}), name='user-list'),  # Example for listing users
    path('transactions/', TransactionViewSet.as_view({'get': 'list'}), name='transaction-list'),
]
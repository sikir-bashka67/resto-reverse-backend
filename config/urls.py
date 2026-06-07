from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from booking.views import BookingViewSet
from clients.views import ClientViewSet
from hallstables.views import HallViewSet, TableViewSet
from menuorderspreorders.views import CategoryViewSet, MenuViewSet, OrderViewSet, PreOrderViewSet, ProfileViewSet
from staff.views import StaffViewSet
from clients.views import RegisterView, LogoutView, DeleteAccountView, PasswordResetView, PasswordResetConfirmView, VerifyEmailView

router = routers.DefaultRouter()
router.register(r'staff', StaffViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'client', ClientViewSet)
router.register(r'booking', BookingViewSet)
router.register(r'order', OrderViewSet)
router.register(r'preorder', PreOrderViewSet)
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'category', CategoryViewSet)
router.register(r'hall', HallViewSet)
router.register(r'table', TableViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Resto-Reserve API',
        default_version='v1',
        description='API documentation for the restaurant reservation system.',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('api/auth/delete-account/', DeleteAccountView.as_view(), name='auth_delete_account'),
    path('api/auth/password-reset/', PasswordResetView.as_view(), name='auth_password_reset'),
    path('api/auth/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='auth_password_reset_confirm'),
    path('api/auth/verify-email/', VerifyEmailView.as_view(), name='auth_verify_email')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'fabricante', views.FabricanteViewSet)
router.register(r'pneu', views.PneuViewSet)
router.register(r'compra', views.CompraViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Autenticação
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Outros endpoints
    path('teste/', views.teste),
    path('teste2/', views.teste2),
    path('categorias-class/', views.CategoriaView.as_view()),
    path('categorias-class/<int:id>/', views.CategoriaView.as_view()),
    path('categorias-apiview/', views.CategoriasList.as_view()),
    path('categorias-apiview/<int:id>/', views.CategoriaDetail.as_view()),
    path('categorias-generic/', views.CategoriaListGeneric.as_view()),
    path('categorias-generic/<int:id>/', views.CategoriaDetailGeneric.as_view()),
    path('api/', include(router.urls))
]

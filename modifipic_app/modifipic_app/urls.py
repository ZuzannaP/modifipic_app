"""modifipic_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .settings import MEDIA_URL, MEDIA_ROOT
from img_modifier.views import RawImageViewSet, BluredImageViewSet, FlippedHorizontallyImageViewSet, GrayImageViewSet,\
                               SepiaImageViewSet

import frontend_modifipic.urls

router = DefaultRouter()
router.register(r'raw_images', RawImageViewSet, basename='Raw Images View')
router.register(r'blurred_images', BluredImageViewSet, basename='Blured Images View')
router.register(r'flipped_horizontally_images', FlippedHorizontallyImageViewSet,
                basename='Flipped Horizontally Images View')
router.register(r'gray_images', GrayImageViewSet, basename='Gray Images View')
router.register(r'sepia_images', SepiaImageViewSet, basename='Sepia Images View')

urlpatterns = [
    path('owner/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-authenticate', include("rest_framework.urls")),
    path('', include(frontend_modifipic.urls)),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)

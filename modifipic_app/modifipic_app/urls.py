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
from img_modifier.views import ImageViewSet, BluredImageViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet, basename='Images View')
router.register(r'blurred_images', BluredImageViewSet, basename=' Blured Images View')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # path('blur/', BlurView.as_view(), name="blur"),
    # path('sepia/', SepiaView.as_view(), name="sepia"),
    # path('flip_horizontally/', FlipHorizontallyView.as_view(), name="flip_horizontally"),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)

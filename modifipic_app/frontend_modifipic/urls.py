from django.urls import path
from django.conf.urls.static import static

from modifipic_app.settings import MEDIA_URL, MEDIA_ROOT
from .views import upload_image_via_form_view, display_image_view, ModifyImageView


urlpatterns = [
    path('', upload_image_via_form_view, name="landing_page"),
    path('modify/<int:pk>', ModifyImageView.as_view(), name="modify"),
    path('result/<int:pk>', display_image_view, name="result")

] + static(MEDIA_URL, document_root=MEDIA_ROOT)

from django.urls import path
from django.conf.urls.static import static

from modifipic_app.settings import MEDIA_URL, MEDIA_ROOT
from img_modifier.views import upload_image_via_form_view


urlpatterns = [
    path('', upload_image_via_form_view, name="landing_page")

] + static(MEDIA_URL, document_root=MEDIA_ROOT)

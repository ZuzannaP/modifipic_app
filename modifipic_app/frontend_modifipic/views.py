from django.shortcuts import render, redirect
from .forms import ImageFileUploadForm
from img_modifier.models import TheImage


def upload_image_via_form_view(request):
    if request.method == 'POST':
        form = ImageFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]
            image = TheImage.objects.create(file=file)
            return redirect(f"modify/{image.pk}")
        else:
            # todo insert here message
            return "Something went wrong"
    else:
        form = ImageFileUploadForm()
        return render(request, 'landing_page.html', {'form': form})


def modify_image_view(request, pk):
    if request.method == 'GET':
        return render(request, 'modify_page.html')
    if request.method == 'POST':
        image = TheImage.objects.get(pk=pk)
        chosen_modification = request.POST.get("modificationType")
        if chosen_modification == "gray":
            pass
        elif chosen_modification == "sepia":
            pass
        elif chosen_modification == "blurred":
            pass
        elif chosen_modification == "flipped-horizontally":
            pass
        return redirect(f"result/{image.pk}")


def download_image_view(request, pk):
    if request.method == 'GET':
        return render(request, 'result_page.html')
    # if request.method == 'POST':
    #     pass

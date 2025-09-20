from django.shortcuts import render
from django.conf import settings
from .forms import UploadFileForm
from azure.storage.blob import BlobServiceClient

def upload_file(request):
    url = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            blob_service_client = BlobServiceClient.from_connection_string(
                settings.AZURE_STORAGE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(
                container=settings.AZURE_CONTAINER,
                blob=file.name
            )
            blob_client.upload_blob(file, overwrite=True)
            url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{settings.AZURE_CONTAINER}/{file.name}"
    else:
        form = UploadFileForm()
    return render(request, 'home/upload.html', {'form': form, 'url': url})

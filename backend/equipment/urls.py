from django.urls import path
from .views import upload_csv, get_datasets, get_dataset_detail, generate_pdf_report

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('datasets/', get_datasets, name='get_datasets'),
    path('datasets/<int:dataset_id>/', get_dataset_detail, name='get_dataset_detail'),
    path('datasets/<int:dataset_id>/pdf/', generate_pdf_report, name='generate_pdf_report'),
]

from django.urls import path
from sales.views import SalesDataListCreateView, SalesDataRetrieveUpdateDestroyView
from sales.views import GenerateReportAPI

urlpatterns = [
    path('api/sales/', SalesDataListCreateView.as_view(), name='sales-data-list-create'),
    path('api/sales/<int:pk>/', SalesDataRetrieveUpdateDestroyView.as_view(), name='sales-data-retrieve-update-destroy'),
    path('api/generate-report/', GenerateReportAPI.as_view(), name='generate-report'),
]

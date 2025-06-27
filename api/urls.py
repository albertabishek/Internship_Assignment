from django.urls import path 
from .views import PublicDataView, ProtectedDataView

urlpatterns = [
    path('public/', PublicDataView.as_view(), name='public-data'),
    path('protected/', ProtectedDataView.as_view(), name='protected-data'),
    
]
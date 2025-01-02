from django.urls import include, path
from rest_app import views

urlpatterns = [
    path('createorupdateproduct/', views.CreateProductApiView.as_view()),
    path('get-product-list',views.GetProductApiView.as_view()),
    path('get-product-details',views.GetProductDetailApiView.as_view()),
    path('delete-products',views.DeleteProductApiView.as_view())
    
]
from django.urls import include,path
from customer import views

urlpatterns = [
    path('createorupdatecustomer/', views.CreateorupdateCustomerApiView.as_view()),
    path('get-customer-list',views.CustomerlistApiView.as_view()),
    path('get-customer-details',views.GetCustomerDetailsApiViiew.as_view()),
    path('delete-customers',views.DeleteCustomerApiView.as_view())
    
]
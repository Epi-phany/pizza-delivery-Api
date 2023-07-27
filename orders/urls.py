from django.urls import path
from .views import *

urlpatterns = [
    path('',OrderCreateListView.as_view(),name='orders'),
    path('<int:pk>/',OrderDetailView.as_view(),name='order_id'),
    path('status-update/<int:pk>/',UpdateOrderStatus.as_view(),name='order_status'),
    path('user/<int:user_id>/order',UserOrderView.as_view(),name='users-order'),
    path('user/<int:user_id>/order/<int:order_id>/',UserOrderDetail.as_view(),name='user-detail')
]

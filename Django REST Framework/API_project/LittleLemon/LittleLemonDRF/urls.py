from django.urls import path, include
from . import views
from .views import SingleOrderView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('menu-items/', views.MenuItemListView.as_view()),
    path('menu-items/category', views.CategoryView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemDetailView.as_view()),
    path('groups/managers/users', views.ManagersListView.as_view()),
    path('groups/managers/users/<int:pk>', views.ManagerView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewListView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewView.as_view()),
    path('cart/menu-items', views.CartOperationsView.as_view()),
    path('orders/', views.OrderListView.as_view()),
    path('orders/<int:pk>', SingleOrderView.as_view(), name='single-order'),
   
]
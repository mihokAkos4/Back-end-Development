from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import MenuItem, Cart, Order, OrderItem, Category
from .serializers import  MenuItemSerializer, ManagerListSerializer, CartSerializer, OrderItemSerializer, CartAddSerializer, CartRemoveSerializer, OrderItemSerializer, OrderDetailSerializer, CategorySerializer
from .paginations import MenuItemListPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from .permissions import IsManager, IsDeliveryCrew
from datetime import date

# View for listing and creating menu items
class MenuItemListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]  # Rate limiting for users
    queryset = MenuItem.objects.all()  # Fetch all menu items
    serializer_class = MenuItemSerializer  # Serializer for MenuItem model
    search_fields = ['title', 'category__title']  # Fields to allow search
    ordering_fields = ['price', 'category']  # Fields to allow ordering
    pagination_class = MenuItemListPagination  # Pagination for menu items

    def get_permissions(self):
        # Define permissions based on request method
        if self.request.method == 'GET':
            permission_classes = []  # No authentication required for GET
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]  # Auth required for other methods
        return [permission() for permission in permission_classes]

# View for managing categories
class CategoryView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()  # Fetch all categories
    permission_classes = []  

# View for retrieving, updating, or deleting a specific menu item
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        # Define permissions based on request method
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
            if self.request.method == 'PATCH':
                permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
            if self.request.method == "DELETE":
                permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def patch(self, request, *args, **kwargs):
        # Toggle 'featured' status for a menu item
        menuitem = MenuItem.objects.get(pk=self.kwargs['pk'])
        menuitem.featured = not menuitem.featured
        menuitem.save()
        return JsonResponse(status=200, data={'message': f'Featured status of {menuitem.title} changed to {menuitem.featured}'})
    
# View for listing and adding managers
class ManagersListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name='Managers')  # Users in 'Managers' group
    serializer_class = ManagerListSerializer

    def get_permissions(self):
        # Allow unauthenticated GET requests
        if self.request.method == 'GET':
            permission_classes = []  # No authentication required for GET
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]  # Auth required for POST
        return [permission() for permission in permission_classes]

    def post(self, request, *args, **kwargs):
        # Add user to 'Managers' group
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Managers')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'User added to Managers group'})

class ManagerView(generics.RetrieveAPIView):  # Use RetrieveAPIView for single object retrieval
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ManagerListSerializer
    queryset = User.objects.filter(groups__name='Managers')

    def get_permissions(self):
        # Allow unauthenticated GET requests
        if self.request.method == 'GET':
            permission_classes = []  # No authentication required for GET
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]  # Auth required for other methods
        return [permission() for permission in permission_classes]

# View for managing the Delivery Crew group
class DeliveryCrewListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name='Delivery crew')  # Fetch users in 'Delivery crew' group
    serializer_class = ManagerListSerializer  # Use the same or a different serializer

    def get_permissions(self):
        # Allow unauthenticated GET requests
        if self.request.method == 'GET':
            permission_classes = []  # No authentication required for GET
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]  # Auth required for POST
        return [permission() for permission in permission_classes]

class DeliveryCrewView(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = ManagerListSerializer
    queryset = User.objects.filter(groups__name='Delivery crew')

    def get_permissions(self):
        # Allow unauthenticated GET requests
        if self.request.method == 'GET':
            permission_classes = []  # No authentication required for GET
        else:
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]  # Auth required for DELETE
        return [permission() for permission in permission_classes]

    def delete(self, request, *args, **kwargs):
        # Remove user from 'Delivery Crew' group
        user = self.get_object()
        delivery_crew_group = Group.objects.get(name='Delivery crew')
        delivery_crew_group.user_set.remove(user)
        return JsonResponse(status=200, data={'message': f'User {user.username} removed from Delivery Crew group'})

# View for handling cart operations
class CartOperationsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch the current user's cart items
        return Cart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        # Add item to cart
        serialized_item = CartAddSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        menuitem_id = request.data['menuitem']
        quantity = request.data['quantity']
        menuitem = get_object_or_404(MenuItem, id=menuitem_id)
        price = int(quantity) * menuitem.price

        # Check if the item is already in the cart
        if Cart.objects.filter(user=request.user, menuitem=menuitem).exists():
            return JsonResponse(status=409, data={'message': 'Item already in cart'})

        # Add item to cart
        Cart.objects.create(user=request.user, quantity=quantity, unit_price=menuitem.price, price=price, menuitem=menuitem)
        return JsonResponse(status=201, data={'message': 'Item added to cart!'})

    def delete(self, request, *args, **kwargs):
        # Remove item(s) from cart
        if 'menuitem' in request.data:
            serialized_item = CartRemoveSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem_id = request.data['menuitem']
            cart_item = get_object_or_404(Cart, user=request.user, menuitem_id=menuitem_id)
            cart_item.delete()
            return JsonResponse(status=200, data={'message': 'Item removed from cart'})
        else:
            # Clear the entire cart
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=200, data={'message': 'All items removed from cart'})

    def delete(self, request, *args, **kwargs):
        # Remove item(s) from cart
        if request.data['menuitem']:
            serialized_item = CartRemoveSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem = request.data['menuitem']
            cart = get_object_or_404(Cart, user=request.user, menuitem=menuitem)
            cart.delete()
            return JsonResponse(status=200, data={'message': 'Item removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=201, data={'message': 'All items removed from cart'})

# View for handling order operations
class OrderListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch orders for the authenticated user
        return Order.objects.filter(user=self.request.user)

class SingleOrderView(generics.RetrieveAPIView):
    """
    View to retrieve the details of a specific order.
    No authentication is required to access this view.
    """
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()  # Allow access to all orders
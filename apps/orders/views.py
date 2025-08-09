from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import CartSerializer, CartItemSerializer
from .serializers import OrderSerializer, OrderItemSerializer, StatusSerializer
from .models import Cart, CartItem, Order, OrderItem



class CartItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if quantity <= 0:
            raise ValidationError({'detail': 'Quantity must be greater than 0'})

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()



class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'item_id'
    lookup_url_kwarg = 'item_id'

    def get_object(self):
        cart_item = super().get_object()
        if self.request.user == cart_item.cart.user or self.request.user.is_staff:
            return cart_item
        raise PermissionDenied({'detail': 'You do not have the permission to modify this user\'s cart items'})



class CartCheckoutAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart or not cart.items.exists():
            raise ValidationError({'detail': 'Cart is empty'})

        order = serializer.save(user=user)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product = item.product,
                quantity = item.quantity
            )

        cart.items.all().delete()



class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'cart_id'
    lookup_url_kwarg = 'cart_id'

    def get_object(self):
        cart = super().get_object()
        if self.request.user == cart.user or self.request.user.is_staff:
            return cart
        raise PermissionDenied({'detail': 'You do not have the permission to modify this user\'s cart'})



class MyCartAPIView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)



class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

        

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_id'
    lookup_url_kwarg = 'order_id'

    def get_object(self):
        order = super().get_object()
        if self.request.user == order.user or self.request.user.is_staff:
            return order
        raise PermissionDenied({'detail': 'You do not have the permission to access this user\'s order'})



class MyOrderAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')



class OrderStatusAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'order_id'
    lookup_url_kwarg = 'order_id'

    def get_object(self):
        order = super().get_object()
        if self.request.user.is_staff:
            return order
        raise PermissionDenied({'detail': 'You do not have the permission to update this user\'s order status'})

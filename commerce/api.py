from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from ninja.errors import HttpError
from .models import Product, CartItem, Order, OrderItem
from .schemas import ProductIn, ProductOut, CartItemIn, CartItemOut, OrderOut
from .auth import SimpleBearerAuth

User = get_user_model()
router = Router()
auth_scheme = SimpleBearerAuth()


@router.post("/products/", response=ProductOut, auth=auth_scheme)
def create_product(request, data: ProductIn) -> Product:
    """Create a new product
    """
    product = Product.objects.create(**data.dict())
    return product


@router.get("/products/", response=List[ProductOut])
def list_products(request) -> List[Product]:
    """List all products
    """
    return list(Product.objects.all())


@router.get("/products/{product_id}/", response=ProductOut)
def get_product(request, product_id: int) -> Product:
    """Get a product by ID
    """
    return get_object_or_404(Product, id=product_id)


@router.put("/products/{product_id}/", response=ProductOut, auth=auth_scheme)
def update_product(request, product_id: int, data: ProductIn) -> Product:
    """Update a product
    """
    product = get_object_or_404(Product, id=product_id)
    for attr, value in data.dict().items():
        setattr(product, attr, value)
    product.save()
    return product


@router.delete("/products/{product_id}/", auth=auth_scheme)
def delete_product(request, product_id: int) -> dict:
    """Delete a product
    """
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return {"success": True}


@router.post("/cart/add/", response=CartItemOut, auth=auth_scheme)
def add_to_cart(request, data: CartItemIn) -> CartItem:
    """Add a product to the cart or update quantity
    """
    user = request.user
    if not isinstance(user, User) or user.id is None:
        raise HttpError(401, "Unauthorized")

    product = get_object_or_404(Product, id=data.product_id)

    cart_item, created = CartItem.objects.get_or_create(user_id=user.id, product=product)

    if not created:
        cart_item.quantity += data.quantity
    else:
        cart_item.quantity = data.quantity

    cart_item.save()
    return cart_item


@router.post("/cart/remove/", auth=auth_scheme)
def remove_from_cart(request, data: CartItemIn) -> dict:
    """Remove a product from the cart
    """
    user = request.user
    if not isinstance(user, User) or user.id is None:
        raise HttpError(401, "Unauthorized")

    cart_item = get_object_or_404(CartItem, user_id=user.id, product_id=data.product_id)
    cart_item.delete()
    return {"success": True}


@router.post("/orders/create/", response=OrderOut, auth=auth_scheme)
def create_order(request) -> OrderOut:
    """Create an order from cart items
    """
    user = request.user
    if not isinstance(user, User) or user.id is None:
        raise HttpError(401, "Unauthorized")

    cart_items = CartItem.objects.filter(user_id=user.id)
    if not cart_items.exists():
        raise HttpError(400, "Cart is empty")

    order = Order.objects.create(user=user)
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    cart_items.delete()
    products = [item.product for item in order.items.all()]

    return OrderOut(id=order.id, status=order.status, products=products)


@router.get("/orders/", response=List[OrderOut], auth=auth_scheme)
def list_orders(request) -> List[OrderOut]:
    """List all orders of the authenticated user
    """
    user = request.user
    if not isinstance(user, User) or user.id is None:
        raise HttpError(401, "Unauthorized")

    orders = Order.objects.filter(user_id=user.id)
    result: List[OrderOut] = []

    for order in orders:
        products = [item.product for item in order.items.all()]
        result.append(OrderOut(id=order.id, status=order.status, products=products))

    return result


@router.put("/orders/{order_id}/status/", auth=auth_scheme)
def update_order_status(request, order_id: int, status: str) -> dict:
    """Update order status
    """
    user = request.user
    if not isinstance(user, User) or user.id is None:
        raise HttpError(401, "Unauthorized")

    order = get_object_or_404(Order, id=order_id, user_id=user.id)
    valid_statuses = dict(Order.STATUS_CHOICES)

    if status not in valid_statuses:
        raise HttpError(400, "Invalid status")

    order.status = status
    order.save()
    return {"success": True, "status": order.status}

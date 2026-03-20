from ninja import Schema


class ProductIn(Schema):
    """Schema for creating a product
    """
    name: str
    description: str = ""
    price: float
    stock: int = 0


class ProductOut(Schema):
    """Schema for returning product data
    """

    id: int
    name: str
    description: str
    price: float
    stock: int


class CartItemIn(Schema):
    """Schema for cart operations
    """
    product_id: int
    quantity: int = 1


class CartItemOut(Schema):
    """Schema for returning cart item
    """
    id: int
    product: ProductOut
    quantity: int


class OrderOut(Schema):
    """Schema for returning order data
    """
    id: int
    status: str
    products: list[ProductOut]

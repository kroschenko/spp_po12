"""Module implementing e-commerce system with users, products, orders and sales."""

from typing import List, Dict, Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class OrderStatus(Enum):
    """Enumeration of possible order statuses."""

    PENDING = "Pending"
    PAID = "Paid"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class PaymentMethod(Enum):
    """Enumeration of available payment methods."""

    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    PAYPAL = "PayPal"
    BANK_TRANSFER = "Bank Transfer"


class User:
    """Base user class with common attributes."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Initialize a user with ID, name and email."""
        self._user_id = user_id
        self._name = name
        self._email = email
        self._created_at = datetime.now()

    @property
    def user_id(self) -> int:
        """Get user ID."""
        return self._user_id

    @property
    def name(self) -> str:
        """Get user name."""
        return self._name

    @property
    def email(self) -> str:
        """Get user email."""
        return self._email

    def __str__(self) -> str:
        """Return string representation of user."""
        return f"{self.__class__.__name__}" f"(id={self._user_id}, name='{self._name}')"

    def __eq__(self, other: object) -> bool:
        """Check equality based on user ID."""
        if not isinstance(other, User):
            return NotImplemented
        return self._user_id == other._user_id


class Product:
    """Product class with price, stock management and availability check."""

    def __init__(  # pylint: disable=too-many-positional-arguments
        self,
        product_id: int,
        name: str,
        description: str,
        price: Decimal,
        stock_quantity: int,
    ) -> None:
        """Initialize a product with all its attributes."""
        self._product_id = product_id
        self._name = name
        self._description = description
        self._price = price
        self._stock_quantity = stock_quantity
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def product_id(self) -> int:
        """Get product ID."""
        return self._product_id

    @property
    def name(self) -> str:
        """Get product name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set product name and update timestamp."""
        self._name = value
        self._updated_at = datetime.now()

    @property
    def description(self) -> str:
        """Get product description."""
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        """Set product description and update timestamp."""
        self._description = value
        self._updated_at = datetime.now()

    @property
    def price(self) -> Decimal:
        """Get product price."""
        return self._price

    @price.setter
    def price(self, value: Decimal) -> None:
        """Set product price with validation."""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
        self._updated_at = datetime.now()

    @property
    def stock_quantity(self) -> int:
        """Get stock quantity."""
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value: int) -> None:
        """Set stock quantity with validation."""
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")
        self._stock_quantity = value
        self._updated_at = datetime.now()

    def is_available(self, quantity: int = 1) -> bool:
        """Check if requested quantity is available."""
        return self._stock_quantity >= quantity

    def reduce_stock(self, quantity: int) -> bool:
        """Reduce stock by given quantity if available."""
        if self.is_available(quantity):
            self._stock_quantity -= quantity
            self._updated_at = datetime.now()
            return True
        return False

    def __str__(self) -> str:
        """Return string representation of product."""
        return (
            f"Product(id={self._product_id}, "
            f"name='{self._name}', price=${self._price})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on product ID."""
        if not isinstance(other, Product):
            return NotImplemented
        return self._product_id == other._product_id


class CartItem:
    """Represents a single item in shopping cart."""

    def __init__(self, product: Product, quantity: int) -> None:
        """Initialize cart item with product and quantity."""
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
        self._product = product
        self._quantity = quantity

    @property
    def product(self) -> Product:
        """Get product in cart item."""
        return self._product

    @property
    def quantity(self) -> int:
        """Get quantity of product."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Set quantity with validation."""
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        self._quantity = value

    @property
    def subtotal(self) -> Decimal:
        """Calculate subtotal for this cart item."""
        return self._product.price * self._quantity

    def __str__(self) -> str:
        """Return string representation of cart item."""
        return f"{self._quantity}x {self._product.name} (${self.subtotal})"


class Cart:
    """Shopping cart that holds cart items."""

    def __init__(self) -> None:
        """Initialize empty cart."""
        self._items: Dict[int, CartItem] = {}

    @property
    def items(self) -> List[CartItem]:
        """Get list of all cart items."""
        return list(self._items.values())

    @property
    def total(self) -> Decimal:
        """Calculate total price of all items."""
        return sum(item.subtotal for item in self._items.values())

    @property
    def item_count(self) -> int:
        """Get total number of items (sum of quantities)."""
        return sum(item.quantity for item in self._items.values())

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Add product to cart with given quantity."""
        if not product.is_available(quantity):
            raise ValueError(f"Insufficient stock for {product.name}")
        if product.product_id in self._items:
            new_quantity = self._items[product.product_id].quantity + quantity
            if not product.is_available(new_quantity):
                raise ValueError(f"Insufficient stock for {product.name}")
            self._items[product.product_id].quantity = new_quantity
        else:
            self._items[product.product_id] = CartItem(product, quantity)

    def remove_item(self, product_id: int) -> bool:
        """Remove product from cart by ID."""
        if product_id in self._items:
            del self._items[product_id]
            return True
        return False

    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """Update quantity of product in cart."""
        if product_id not in self._items:
            return False
        cart_item = self._items[product_id]
        if not cart_item.product.is_available(quantity):
            raise ValueError(f"Insufficient stock for {cart_item.product.name}")
        if quantity <= 0:
            del self._items[product_id]
        else:
            cart_item.quantity = quantity
        return True

    def clear(self) -> None:
        """Remove all items from cart."""
        self._items.clear()

    def __str__(self) -> str:
        """Return string representation of cart."""
        if not self._items:
            return "Cart is empty"
        items_str = "\n  ".join(str(item) for item in self._items.values())
        return f"Cart contains:\n  {items_str}\nTotal: ${self.total}"


class Customer(User):
    """Customer class extending User with shopping cart and order history."""

    def __init__(  # pylint: disable=too-many-positional-arguments
        self,
        user_id: int,
        name: str,
        email: str,
        phone: str,
        address: str,
    ) -> None:
        """Initialize customer with personal information."""
        super().__init__(user_id, name, email)
        self._phone = phone
        self._address = address
        self._cart = Cart()
        self._orders: List["Order"] = []
        self._is_blacklisted = False

    @property
    def phone(self) -> str:
        """Get customer phone number."""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Set customer phone number."""
        self._phone = value

    @property
    def address(self) -> str:
        """Get customer address."""
        return self._address

    @address.setter
    def address(self, value: str) -> None:
        """Set customer address."""
        self._address = value

    @property
    def cart(self) -> Cart:
        """Get customer's shopping cart."""
        return self._cart

    @property
    def orders(self) -> List["Order"]:
        """Get copy of customer's order list."""
        return self._orders.copy()

    @property
    def is_blacklisted(self) -> bool:
        """Check if customer is blacklisted."""
        return self._is_blacklisted

    def set_blacklisted(self, value: bool) -> None:
        """Set blacklist status (internal use)."""
        self._is_blacklisted = value

    def add_order(self, order: "Order") -> None:
        """Add order to customer's history."""
        self._orders.append(order)

    def __str__(self) -> str:
        """Return string representation of customer."""
        status = " [BLACKLISTED]" if self._is_blacklisted else ""
        return f"Customer(id={self.user_id}, " f"name='{self.name}'{status})"


class Order:
    """Order class representing a customer purchase."""

    def __init__(self, order_id: int, customer: Customer) -> None:
        """Initialize order with ID and customer."""
        self._order_id = order_id
        self._customer = customer
        self._items: List[CartItem] = []
        self._status = OrderStatus.PENDING
        self._created_at = datetime.now()
        self._paid_at: Optional[datetime] = None
        self._payment_method: Optional[PaymentMethod] = None
        self._total_amount = Decimal("0.00")

    @property
    def order_id(self) -> int:
        """Get order ID."""
        return self._order_id

    @property
    def customer(self) -> Customer:
        """Get customer who placed order."""
        return self._customer

    @property
    def items(self) -> List[CartItem]:
        """Get copy of order items."""
        return self._items.copy()

    @property
    def status(self) -> OrderStatus:
        """Get order status."""
        return self._status

    @property
    def total_amount(self) -> Decimal:
        """Get total order amount."""
        return self._total_amount

    @property
    def created_at(self) -> datetime:
        """Get order creation timestamp."""
        return self._created_at

    @property
    def paid_at(self) -> Optional[datetime]:
        """Get payment timestamp."""
        return self._paid_at

    @property
    def payment_method(self) -> Optional[PaymentMethod]:
        """Get payment method used."""
        return self._payment_method

    def create_from_cart(self) -> None:
        """Create order items from customer's cart."""
        self._items = [
            CartItem(item.product, item.quantity) for item in self._customer.cart.items
        ]
        self._total_amount = self._customer.cart.total

    def pay(self, payment_method: PaymentMethod) -> bool:
        """Process payment for the order."""
        if self._customer.is_blacklisted:
            return False
        if self._status != OrderStatus.PENDING:
            return False
        for item in self._items:
            if not item.product.is_available(item.quantity):
                return False
        for item in self._items:
            item.product.reduce_stock(item.quantity)
        self._status = OrderStatus.PAID
        self._paid_at = datetime.now()
        self._payment_method = payment_method
        self._customer.cart.clear()
        return True

    def update_status(self, status: OrderStatus) -> None:
        """Update order status."""
        self._status = status

    def __str__(self) -> str:
        """Return string representation of order."""
        return (
            f"Order #{self._order_id} - "
            f"{self._status.value} - ${self._total_amount}"
        )


class Sale:
    """Sale class representing completed payment transaction."""

    def __init__(self, sale_id: int, order: Order) -> None:
        """Initialize sale from paid order."""
        if order.status != OrderStatus.PAID:
            raise ValueError("Only paid orders can be registered as sales")
        self._sale_id = sale_id
        self._order = order
        self._registered_at = datetime.now()

    @property
    def sale_id(self) -> int:
        """Get sale ID."""
        return self._sale_id

    @property
    def order(self) -> Order:
        """Get associated order."""
        return self._order

    @property
    def registered_at(self) -> datetime:
        """Get registration timestamp."""
        return self._registered_at

    @property
    def total_amount(self) -> Decimal:
        """Get sale total amount."""
        return self._order.total_amount

    def __str__(self) -> str:
        """Return string representation of sale."""
        return (
            f"Sale #{self._sale_id} "
            f"(Order #{self._order.order_id}) - ${self.total_amount}"
        )


class BlacklistEntry:
    """Blacklist entry for banned customers."""

    def __init__(self, customer: Customer, reason: str, admin: "Administrator") -> None:
        """Initialize blacklist entry."""
        self._customer = customer
        self._reason = reason
        self._added_by = admin
        self._added_at = datetime.now()
        self._is_active = True
        customer.set_blacklisted(True)

    @property
    def customer(self) -> Customer:
        """Get blacklisted customer."""
        return self._customer

    @property
    def reason(self) -> str:
        """Get blacklist reason."""
        return self._reason

    @property
    def added_by(self) -> "Administrator":
        """Get admin who added entry."""
        return self._added_by

    @property
    def added_at(self) -> datetime:
        """Get creation timestamp."""
        return self._added_at

    @property
    def is_active(self) -> bool:
        """Check if blacklist entry is active."""
        return self._is_active

    def deactivate(self) -> None:
        """Deactivate blacklist entry."""
        self._is_active = False
        self._customer.set_blacklisted(False)

    def __str__(self) -> str:
        """Return string representation of blacklist entry."""
        status = "Active" if self._is_active else "Inactive"
        return f"BlacklistEntry({self._customer.name} - " f"{status} - {self._reason})"


class Administrator(User):
    """Administrator class with product and blacklist management."""

    def __init__(self, user_id: int, name: str, email: str, role: str) -> None:
        """Initialize administrator with role."""
        super().__init__(user_id, name, email)
        self._role = role
        self._blacklist: List[BlacklistEntry] = []
        self._products: List[Product] = []
        self._sales: List[Sale] = []

    @property
    def role(self) -> str:
        """Get administrator role."""
        return self._role

    def add_product(self, product: Product) -> None:
        """Add product to admin's managed list."""
        self._products.append(product)

    def update_product(self, product_id: int, **kwargs) -> bool:
        """Update product attributes dynamically."""
        for product in self._products:
            if product.product_id == product_id:
                for key, value in kwargs.items():
                    if hasattr(product, key):
                        setattr(product, key, value)
                return True
        return False

    def remove_product(self, product_id: int) -> bool:
        """Remove product from admin's list."""
        for i, product in enumerate(self._products):
            if product.product_id == product_id:
                self._products.pop(i)
                return True
        return False

    def register_sale(self, order: Order) -> Optional[Sale]:
        """Register a sale from paid order."""
        if order.status != OrderStatus.PAID:
            return None
        sale_id = len(self._sales) + 1
        sale = Sale(sale_id, order)
        self._sales.append(sale)
        return sale

    def add_to_blacklist(self, customer: Customer, reason: str) -> BlacklistEntry:
        """Add customer to blacklist."""
        entry = BlacklistEntry(customer, reason, self)
        self._blacklist.append(entry)
        return entry

    def remove_from_blacklist(self, customer: Customer) -> bool:
        """Remove customer from blacklist."""
        for entry in self._blacklist:
            if entry.customer == customer and entry.is_active:
                entry.deactivate()
                return True
        return False

    def get_blacklist(self) -> List[BlacklistEntry]:
        """Get all blacklist entries."""
        return self._blacklist.copy()

    def get_active_blacklist(self) -> List[BlacklistEntry]:
        """Get only active blacklist entries."""
        return [entry for entry in self._blacklist if entry.is_active]

    def __str__(self) -> str:
        """Return string representation of administrator."""
        return (
            f"Administrator(id={self.user_id}, "
            f"name='{self.name}', role='{self._role}')"
        )


class ECommerceSystem:
    """Main e-commerce system coordinating all components."""

    def __init__(self) -> None:
        """Initialize empty e-commerce system."""
        self._customers: Dict[int, Customer] = {}
        self._administrators: Dict[int, Administrator] = {}
        self._products: Dict[int, Product] = {}
        self._orders: Dict[int, Order] = {}
        self._sales: List[Sale] = []
        self._next_order_id = 1

    def register_customer(self, customer: Customer) -> None:
        """Register a new customer in system."""
        self._customers[customer.user_id] = customer

    def register_administrator(self, admin: Administrator) -> None:
        """Register a new administrator in system."""
        self._administrators[admin.user_id] = admin

    def add_product(self, product: Product, admin: Administrator) -> bool:
        """Add product to system if admin exists."""
        if admin.user_id not in self._administrators:
            return False
        self._products[product.product_id] = product
        admin.add_product(product)
        return True

    def create_order(self, customer: Customer) -> Optional[Order]:
        """Create an order from customer's cart."""
        if customer.user_id not in self._customers:
            return None
        if customer.cart.item_count == 0:
            return None
        order = Order(self._next_order_id, customer)
        order.create_from_cart()
        self._orders[self._next_order_id] = order
        customer.add_order(order)
        self._next_order_id += 1
        return order

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return self._products.get(product_id)

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        return self._customers.get(customer_id)

    def get_order(self, order_id: int) -> Optional[Order]:
        """Get order by ID."""
        return self._orders.get(order_id)

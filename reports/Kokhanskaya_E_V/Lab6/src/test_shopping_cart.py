"""Tests for shopping cart functionality."""

# pylint: disable=redefined-outer-name

from unittest.mock import patch

import pytest

# Try to import requests, but don't fail if not installed
try:
    import requests
except ImportError:
    requests = None


class Cart:
    """Shopping cart implementation."""

    def __init__(self):
        """Initialize empty cart."""
        self._items = []

    def add_item(self, name: str, price: float) -> None:
        """
        Add item to cart.

        Args:
            name: Item name
            price: Item price

        Raises:
            ValueError: If price is negative
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._items.append({"name": name, "price": price})

    def total(self) -> float:
        """Calculate total cost of all items."""
        return sum(item["price"] for item in self._items)

    def get_items_count(self) -> int:
        """Get number of items in cart."""
        return len(self._items)

    def apply_discount(self, percent: float) -> None:
        """
        Apply discount to all items.

        Args:
            percent: Discount percentage (0-100)

        Raises:
            ValueError: If percent is outside 0-100 range
        """
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        multiplier = 1 - (percent / 100)
        for item in self._items:
            item["price"] = item["price"] * multiplier

    def apply_coupon(self, coupon_code: str) -> None:
        """
        Apply coupon discount.

        Args:
            coupon_code: Coupon code to apply

        Raises:
            ValueError: If coupon is invalid
        """
        coupons = {"SAVE10": 10, "HALF": 50}
        if coupon_code in coupons:
            self.apply_discount(coupons[coupon_code])
        else:
            raise ValueError("Invalid coupon")


def log_purchase(item):
    """Log purchase to remote system."""
    if requests is None:
        return  # Skip if requests not installed
    requests.post("https://example.com/log", json=item, timeout=5)


@pytest.fixture
def empty_cart():
    """Fixture that returns empty Cart instance."""
    return Cart()


class TestCart:
    """Test cases for Cart class."""

    # ========== TASK 1.1: ADD ITEM TESTS ==========

    def test_add_item_success(self, empty_cart):
        """Test adding item to cart increases item count."""
        empty_cart.add_item("Apple", 10.0)
        assert empty_cart.get_items_count() == 1

    def test_add_item_negative_price_raises_error(self, empty_cart):
        """Test adding item with negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price cannot be negative"):
            empty_cart.add_item("Apple", -10.0)

    def test_total_calculation(self, empty_cart):
        """Test total calculation returns correct sum."""
        empty_cart.add_item("Apple", 10.0)
        empty_cart.add_item("Banana", 15.0)
        empty_cart.add_item("Orange", 5.0)
        assert empty_cart.total() == 30.0

    # ========== TASK 1.2: DISCOUNT TESTS WITH PARAMETRIZE ==========

    @pytest.mark.parametrize(
        "discount,expected_price",
        [
            (0, 100.0),
            (50, 50.0),
            (100, 0.0),
        ],
    )
    def test_apply_discount_valid(self, discount, expected_price):
        """Test discount with valid percentages."""
        cart = Cart()
        cart.add_item("Laptop", 100.0)
        cart.apply_discount(discount)
        assert cart.total() == expected_price

    @pytest.mark.parametrize("discount", [-10, 110, 150, -1])
    def test_apply_discount_invalid_raises_error(self, discount):
        """Test discount with invalid percentages raises ValueError."""
        cart = Cart()
        cart.add_item("Laptop", 100.0)
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            cart.apply_discount(discount)

    # ========== TASK 1.3: USING FIXTURE ==========

    def test_empty_cart_fixture(self, empty_cart):
        """Test that empty_cart fixture returns empty cart."""
        assert empty_cart.get_items_count() == 0
        assert empty_cart.total() == 0.0

    def test_add_multiple_items_using_fixture(self, empty_cart):
        """Test adding multiple items to cart using fixture."""
        empty_cart.add_item("Book", 25.0)
        empty_cart.add_item("Pen", 2.5)
        assert empty_cart.get_items_count() == 2
        assert empty_cart.total() == 27.5

    # ========== TASK 1.4: MOCKING HTTP REQUESTS ==========

    @patch("test_shopping_cart.requests.post")
    def test_log_purchase_mocks_http_request(self, mock_post):
        """Test that log_purchase calls requests.post with correct data."""
        item = {"name": "Laptop", "price": 1000.0}
        log_purchase(item)

        mock_post.assert_called_once()
        mock_post.assert_called_with("https://example.com/log", json=item, timeout=5)

    @patch("test_shopping_cart.requests.post")
    def test_log_purchase_multiple_calls(self, mock_post):
        """Test multiple log_purchase calls."""
        items = [
            {"name": "Apple", "price": 10.0},
            {"name": "Banana", "price": 15.0},
        ]
        for item in items:
            log_purchase(item)

        assert mock_post.call_count == 2

    # ========== TASK 1.5: COUPON TESTS ==========

    def test_apply_coupon_save10(self, empty_cart):
        """Test SAVE10 coupon applies 10% discount."""
        empty_cart.add_item("Item", 100.0)
        empty_cart.apply_coupon("SAVE10")
        assert empty_cart.total() == 90.0

    def test_apply_coupon_half(self, empty_cart):
        """Test HALF coupon applies 50% discount."""
        empty_cart.add_item("Item", 100.0)
        empty_cart.apply_coupon("HALF")
        assert empty_cart.total() == 50.0

    def test_apply_coupon_invalid_raises_error(self, empty_cart):
        """Test invalid coupon raises ValueError."""
        empty_cart.add_item("Item", 100.0)
        with pytest.raises(ValueError, match="Invalid coupon"):
            empty_cart.apply_coupon("INVALID")


class TestAdditionalCartFeatures:
    """Additional test cases for cart functionality."""

    def test_cart_with_no_items_total_zero(self, empty_cart):
        """Test total returns 0 for empty cart."""
        assert empty_cart.total() == 0.0

    def test_apply_discount_multiple_items(self):
        """Test discount applied to all items."""
        cart = Cart()
        cart.add_item("A", 100.0)
        cart.add_item("B", 200.0)
        cart.apply_discount(10)
        assert cart.total() == 270.0

    def test_sequential_discounts(self):
        """Test applying multiple discounts sequentially."""
        cart = Cart()
        cart.add_item("Item", 100.0)
        cart.apply_discount(10)
        assert cart.total() == 90.0
        cart.apply_discount(10)
        assert cart.total() == 81.0

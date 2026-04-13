
const cartProducts = [
  {
    id: 1,
    name: "Luxury Smart Kettle 1.7L",
    price: 11328,
    image: "https://cdn.easyfrontend.com/pictures/portfolio/portfolio17.jpg",
    qty: 1
  },
  {
    id: 2,
    name: "20,000mAh Power Bank",
    price: 5411,
    image: "https://cdn.easyfrontend.com/pictures/portfolio/portfolio3.jpg",
    qty: 5
  },
  {
    id: 3,
    name: "LED Bulbs 10W (4-pack)",
    price: 21345,
    image: "https://cdn.easyfrontend.com/pictures/portfolio/portfolio13.jpg",
    qty: 3
  },
  {
    id: 4,
    name: "10m Extension Cord",
    price: 27351,
    image: "https://cdn.easyfrontend.com/pictures/portfolio/portfolio_1_1.png",
    qty: 2
  }
];

let cart = JSON.parse(localStorage.getItem('eBasketCart')) || cartProducts;
let couponDiscount = 0;

// Initialize cart
function initCart() {
  renderCartItems();
  updateSummary();
}

// Render cart items
function renderCartItems() {
  const cartItemsContainer = document.getElementById('cartItems');

  if (cart.length === 0) {
    document.getElementById('emptyCart').classList.remove('d-none');
    document.getElementById('cartItems').innerHTML = '';
    return;
  }

  document.getElementById('emptyCart').classList.add('d-none');

  cartItemsContainer.innerHTML = cart.map((product, index) => `
        <div class="card cart-card mb-4">
          <div class="card-body d-flex align-items-start p-4">
            <div class="cart-image me-3 me-md-4">
              <img src="${product.image}" alt="${product.name}" class="img-fluid" style="height: 80px; object-fit: cover;">
            </div>
            <div class="flex-grow-1">
              <div class="cart-heading mb-3">
                <h6 class="mb-2 fw-bold">${product.name}</h6>
                <small class="text-muted">Item #${product.id}</small>
              </div>
              <div class="row align-items-center">
                <div class="col-md-6">
                  <h5 class="cart-price mb-0">₹${product.price.toLocaleString()}</h5>
                  <small class="text-muted">per unit</small>
                </div>
                <div class="col-md-6">
                  <div class="input-group cart-qty">
                    <button class="btn" onclick="updateQuantity(${index}, -1)" type="button">
                      <i class="fa fa-minus"></i>
                    </button>
                    <input type="text" class="form-control" value="${product.qty}" readonly>
                    <button class="btn" onclick="updateQuantity(${index}, 1)" type="button">
                      <i class="fa fa-plus"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <button class="btn cart-del" onclick="removeItem(${index})" title="Remove Item">
                <i class="fa fa-trash-alt"></i>
              </button>
            </div>
          </div>
        </div>
      `).join('');
}

// Update quantity
function updateQuantity(index, change) {
  cart[index].qty = Math.max(1, cart[index].qty + change);

  if (cart[index].qty > 99) {
    cart[index].qty = 99;
    alert('Maximum 99 items allowed!');
  }

  saveCart();
  renderCartItems();
  updateSummary();
}

// Remove item
function removeItem(index) {
  if (confirm('Remove this item from cart?')) {
    cart.splice(index, 1);
    saveCart();
    renderCartItems();
    updateSummary();
  }
}

// Update order summary
function updateSummary() {
  const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);

  document.getElementById('subtotal').textContent = `₹${subtotal.toLocaleString()}`;
  document.getElementById('grandTotal').textContent = `₹${(subtotal - couponDiscount).toLocaleString()}`;
  document.getElementById('itemCount').textContent = totalItems;
}

// Save to localStorage
function saveCart() {
  localStorage.setItem('eBasketCart', JSON.stringify(cart));
}
// Clear cart
function clearCart() {
  if (confirm('Clear entire cart?')) {
    cart = [];
    saveCart();
    renderCartItems();
    updateSummary();
  }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initCart);

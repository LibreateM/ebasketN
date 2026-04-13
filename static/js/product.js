
const productData = {
  price: parseFloat(productPrice) || 0,
  shipping: 0
};
const qtyInput = document.getElementById('productQty');
const qtyMinus = document.getElementById('qtyMinus');
const qtyPlus = document.getElementById('qtyPlus');
const totalPriceEl = document.getElementById('totalPrice');
const pricePerItemEl = document.getElementById('pricePerItem');
const qtyDisplayEl = document.getElementById('qtyDisplay');
const singlePriceEl = document.getElementById('singlePrice');
const buyNowBtn = document.getElementById('buyNowBtn');
const addToCartBtn = document.getElementById('addToCartBtn');
function formatPrice(price) {
  return '₹' + price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
console.log(productPrice);
function updateTotal() {
  const qty = parseInt(qtyInput.value) || 1;
  const total = qty * productData.price + productData.shipping;
  totalPriceEl.textContent = formatPrice(total);
  pricePerItemEl.textContent = formatPrice(productData.price);
  qtyDisplayEl.textContent = qty;
}
qtyMinus.addEventListener('click', function () {
  let currentQty = parseInt(qtyInput.value) || 1;
  if (currentQty > 1) {
    qtyInput.value = currentQty - 1;
    updateTotal();
  }
});
qtyPlus.addEventListener('click', function () {
  let currentQty = parseInt(qtyInput.value) || 1;
  if (currentQty < 99) {
    qtyInput.value = currentQty + 1;
    updateTotal();
  }
});
qtyInput.addEventListener('input', function () {
  let value = parseInt(this.value);
  if (isNaN(value) || value < 1) {
    this.value = 1;
  } else if (value > 99) {
    this.value = 99;
  }
  updateTotal();
});
updateTotal();

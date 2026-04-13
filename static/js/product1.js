// product1.js

const productData = {
    price: parseFloat(productPrice) || 0,
    shipping: 0
};

const qtyInput = document.getElementById('productQty');
const qtyMinus = document.getElementById('qtyMinus');
const qtyPlus = document.getElementById('qtyPlus');
const totalPriceEl = document.getElementById('totalPrice');
const pricePerItemEl = document.getElementById('pricePerItem');
const qtyDisplayEl = document.getElementById('qtyDisplay');   // <span> — display only
const qtyHiddenEl = document.getElementById('qtyHidden');    // FIX: hidden input submitted in POST

function formatPrice(price) {
    return '₹' + price.toLocaleString('en-IN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function updateTotal() {
    const qty = parseInt(qtyInput.value) || 1;
    const total = qty * productData.price + productData.shipping;

    totalPriceEl.textContent = formatPrice(total);
    pricePerItemEl.textContent = formatPrice(productData.price);

    // FIX: update the visible display span
    qtyDisplayEl.textContent = qty;

    // FIX: update the hidden input so the correct qty is submitted with the form
    qtyHiddenEl.value = qty;
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

// Initialise on page load
updateTotal();
function increment_product(product_id) {
    var product_price = document.getElementById(product_id + "-price");
    product_price.innerHTML = parseInt(product_price.innerHTML) + parseInt(product_price.innerHTML) / parseInt(document.getElementById(product_id + "-count").innerHTML)
    document.getElementById(product_id + "-count").innerHTML++;
    fetch('/increase-product', {
        method: 'POST',
        body: JSON.stringify({ productId: product_id })
    })
    cart_change()
};

function decrement_product(product_id) {
    if (document.getElementById(product_id + "-count").innerHTML > 1) {
        var product_price = document.getElementById(product_id + "-price");
        product_price.innerHTML = parseInt(product_price.innerHTML) - parseInt(product_price.innerHTML) / parseInt(document.getElementById(product_id + "-count").innerHTML)
        document.getElementById(product_id + "-count").innerHTML--;
        fetch('/decrease-product', {
            method: 'POST',
            body: JSON.stringify({ productId: product_id })
        })
        cart_change()
    }
    else {
        fetch('/delete-product', {
            method: 'POST',
            body: JSON.stringify({ productId: product_id })
        }).then((_res) => {
            var cart = document.querySelector('div.offcanvas-body');
            var cartDiv_removable = document.getElementById(product_id + '-productDiv');
            cart.removeChild(cartDiv_removable);

            cart_change();
            document.getElementById('product' + product_id).disabled = false;
        });
    }
};

// Отображение корзины при наличии товара и его отсутсвии
function cart_change() {
    total = get_total_by_class('productCount')
    if (total > 0) {
        document.getElementById('shoppingCart').innerHTML = 'Корзина | ' + total;
        document.getElementById('cartHeader').innerHTML = 'Ваш выбор';
        document.getElementById('cartTotalPrice').innerHTML = get_total_by_class('productPrice');
    }
    else {
        document.getElementById('shoppingCart').innerHTML = 'Корзина';
        document.getElementById('cartHeader').innerHTML = 'Корзина пуста :(';

        var cart = document.getElementById('offcanvasRight');
        var cartFooter = document.querySelector('div.offcanvas-footer');

        cart.removeChild(cartFooter);
    }
};

function show_cart_footer() {
    var cart = document.getElementById('offcanvasRight');

    var cartFooter = document.createElement('div');
    cartFooter.className = 'offcanvas-footer';
    cart.onclick = () => { window.location.pathname = "/order" };

    var order_button = document.createElement('button');
    order_button.textContent = 'К оформлению заказа';

    var total_price = document.createElement('p');
    total_price.id = 'cartTotalPrice';
    total_price.textContent = get_total_by_class('productPrice')

    cartFooter.appendChild(total_price)
    cartFooter.appendChild(order_button)

    cart.appendChild(cartFooter);
}

// Подсчет итогового количества товара и цены
function get_total_by_class(class_name) {
    var counter = 0;
    for (var product_count of document.getElementsByClassName(class_name)) {
        counter += parseInt(product_count.innerHTML)
    };
    return counter;
};

// Добавление товара в корзину, на строне сервера
function add_product_to_cart(product_id) {
    fetch("/add-to-cart", {
        method: 'POST',
        body: JSON.stringify({ productId: product_id })
    });
    document.getElementById('product' + product_id).disabled = true;
};


function get_product(product_id) {
    fetch("/product/" + product_id)
        .then((response) => {
            return response.json();
        })
        .then((shoppingCart) => {
            add_product_info_in_cart(shoppingCart);
        });
};

// Добавление товара в корзину (без перезагрузки страницы)
function add_product_info_in_cart(product) {
    if (get_total_by_class('productCount') == 0)
        show_cart_footer();

    var cart = document.querySelector('div.offcanvas-body');
    var cartDiv = document.createElement('div');
    cartDiv.id = product.id + "-productDiv";

    var product_info = document.createElement('p')
    description = ' '
    if (product.description)
        description = product.description
    product_info.textContent = ':'.concat(product.name, description, product.category, product.price);

    var product_count = document.createElement('p');
    product_count.className = 'productCount';
    product_count.textContent = '1';
    product_count.id = product.id + '-count';

    var product_price = document.createElement('p');
    product_price.className = 'productPrice';
    product_price.textContent = product.price
    product_price.id = product.id + '-price';

    var increase_button = document.createElement('button')
    increase_button.textContent = '+';
    increase_button.onclick = function () { increment_product(product.id) };

    var decrease_button = document.createElement('button');
    decrease_button.textContent = '-';
    decrease_button.onclick = function () { decrement_product(product.id) };

    cartDiv.appendChild(product_info);
    cartDiv.appendChild(product_count);
    cartDiv.appendChild(product_price)
    cartDiv.appendChild(increase_button);
    cartDiv.appendChild(decrease_button);

    cart.appendChild(cartDiv);

    cart_change();
};

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
            document.getElementById('product' + product_id).innerHTML = 'Добавить в корзину';
            document.getElementById('product' + product_id).disabled = false;
        });
    }
};

// Отображение корзины при наличии товара и его отсутсвии
function cart_change() {
    total = get_total_by_class('productCount')
    if (total > 0) {
        for(item of document.getElementsByClassName('shoppingCart'))
            item.innerHTML = 'Корзина | ' + total;
        document.getElementById('shoppingCartMobile').innerHTML = '<i class="fi fi-rr-shopping-cart"></i>('+total+')';
        document.getElementById('cartHeader').innerHTML = 'Ваш выбор';
        document.getElementById('cartTotalPrice').innerHTML = get_total_by_class('productPrice');
    }
    else {
        for(item of document.getElementsByClassName('shoppingCart'))
            item.innerHTML = 'Корзина';
        document.getElementById('cartHeader').innerHTML = 'Корзина пуста :(';
        document.getElementById('shoppingCartMobile').innerHTML = '<i class="fi fi-rr-shopping-cart"></i>';

        var cart = document.getElementById('offcanvasRight');
        var cartFooter = document.querySelector('div.offcanvas-footer');

        cart.removeChild(cartFooter);
    }
};

function show_cart_footer() {
    var cart = document.getElementById('offcanvasRight');

    var cartFooter = document.createElement('div');
    cartFooter.className = 'offcanvas-footer';

    var cartTotalPrice = document.createElement('div');
    cartTotalPrice.className = 'cartTotalPrice-div';
    cartTotalPrice.innerHTML = '<p>Итоговая стоимость:</p>'

    productPriceSection = document.createElement('div');
    productPriceSection.className = 'productPrice-section';

    var total_price = document.createElement('p');
    total_price.id = 'cartTotalPrice';
    total_price.textContent = get_total_by_class('productPrice');

    productPriceSection.appendChild(total_price);
    productPriceSection.innerHTML += '<i class="fi fi-br-ruble-sign"></i>';

    cartTotalPrice.appendChild(productPriceSection);

    var order_button = document.createElement('button');
    order_button.className = 'orderButton-custom';
    order_button.textContent = 'К оформлению заказа';
    order_button.onclick = () => { window.location.pathname = "/order" };

    cartFooter.appendChild(cartTotalPrice);
    cartFooter.appendChild(order_button);

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
    document.getElementById('product' + product_id).innerHTML = '<i class="fi fi-br-check"></i>';
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
    cartDiv.className = 'productDiv-castom';

    var photo = document.createElement('img');
    console.log(product)
    photo.src = product.photo_url;
    photo.style.height = '100px';

    div_name_description = document.createElement('div');

    var name = document.createElement('div');
    name.className = 'title';
    name.innerHTML = product.name;

    var description = document.createElement('div')
    description.className = 'description';
    description.innerHTML = product.description;

    div_name_description.appendChild(name)
    div_name_description.appendChild(description)

    var product_info = document.createElement('div');
    product_info.className = 'productDiv-info';

    product_info.appendChild(photo);
    product_info.appendChild(div_name_description);
    cartDiv.append(product_info)

    var price_and_count_div = document.createElement('div');
    price_and_count_div.className = 'productDiv-priceAndCount';

    var productPriceSection = document.createElement('div');
    productPriceSection.className = 'productPrice-section';

    var product_price = document.createElement('p');
    product_price.className = 'productPrice';
    product_price.textContent = product.price;
    product_price.id = product.id + '-price';

    productPriceSection.appendChild(product_price);
    productPriceSection.innerHTML += '<i class="fi fi-br-ruble-sign"></i>';

    price_and_count_div.appendChild(productPriceSection);

    var decrease_button = document.createElement('button');
    decrease_button.innerHTML = '<i class="fi fi-br-minus"></i>';
    decrease_button.className = 'button-forDivProdDiv icon'
    decrease_button.onclick = function () { decrement_product(product.id) };

    var increase_button = document.createElement('button')
    increase_button.innerHTML = '<i class="fi fi-br-plus"></i>';
    increase_button.className = 'button-forDivProdDiv icon';
    increase_button.onclick = function () { increment_product(product.id) };

    var product_count = document.createElement('span');
    product_count.className = 'productCount';
    product_count.textContent = '1';
    product_count.id = product.id + '-count';

    var div_for_buttons = document.createElement('div');
    div_for_buttons.className = 'productDiv-buttons';

    div_for_buttons.appendChild(decrease_button);
    div_for_buttons.appendChild(product_count)
    div_for_buttons.appendChild(increase_button);

    price_and_count_div.appendChild(div_for_buttons)

    cartDiv.appendChild(price_and_count_div);

    cart.appendChild(cartDiv);

    cart_change();
};


//Выбор оценки в отзыве
function set_rating(value) {
    document.getElementById('ratingValue').value = value;
};
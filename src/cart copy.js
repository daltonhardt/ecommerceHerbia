let label = document.getElementById("label");
let shoppingCart = document.getElementById("shopping-cart")

// console.log(shopItemsData);

// lendo as quantidades da localStorage no caso de um refresh de página
let basket = JSON.parse(localStorage.getItem("data")) || [];

// busca da memória o tipo de venda (0, 1 ou 2)
let tipo = localStorage.getItem("tipoVenda");

// formatação moeda em REAL
const formatter = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  });

let calculation =() => {
    let cartIcon = document.getElementById("cartAmount");
    cartIcon.innerHTML = basket.map((x) => x.item).reduce((x, y) => x+y, 0);
};
calculation();

let generateCartItems = () => {
    if (basket.length !== 0) {
        console.log("O carrinho não está vazio");
        return shoppingCart.innerHTML = basket.map((x) => {
            console.log(x);
            let { id, item } = x;
            let search = shopItemsData.find((x) => x.id === id) || []; 
            let { img, name, price} = search;
            let valorItem = formatter.format(price[tipo]);
            let valorItemTotal = formatter.format(item * price[tipo]);
            // console.log(id, name, item, valorItemTotal);
            return `
            <div class="cart-item">
                <img width="100" src=${img} alt="" />
                <div class="details">
                    <div class="title-price-x">
                        <h4 class="title-price">
                            <p>${name}</p>
                            <p class="cart-item-price">${valorItem}</p>
                        </h4>
                        <i onclick="removeItem(${id})" class="bi bi-x-lg"></i>
                    </div>
                    <div class="buttons">
                        <i onclick="decrement(${id})" class="bi bi-dash-lg"></i>
                        <div id=${id} class="quantity">${item}</div>
                        <i onclick="increment(${id})" class="bi bi-plus-lg"></i>
                    </div>
                    <h3>${valorItemTotal}</h3>
                    <div class="buttons">
                        <p>Desc.</p>
                        <i onclick="decrementDiscountItem(${id})" class="bi bi-dash-lg"></i>
                        <div id=${id} class="discountItem">${item}</div>
                        <i onclick="incrementDiscountItem(${id})" class="bi bi-plus-lg"></i>
                    </div>
                </div>
            </div>
            `;
        }).join("");
    }
    else {
        console.log("O carrinho está Vazio");
        shoppingCart.innerHTML = ``;
        label.innerHTML = `
        <h2>Carrinho está Vazio</h2>
        <a href="index.html">
            <button class="HomeBtn">Início</button>
        </a>
        `;
    }
};
generateCartItems();

let increment = (id)=>{
    let selectedItem = id;
    console.log("incrementCart", selectedItem.id);
    let search = basket.find((x)=> x.id === selectedItem.id);

    if (search === undefined) {
        basket.push({ 
            id: selectedItem.id,
            item: 1,
        });
    } else {
        search.item += 1;
    }
    
    // gerando novamente os itens no carrinho 
    generateCartItems();
    
    // console.log(basket);
    update(selectedItem.id);

    // salvando as quantidades na localStorage para não perder com refresh
    localStorage.setItem("data", JSON.stringify(basket));
};

let decrement = (id)=>{
    let selectedItem = id;
    console.log("decrementCart", selectedItem.id);
    let search = basket.find((x)=> x.id === selectedItem.id);

    if (search === undefined) return;  // cai fora se a basket está vazia
    else if (search.item === 0) return;
    else {
        search.item -= 1;
    }
    
    // console.log(basket);
    update(selectedItem.id);
    
    // filtrando o basket para deixar somente os items com quantidade (> 0)
    basket = basket.filter((x) => x.item != 0);

    // gerando novamente os itens no carrinho para quando a 
    // quantidade = 0 o quadro do item é removido da tela
    generateCartItems();

    // salvando as quantidades na localStorage para não perder com refresh
    localStorage.setItem("data", JSON.stringify(basket));
};

let incrementDiscountItem = (id)=>{
    let selectedItem = id;
    console.log("incrementDiscount", selectedItem.id);
};

let decrementDiscountItem = (id)=>{
    let selectedItem = id;
    console.log("decrementDiscount", selectedItem.id);
};

// let discountCartItem = (id)=>{
//     let selectedItem = id;
//     // let descontoItem = document.getElementById("discItem");
//     console.log("Desconto no Item", descontoItem);
//     let search = basket.find((x)=> x.id === selectedItem.id);
//     if (search === undefined) {
//         basket.push({ 
//             id: selectedItem.id,
//             item: 1,
//         });
//     } else {
//         search.discItem = descontoItem;
//         search.item += 1;
//     }
    
//     // gerando novamente os itens no carrinho para quando a 
//     // quantidade = 0 o quadro do item é removido da tela
//     generateCartItems();
    
//     // console.log(basket);
//     update(selectedItem.id);

//     // salvando as quantidades na localStorage para não perder com refresh
//     localStorage.setItem("data", JSON.stringify(basket));
// };


let update = (id)=>{
    let search = basket.find((x) => x.id === id);
    document.getElementById(id).innerHTML = search.item;
    calculation();
    totalAmount();
};

let removeItem = (id) => {
    if (confirm('Quer realmente eliminar este item?')) {
        let selectedItem = id;
        // console.log(selectedItem.id);
        basket = basket.filter((x) => x.id !== selectedItem.id);
        // gerando novamente os itens no carrinho para quando a 
        // quantidade = 0 o quadro do item é removido da tela
        generateCartItems();
        // atualiza a quantidade total da compra
        totalAmount();
        // atualiza o contador de itens comprados
        calculation();
        // salvando as quantidades na localStorage para não perder com refresh
        localStorage.setItem("data", JSON.stringify(basket));
    };
};

let clearCart = () => {
    if (confirm('Quer realmente limpar o carrinho?')) {
        // zera o conteúdo da cesta
        basket = [];
        generateCartItems();
        // atualiza o contador de itens comprados
        calculation();
        // salva as quantidades na localStorage para atualizar os valores
        localStorage.setItem("data", JSON.stringify(basket));
    };
};

let checkout = () => {
    if (basket.length !== 0) {
        if (confirm('Quer finalizar a compra?')) {
            console.log("====Salvando o conteúdo da cesta em arquivo externo..");
            let venda = localStorage.getItem("tipoDeVenda");
            console.log("Tipo de venda:", venda);
            let regFinal = [];
            basket.map((x) => {
                // console.log('x=', x);
                let { id, item } = x;
                let search = shopItemsData.find((x) => x.id === id) || []; 
                let { name, price} = search;
                let valorItem = price[tipo];
                let valorItemTotal = item * price[tipo];
                let reg = venda + ',' + id + ',' + name + ',' + item + ',' + valorItem + ',' + valorItemTotal;
                console.log(reg);
                regFinal += reg + '\n';
            }).join("");
            // console.log('registro final:\n', regFinal)
            var blob = new Blob([regFinal], { type: "text/plain;charset=utf-8" });
            saveAs(blob, "venda-feira2024.txt");
        };
    };
};

let totalAmount = () => {
    if (basket.length !== 0) {
        let amount = basket.map((x) => {
            let {item, id } = x;
            let search = shopItemsData.find((y) => y.id === id) || [];
            return item * search.price[tipo];
        }).reduce((x,y) => x+y, 0);
        let total = formatter.format(amount);
        console.log("Total da compra:", total);
        localStorage.setItem("totalCompra", total);
        if (tipo == 0) {
            localStorage.setItem("tipoDeVenda", 'CONSUMIDOR FINAL');
        } else if (tipo == 1) {
            localStorage.setItem("tipoDeVenda", 'LOJISTA');
        } else {
            localStorage.setItem("tipoDeVenda", 'BRINDE');
        }
        let venda = localStorage.getItem("tipoDeVenda");
        label.innerHTML = `
        <h1>Total: ${total}</h1>
        <h3 class="tipo-de-venda">⚠️ ${venda} </h3><br>
        <a href="loja.html"><button class="continuarComprando">Continuar Comprando</button></a>
        <button onclick="checkout()" class="checkout">Finalizar</button> 
        <button onclick="clearCart()" class="removeAll">Limpar Carrinho</button>
        `
    } else return
};
totalAmount();

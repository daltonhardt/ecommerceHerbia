let shop = document.getElementById('shop');

// lendo as quantidades da localStorage no caso de um refresh de página
// se o carrinho estiver vazio inicializa com um array vazio
let basket = JSON.parse(localStorage.getItem("data")) || [];

// guardando os dados do data.js
//let inventario = JSON.parse(localStorage.getItem("inventario"));
let estoque = JSON.parse(localStorage.getItem("inventario")) || [];

// busca da memória o tipo de venda (0, 1 ou 2)
let tipo = localStorage.getItem("tipoVenda");

// formatação moeda em REAL
const formatter = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  });

// função para gravar inventario no localStorage
let geraInventario = () => {
    shopItemsData.map((x) => {
        // console.log('shopItemsData =', x);
        inventario.push(x)
        localStorage.setItem("inventario", JSON.stringify(inventario));
    })
}
if (inventario = []) {
    geraInventario();
}

// Criando a função para gerar todos os itens da Loja
let generateShop =() => {
    return (shop.innerHTML = shopItemsData.map((x)=> {
        let { id, name, price, maxItemDiscount, itemStock, img} = x;

        // procura se o carrinho já tem algum produto e salva o ID na variavel search
        let search = basket.find((x) => x.id === id) || [];
        let valorItem = formatter.format(price[tipo]);
        return `
        <div id=product-id-${id} class="item">
            <img width="220" src=${img} alt="">
            <div class="details">
                <h2>${name}</h2>
                <div class="price-quantity">
                    <h3 class="cart-item-price">${valorItem}</h3>
                    <div class="plus-minus-buttons">
                        <i onclick="decrement(${id}, ${maxItemDiscount})" class="bi bi-dash-lg"></i>
                        <div id=${id} class="quantity">
                        ${search.item === undefined? 0: search.item}
                        </div>
                        <i onclick="increment(${id}, ${maxItemDiscount})" class="bi bi-plus-lg"></i>
                    </div>
                </div>
                Estoque: ${itemStock}
            </div>
        </div>
        `;
    }).join(""));
};
generateShop();  // chamando/rodando a função criada acima

// função para Aumentar a quantidade de produtos (sinal MAIS)
let increment = (id, maxItemDiscount)=>{
    //console.log('Loja increment ID:', id);
    //console.log('Loja increment max Item Disc.:', maxItemDiscount);
    let selectedItem = id;
    //console.log("Loja increment", selectedItem.id);
    
    let search = basket.find((x)=> x.id === selectedItem.id);
    //console.log('search:', search);

    // procurando se o produto já existe no carrinho
    if (search === undefined) {  // se não existe colocamos 1 unidade do produto no carrinho (push)
        basket.push({   
            id: selectedItem.id,
            item: 1,
            maxDesconto: maxItemDiscount,
            descontoItem: 0
        });
    } else {  // se o produto já existe no carrinho somente incrementa a quantidade
        search.item += 1;  // soma 1 na quantidade
    }
    
    //console.log('Increment basket:', basket);
    // chamando a função para atualizar o produto
    update(selectedItem.id);

    // salvando as quantidades na localStorage para não perder com refresh da página
    localStorage.setItem("data", JSON.stringify(basket));
};

// função para Diminuir a quantidade de produtos (sinal MENOS)
let decrement = (id)=>{
    let selectedItem = id;
    // console.log("decrement", selectedItem.id);
    let search = basket.find((x)=> x.id === selectedItem.id);

    if (search === undefined) return;  // cai fora se a cesta está vazia
    else if (search.item === 0) return;  //cai fora se a quantidade ZERO de produto
    else {
        search.item -= 1;  // diminui 1 na quantidade
    }
    
    //console.log('Decrement basket:', basket);

    // chamando a função para atualizar o produto
    update(selectedItem.id);
    
    // filtrando a cesta somente com os produtos com quantidade item diferente de zero
    basket = basket.filter((x) => x.item !== 0);

    // salvando as quantidades na localStorage para não perder com refresh da página
    localStorage.setItem("data", JSON.stringify(basket));
};

// função para atualizar o numero da quantidade do produto escolhido
let update = (id)=>{
    let search = basket.find((x) => x.id === id);  //procurando o produto na cesta
    // console.log(search.id, search.item, search.descontoItem);
    document.getElementById(id).innerHTML = search.item;
    calculation();
};

// função para somar todas as quantidades de produtos e mostrar no icone do Carrinho
let calculation =() => {
    let cartIcon = document.getElementById("cartAmount");
    cartIcon.innerHTML = basket.map((x) => x.item).reduce((y, z) => y+z, 0);
};
calculation();  // chamando/rodando a função acima quando der refresh na página

const apiBaseUrl = "https://your-app-name.onrender.com";

async function loadMenu() {
    let response = await fetch(`${apiBaseUrl}/menu`);
    let menu = await response.json();
    document.getElementById("menu").innerHTML = menu.map(item => `
        <div class="item">
            <img src="${item.img}" alt="${item.name}" width="100">
            <p>${item.name}</p>
            <button onclick="addToOrder(${item.id})">点菜</button>
        </div>
    `).join('');
}

let orderList = [];
function addToOrder(id) {
    orderList.push(id);
    document.getElementById("order-list").innerHTML = orderList.join(", ");
}

async function checkout() {
    await fetch(`${apiBaseUrl}/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: "your-email@qq.com", order: orderList })
    });
    alert("订单已提交！");
}

loadMenu();

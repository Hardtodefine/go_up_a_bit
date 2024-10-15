此代码用于**购物车系统**，该系统可以与两个不同的“适配器”交互，用于存储和检索购物车数据：一个适配器使用`localStorage`（客户端存储），另一个适配器与远程服务器通信。

```js
const localStorageAdapter = { 
  // 此适配器使用浏览器的`localStorage`在用户设备上本地保存和检索购物车数据。
  findAll: function (callback) {
    let cartList = JSON.parse(localStorage['cart'])
    // 检索存储在`localStorage['cart']`（在`'cart'`键下）中的所有购物车商品。
    callback(cartList)
    // 传递给`callback`函数
  },
  save: function (item) {
    let cartList = JSON.stringify(localStorage['cart'])
    cartList = cartList.split(',')
    // 从 `localStorage['cart']` 检索购物车列表，拆分为数组。
    console.log(cartList);
    cartList.push(item.title)
    localStorage['cart'] = JSON.stringify(cartList)
    // 使用 `JSON.stringify()` 将更新后的数组转换回字符串并保存回 `localStorage['cart']`。
  }
}

const serverAdapter = {
  // 此适配器与远程服务器通信以保存和检索购物车数据。
  findAll: function (callback) {
	// 它向 URL 发送 `GET` 请求以从服务器获取所有购物车项目。
	// 收到响应后，使用 `.json()` 将其转换为 JSON，并将数据传递给 `callback` 函数。
    fetch('https://jirengu.com/getCartList')
      .then(res => res.json())
      .then(data => callback(data))
  },
  save: function (item) {
      // 向 URL 发送 `POST` 请求，以将新商品添加到服务器上的购物车中。
    fetch('https://jirengu.com/addToCart', { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(item) })
      .then(res => res.json())
      // `item` 在请求正文中以 JSON 形式发送。
      .then(data => callback(data))
  }
}

class ShoppingCart {
    // 此类用于管理购物车，抽象出购物车存储方式（无论是本地存储还是服务器存储）的细节。
  constructor(adapter) {
    this.adapter = adapter
      // 该类接受适配器（`localStorageAdapter` 或 `serverAdapter`）并将其分配给 `this.adapter`。
      // 这允许购物车使用 `localStorage` 或服务器，具体取决于传递了哪个适配器。
  }
  add(item) {
      // 调用适配器的 `save()` 函数，将提供的 `item` 保存到购物车（在 `localStorage` 中或服务器上，具体取决于适配器）。
    this.adapter.save(item)
  }
  show() {
    // 调用适配器的 `findAll()` 函数检索所有购物车商品。
	// 购物车商品通过将其传递给 `callback` 函数（在本例中为 `console.log`）记录到控制台。
    this.adapter.findAll(list => {
      console.log(list)
    })
  }
}


let cart = new ShoppingCart(localStorageAdapter)
//let cart = new ShoppingCart(serverAdapter)
cart.add({ title: '手机' })
cart.add({ title: '电脑' })
cart.show()
// 将两个项目（`手机`，表示“电话”，和`电脑`，表示“电脑”）添加到购物车，然后在控制台中显示购物车的内容。
```

### 要点：
- **适配器** 使购物车系统灵活，并可以使用不同的存储方法（`localStorage` 或服务器）。
- **回调** 用于处理异步任务，例如从 `localStorage` 或远程服务器检索数据。
- 该系统可以通过更改 `ShoppingCart` 构造函数中的适配器，轻松地在本地和基于服务器的存储之间切换。

### 它如何适合适配器模式：

适配器模式用于允许两个不兼容的接口协同工作。在这种情况下，ShoppingCart 类期望与特定接口交互以保存和检索购物车项目（通过 add() 和 show() 方法）。但是，存储方法（无论是本地存储还是服务器端存储）具有不同的实现。

适配器（localStorageAdapter 和 serverAdapter）充当符合相同接口的中介，允许 ShoppingCart 类与不同的存储系统交互而无需了解其具体细节。

### 代码中适配器模式的关键元素：

目标接口：ShoppingCart 期望其适配器提供两种方法：

findAll(callback)：检索购物车中的所有项目。
save(item)：将新项目保存到购物车。
localStorageAdapter 和 serverAdapter 都符合此预期接口，尽管它们以不同的方式处理存储（本地存储与服务器 API）。

适配器：

localStorageAdapter：通过与 localStorage 交互来实现接口。
serverAdapter：实现相同的接口，但通过 HTTP 请求与远程服务器通信。
ShoppingCart（客户端）： ShoppingCart 类不需要知道它是在使用 localStorage 还是服务器；它只需在其适配器上调用 save() 和 findAll() 方法，适配器会处理具体细节。这允许购物车与存储无关。

此代码中适配器模式的优势：
灵活性：只要适配器实现预期的接口， ShoppingCart 类就可以与任何存储系统一起使用。您可以添加新的适配器（例如，用于 IndexedDB 或会话存储），而无需更改 ShoppingCart 类。
关注点分离： ShoppingCart 类仅专注于管理购物车项目，而存储逻辑则被抽象到适配器中。
可互换性：您只需更改 ShoppingCart 构造函数中的适配器即可在 localStorageAdapter 和 serverAdapter 之间切换，而无需修改核心购物车逻辑。
总之，此代码是适配器模式实际应用的一个清晰示例，允许 ShoppingCart 以灵活且可维护的方式使用不同的存储机制。
### 面向对象编程

```js
原始代码

function startAnimation() {
    console.log('start animation')
}
function stopAnimation() {
    console.log('stop animation')
}
改为面向对象的方式

var Anim = function() {
}
Anim.prototype.start = function() {
    console.log('start animation')
}
Anim.prototype.stop = function() {
    console.log('stop animation')
}
var myAnim = new Anim()
myAnim.start()
myAnim.stop()
变形简化

var Anim = function() {}
Anim.prototype = {
    start: function() {
        console.log('start')
    },
    stop: function() {
        console.llog('end')
    }
}
持续改进

Function.prototype.method = function(name, fn) {
    this.prototype[name] = fn
}
var Anim = function() {
}
Anim.method('start', function() {
    console.log('start animation')
})
Anim.method('stop', function() {
    console.log('stop animation')
})
持续改进，链式调用

Function.prototype.method = function(name, fn) {
    this.prototype[name] = fn
    return this
}
var Anim = function() {}
Anim.method('start', function() {
    console.log('start animation')
}).method('stop', function() {
    console.log(stop animation')
})
```



### 匿名函数

> 没有名字的函数

### 自调用函数

```js
(function(a1,a2){
  console.log(a1*a2)
})(1,2)

//上面和下面是一样的

var a = function(foo,bar){
  console.log(foo*bar)
}
a(1,2)
```

### 闭包

> 访问函数内部的局部变量

```js
var baz; 
(function(){
  var value1 = 1
  var value2 = 2
  baz = function(){
    return value1*value2
  }
})();
baz();
console.log(baz())
```



### JS函数的返回值

1. **所有函数都有返回值**：即使函数体中没有显式地使用 `return` 语句，JavaScript 也会隐式地返回 `undefined`。
2. **函数的返回值由什么确定**：
   - **调用时输入的参数**：某些函数的返回值可能依赖于传入的参数。
   - **定义时的环境**：函数内部的逻辑决定了返回值，包括变量的作用域、条件判断等。

### 子程序与方法

3. **子程序**：如果一个函数有返回值，则称为函数。
4. **过程**：如果一个函数没有返回值，则称为过程。
5. **方法**：当一个函数作为对象的属性时，称其为方法。

### `this` 的一些问题

6. **`this` 的绑定规则**：
   - 默认绑定：全局环境中，默认 `this` 指向全局对象（浏览器中是 `window`，Node.js 中是 `global`）。
   - 隐式绑定：当函数作为对象的方法调用时，`this` 绑定到该对象。
   - 显式绑定：使用 `call`、`apply` 或 `bind` 方法可以显式地改变 `this` 的绑定。
   - 新绑定：使用 `new` 关键字调用构造函数时，`this` 绑定到新创建的对象。

### 原型链

7. **原型链的概念**：原型链是通过对象的 `__proto__` 属性连接起来的一系列对象。
8. **字面量方式创建对象**：
   ```javascript
   var a = {};
   console.log(a.__proto__);  // Object {}
   console.log(a.__proto__ === a.constructor.prototype); // true
   ```
9. **构造器方式创建对象**：
   ```javascript
   var A = function() {};
   var a = new A();
   console.log(a.__proto__);  // A {}
   console.log(a.__proto__ === a.constructor.prototype); // true
   ```
10. **`Object.create` 方式创建对象**：
    ```javascript
    var a1 = {a: 1};
    var a2 = Object.create(a1);
    console.log(a2.__proto__);  // Object {a: 1}
    console.log(a2.__proto__ === a1); // true
    console.log(a2.__proto__ === a2.constructor.prototype); // false
    ```

### 构造函数与实例对象

11. **构造函数**：构造函数是一种特殊的函数，通常用于创建对象实例。
    ```javascript
    function Student(name, age, gender) {
      this.name = name;
      this.age = age;
      this.gender = gender;
      this.sayHi = function() {
        console.log('hello ' + this.name);
        console.log(this);
      };
    }
    var stu1 = new Student('zs', 18, 'male');
    ```
12. **`this` 的绑定**：在构造函数中，`this` 指向新创建的对象实例。
    
    ```javascript
    var stu1 = new Student('zs', 18, 'male');
    stu1.sayHi();  // 输出: hello zs 和 stu1 对象
```
    
13. **错误示例**：如果不使用 `new` 关键字调用构造函数，`this` 将指向全局对象（通常是 `window`），这可能会导致意外的结果。
    ```javascript
    var stu1 = Student('zs', 18, 'male');  // 错误示例
    // 此时 `this` 指向 `window`，而不是新创建的对象
    ```

### 总结

- **函数的返回值**：所有函数都有返回值，如果没有显式返回则默认返回 `undefined`。

- **子程序与方法**：有返回值的是函数，没有返回值的是过程，作为对象属性的是方法。

- **`this` 的绑定**：取决于调用方式，默认绑定、隐式绑定、显式绑定和新绑定。

- **原型链**：通过 `__proto__` 属性连接的一系列对象，用于继承和属性查找。

- **构造函数与实例对象**：构造函数用于创建对象实例，`new` 关键字确保 `this` 绑定到新创建的对象。

  **@ts-ignore**

  > 可以忽略下面第一行的报错


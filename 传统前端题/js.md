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


### 总结

- **函数的返回值**：所有函数都有返回值，如果没有显式返回则默认返回 `undefined`。
- **子程序与方法**：有返回值的是函数，没有返回值的是过程，作为对象属性的是方法。
- **原型链**：通过 `__proto__` 属性连接的一系列对象，用于继承和属性查找。



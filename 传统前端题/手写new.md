```js
// Function prototype
function printMessage(message) {
  console.log(message);
}

function myNew(func, ...args) {
  // Create a new object with the prototype of the given function
  const newObj = Object.create(func.prototype);

  // Call the given function with the new object as the context
  const result = func.apply(newObj, args);

  // If the function returns an object, return that object
  if (typeof result === 'object' && result !== null) {
    return result;
  }

  // Otherwise, return the new object
  return newObj;
}

// Usage
function Person(name) {
  this.name = name;
}

Person.prototype.greet = function() {
  console.log(`Hello, my name is ${this.name}`);
};

const john = myNew(Person, 'John');
john.greet(); // Output: Hello, my name is John


```

在此示例中，我们有一个名为 myNew 的函数，它充当 JavaScript 中 new 关键字的自定义实现。 它采用函数 func 作为第一个参数以及将传递给该函数的任何其他参数 …args。
在 myNew 函数中，我们使用 Object.create(func.prototype) 创建一个新对象 newObj。 这将创建一个具有给定函数原型的新对象，允许新对象从函数原型继承属性和方法。
接下来，我们使用 func.apply(newObj, args) 以新对象作为上下文调用给定函数 func。 这确保了函数以新对象的形式执行，从而允许它修改新对象的属性。
如果函数 func 返回一个对象，我们就返回该对象。 否则，我们返回新对象 newObj。
在使用示例中，我们定义了一个构造函数 Person，它在新创建的对象上设置 name 属性。 我们还向 Person 原型添加了一个greet 方法。
使用 myNew，我们创建一个名为“John”的新 Person 对象 john。 然后我们可以调用 john 上的greet 方法，该方法将“Hello, my name is John”输出到控制台。

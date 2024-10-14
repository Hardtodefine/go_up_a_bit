```js
function MyPromise(executor) {
  // Initial state of the promise
  let state = 'pending';
  let value = undefined;
  let handlers = [];

  function resolve(result) {
    if (state !== 'pending') {
      return;
    }

    state = 'fulfilled';
    value = result;

    // Execute all the registered fulfillment handlers
    handlers.forEach(handler => handler.onFulfilled(value));
    handlers = [];
  }

  function reject(error) {
    if (state !== 'pending') {
      return;
    }

    state = 'rejected';
    value = error;

    // Execute all the registered rejection handlers
    handlers.forEach(handler => handler.onRejected(value));
    handlers = [];
  }

  this.then = function(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      function handle(value) {
        try {
          const result = onFulfilled(value);
          resolve(result);
        } catch (error) {
          reject(error);
        }
      }

      function handleError(error) {
        try {
          const result = onRejected(error);
          resolve(result);
        } catch (error) {
          reject(error);
        }
      }

      if (state === 'fulfilled') {
        handle(value);
      } else if (state === 'rejected') {
        handleError(value);
      } else {
        handlers.push({
          onFulfilled: handle,
          onRejected: handleError
        });
      }
    });
  };

  // Execute the executor function
  try {
    executor(resolve, reject);
  } catch (error) {
    reject(error);
  }
}

```

在此示例中，我们定义了一个 MyPromise 函数，它将执行器函数作为参数。 执行器函数被立即调用并接收两个函数：resolve 和reject，作为参数。 这些函数用于将承诺转换为已完成或已拒绝状态。
在 MyPromise 函数内部，我们维护 Promise 的状态（“pending”、“fulfilled”或“rejected”）、解析值（value）以及 Promise 结算时将执行的处理程序（handlers）数组 。
解决函数通过将状态设置为“已完成”并存储已解决的值，将承诺转换为已完成状态。 然后，它通过使用解析值调用 onFulfilled 函数来执行所有已注册的履行处理程序。
拒绝函数通过将状态设置为“拒绝”并存储拒绝原因，将 Promise 转换为拒绝状态。 然后，它通过调用带有拒绝原因的 onRejected 函数来执行所有已注册的拒绝处理程序。
then 方法用于注册 Promise 的履行和拒绝处理程序。 它返回一个新的 MyPromise 实例，允许链接 then 调用。 在 then 方法中，我们创建一个新的 Promise 并定义两个内部函数，handle 和 handleError，分别处理履行和拒绝情况。
如果承诺已经履行，我们立即使用解析值调用句柄函数。 如果promise已经被拒绝，我们立即调用handleError函数并给出拒绝原因。 否则，我们将包含handle和handleError函数的对象推送到handlers数组，该数组将在promise结算时执行。
最后，我们执行执行器函数，将resolve和reject函数作为参数传递。 我们将执行包装在 try-catch 块中，以处理执行程序函数执行期间发生的任何同步错误。
请注意，这是 Promise 功能的简化实现，不包括链接、错误传播或异步行为等功能。 它作为 Promise 如何实现的基本演示。


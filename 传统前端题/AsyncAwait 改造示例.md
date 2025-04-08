# Async/Await 改造示例

## 示例1：回调函数改造
### 改造前代码

```js
readCardFun() {
    this.$sdk.request().then((res) => {
        this.entryQueryFun()
    })
}
```

### 改造后代码

```js
async readCardFun() {
    const res = await this.$sdk.request()
    await this.entryQueryFun()
}
```

改进点 ：

1. 移除了 .then() 嵌套，代码更扁平
2. 使用 await 使异步代码看起来像同步代码
3. 错误可以通过 try/catch 统一处理
## 示例2：Promise链式调用改造

### 改造前代码
```javascript
entry() {

    const obj = {
        no: this.no
    }
    entryStation(obj).then(res => {
        // ...处理逻辑...
    })
}
```

### 改造后代码

```js
async entry() {
    const obj = {
        no: this.no
    };

    try {
        const res = await entryStation(obj);
        // ...处理逻辑...
        return res;
    } catch (error) {
        // ...错误处理...
        throw error;
    }
}
```

改进点 ：

1. 使用 async/await 替代 .then() 链式调用
2. 添加了 try/catch 错误处理机制
3. 通过 return 返回结果，使调用方可以获取异步结果
4. 代码结构更线性，避免了回调嵌套

## 最佳实践

1. 需要 await 的函数必须声明为 async
2. 多个有依赖关系的异步操作应该顺序 await
3. 使用 try/catch 处理错误
4. 避免不必要的 async 嵌套
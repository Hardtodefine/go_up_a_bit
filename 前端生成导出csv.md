前端导出下载CSV

### CSV格式介绍

以逗号分隔数据,/n分隔每一行, 实际csv格式就是多行数据的集合 对csv格式的理解应该着重于每一行数据和表头是否对的上,数据后面空白可以不用补 数据格式是来自于后端

```js
js 代码解读复制代码var data = [
{a:1,b:1,c:1,user_question:{name:1,age:1}},
{a:2,b:2,c:2,user_question:{gender:3,minggw:2}},
{a:3,b:3,c:3,user_question:{age:4,dev:3}},
{a:4,b:4,c:4,user_question:{gcc:4,echo:4}},
{a:5,b:5,c:5,user_question:{name:5,age:5}},
]
```

a,b,c是固定表头项, 由于user自定义数据每次提交可能有或者没有,或者只有其中几项,因此先遍历一次data拿出所有的 user_question的key值,

```js
js 代码解读复制代码dataToCSV(arr) {
            let headers = ['时间','B','C'];
            let custom_headers = [];
            let csv = '';
          
            arr.forEach((obj,index) => {
                if (obj.user_question && typeof obj.user_question === 'object' && !Array.isArray(obj.user_question)) {
                let objKeys = Object.keys(obj.user_question);
                objKeys.forEach(key => {
                    if (!headers.includes(key)) {
                    headers.push(key);
                    custom_headers.push(key);
                    }
                });
                let solidrow = []
                solidrow.push(obj.a?new Date(Number(obj.a)):'')
                solidrow.push(obj.b?obj.b:'')
                solidrow.push(obj.c?obj.c:'')
                solidrow = solidrow.join(',')
                let row = custom_headers.map(key => this.resolvekey(obj.user_question,key) || '').join(',');
                csv += (solidrow+','+row) + '\n';
                    }
            });
            let headersString = headers.join(',') + '\n';
            csv = headersString + csv;
            return csv
        },
```

这里的判断是有user_question再加固定表头,实际可根据情况调整;

这里的headers是总的表头; custom_headers是单列的自定义表头;

单列是方便对每个数据的自定义部分(custom_headers)做遍历; 下面是点击下载csv的代码

```js
js 代码解读复制代码var uri = this.dataToCSV(data);
let blob = new Blob(['\ufeff'+uri], { type: "data:text/csv;charset=utf-8" });
let a = document.createElement("a");
a.href = window.URL.createObjectURL(blob);
a.download = '导出'+ new Date().getTime() + ".csv";
document.body.appendChild(a);
a.dispatchEvent(new MouseEvent('click'));
document.body.removeChild(a);
```

下载后发现excel打开有中文乱码问题

### 导出下载后excel乱码

优点

是不用用户自己使用记事本另存为ANSI或者excel从CSV导入这类命令

缺点

代码再次读取时每行都有\ufeff 原因是在下载CSV这里要加一个BOM头,即字节顺序标记,用于识别文件编码;

下面是参考资料

[blog.csdn.net/lonelymanon…](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2Flonelymanontheway%2Farticle%2Fdetails%2F117649518)
前端生成XLSX并且下载 记住表格格式是XLSX,不要写成XLSX(笑死了),不然真会被同事笑 官方文档地址(建议读一下)

[Arrays of Data | SheetJS Community Edition](https://link.juejin.cn?target=https%3A%2F%2Fdocs.sheetjs.com%2Fdocs%2Fapi%2Futilities%2Farray%2F)

首先两个方法

```js
js 代码解读复制代码import XLSX from 'xlsx';
var worksheet = XLSX.utils.aoa_to_sheet(aoa);
var workbook = XLSX.utils.book_new();
```

sheet是一张表,xlsx与csv不同的是xlsx允许有多张表,而不只是一张表格, 输入生成表格的数据有

- `aoa_to_sheet` 把转换JS数据数组的数组为工作表。
- `json_to_sheet` 把JS对象数组转换为工作表。
- `table_to_sheet`把DOM TABLE元素转换为工作表 下面是三个 tabletosheet的案例

[elementUi—table组件+xlsx插件实现导出——sheetJs——前端实现表格的导出功能——技能提升_element 表格插件_叶浩成520的博客-CSDN博客](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2Fyehaocheng520%2Farticle%2Fdetails%2F123554455%3Fspm%3D1001.2014.3001.5501)

[使用js-xlsx纯前端导出excel - 爱码网 (likecs.com)](https://link.juejin.cn?target=https%3A%2F%2Fwww.likecs.com%2Fshow-203708170.html)

[sheetJs+xlsx-style——前端实现导出excel表格——设置单元格背景色，居中，自动换行，宽度，百分数展示等_sheetjs cellstyles_叶浩成520的博客-CSDN博客](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2Fyehaocheng520%2Farticle%2Fdetails%2F123641456)

我使用的是aoatosheet

```js
js 代码解读复制代码var data = [
{a:1,b:1,c:1,user_question:{name:1,age:1}},
{a:2,b:2,c:2,user_question:{gender:3,minggw:2}},
{a:3,b:3,c:3,user_question:{age:4,dev:3}},
{a:4,b:4,c:4,user_question:{gcc:4,echo:4}},
{a:5,b:5,c:5,user_question:{name:5,age:5}},
]
// 合并数据
combineArray(object,key){
    if (Array.isArray(object[key])) {
        object[key] = object[key].join('，')
    }
    return object[key]
},
convertToaoa(){
let headers = ['时间','B','C'];
let user_ques = [];
let aoa = [];
arr.forEach((obj) => {
            if (obj.user_question && typeof obj.user_question === 'object' && !Array.isArray(obj.user_question)) {
            let solid_col = []
            solid_col.push(obj.a?new Date(Number(obj.a)):'')
            solid_col.push(obj.b?obj.b:'')
            solid_col.push(obj.c?obj.c:'')
            let col = []
            for (let index = 0; index < custom_headers.length; index++) {
                const element = custom_headers[index];
                if(this.resolvekey(obj.user_question,element)){
                        col.push(this.combineArray(obj.user_question,element))
                    }else{
                        col.push(null)
                    }
            }
            aoa.push(solidcol.concat(col))
            }
        });
        aoa.unshift(headers)
        return aoa
}
输出的数据是二维数组,具体可看文档
```

最后是合成表并且下载

```js
js 代码解读复制代码XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");
XLSX.writeFile(workbook,"test.xlsx");
```

另外还有一个合并单元格的例子

```js
js 代码解读复制代码....
// 变量ws即worksheet
// 变量wb即workbook
var wb = XLSX.utils.book_new();
// ws['!ref'] = `A1:AI${aoa.length}`;
// s 意为 start ，即开始的单元格
// r 是 row ，表示行号，从 0 计起
// c 是 col ，表示列号，从 0 计起
const merge = [
  // 纵向合并，范围是第1列的行1到行2
  { s: { r: 0, c: 0 }, e: { r: 1, c: 0 } },
  // 纵向合并，范围是第2列的行1到行2
  { s: { r: 0, c: 1 }, e: { r: 1, c: 1 } },
  // 横向合并，范围是第1行的列3到列5
  { s: { r: 0, c: 2 }, e: { r: 0, c: 4 } },
  // 横向合并，范围是第1行的列6到列11
];
ws['!merges'] = merge;
XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
......
```

[SheetJS（js-xlsx、XLSX）横向纵向合并单元格 - 知乎 (zhihu.com)](https://link.juejin.cn?target=https%3A%2F%2Fzhuanlan.zhihu.com%2Fp%2F141328581)

尝试了一下,合并单元格时,设置ref并不必要,同样成功合并
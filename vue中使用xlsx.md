### 函数目的

使用 `file-saver` 和 `xlsx` 库导出 HTML 表格为 Excel 文件。

### 重构后的代码

```js
// 引入导出Excel表格的依赖
import FileSaver from "file-saver";
import XLSX from "xlsx";

exportExcel() {
    // 生成工作簿对象
    const workbook = XLSX.utils.table_to_book(document.querySelector("#out-excel"));
    
    // 将工作簿转换为二进制数组
    const binaryOutput = XLSX.write(workbook, {
        bookType: "xlsx",
        bookSST: true,
        type: "array"
    });

    try {
        // 创建 Blob 对象并触发下载
        FileSaver.saveAs(
            new Blob([binaryOutput], { type: "application/octet-stream" }),
            "sheetjs.xlsx" // 设置导出文件名称
        );
    } catch (error) {
        // 错误处理
        if (typeof console !== "undefined") {
            console.log(error, binaryOutput);
        }
    }
    return binaryOutput; // 返回二进制数据
}

```

### 代码说明

1. **模块导入**：引入需要的库 `file-saver` 和 `xlsx`。
2. **工作簿生成**：使用 `XLSX.utils.table_to_book` 方法将 HTML 表格转换为工作簿对象。
3. **二进制转换**：通过 `XLSX.write` 方法将工作簿转换为二进制数组。
4. **文件下载**：使用 `FileSaver.saveAs` 创建 Blob 对象并触发文件下载。
5. **错误处理**：捕获并记录可能的错误。
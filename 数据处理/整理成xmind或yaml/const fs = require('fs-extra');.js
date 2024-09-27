const fs = require('fs-extra');
// 页面路由来源代码为route.js经过导出处理过的
const parsedRoutes = routes[0].children.reduce((acc, route) => {
  // Check if meta and name exist
  if (route.meta && route.meta.name) {
    let componentPathMatches = route.component.toString().match(/'([^']+)'/g).map(match => match.replace(/'/g, ''))
    let componentPath = componentPathMatches ? componentPathMatches[0] : '';

    console.log(componentPathMatches);
    acc.push({
      [route.meta.name]: {
        '路径': route.path,
        '组件': componentPath
      }
    });
  }
  
  return acc;
}, []);
fs.outputFile('结果.ini', JSON.stringify(parsedRoutes, null, 2))
  .then(() => console.log('The file has been saved!'))
  .catch(err => console.error(err));


const filePath = './页面路由.ini'; 
let fileContent = fs.readFileSync(filePath, 'utf-8');


// 读取'./结果.ini'文件的内容
const resultContent = fs.readFileSync('./结果.ini', 'utf-8');
let resultArray = JSON.parse(resultContent);

// 测试数据
// let resultArray = [
//     {
//         "stat管理": {
//           "路径": "corp/:corp/stat",
//           "组件": "@/views/stat.gl"
//         }
//       },
//     {
//         "stat详情": {
//           "路径": "corp/:corp/stat",
//           "组件": "@/views/stat.xq"
//         }
//       },
// ]

// 对相同key进行去重
let keys = [];
resultArray = resultArray.filter(item => {
  const key = Object.keys(item)[0];
  if (keys.includes(key)) {
    return false;
  } else {
    keys.push(key);
    return true;
  }
});

// 遍历结果.ini
for (let item of resultArray) {
    const key = Object.keys(item)[0];

    // 定义要添加的新项
    const newItem = `${key}\r\n\t路径:${item[key]["路径"]}\r\n\t组件:${item[key]["组件"]}`;
    // 查找上一项的缩进
    const currentIndex = fileContent.indexOf(key);
    const lastItemRegex = /(\t+)/g;
    const itemMatchs = fileContent.slice(0, currentIndex).match(lastItemRegex);
    const itemMatchsArray = [...itemMatchs]
    const lastItemIndent = itemMatchsArray[itemMatchsArray.length - 1].length;

    // 添加新项并计算缩进
    const indentedNewItem = newItem
      .split('\n')
      .map((line, index) => {
        return index > 0 ? '\t'.repeat(lastItemIndent) + line : '\t'+line
      })
      .join('\n');
    // 替换内容,使用正则表达式进行全词匹配
    const regex = new RegExp('(?:^|\\s)' + key + '(?:\\s|$)', 'g');
    fileContent = fileContent.replace(regex, indentedNewItem)
}

fs.writeFile(filePath, fileContent, 'utf-8');
// 将更新后的内容写回文件

// console.log('替换完成！');
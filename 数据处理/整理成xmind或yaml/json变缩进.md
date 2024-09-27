导出实现路由表的脑图
先处理源数据成数组
let resultArray = [
    {
        "stat管理": {
          "路径": "corp/:corp/stat",
          "组件": "@/views/stat.gl"
        }
      },
    {
        "stat详情": {
          "路径": "corp/:corp/stat",
          "组件": "@/views/stat.xq"
        }
      },
]
再把转为缩进的yaml或者xmind的可导入格式
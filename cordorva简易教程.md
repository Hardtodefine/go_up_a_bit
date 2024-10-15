Apache Cordova 是一个开源框架，允许开发者使用标准的 Web 技术（HTML、CSS 和 JavaScript）来构建跨平台的移动应用程序。本教程将引导您完成使用 Cordova 创建一个新的 Android 应用程序的过程。

#### 准备工作

1. **安装Node.js**： 确保您的计算机上已安装 Node.js。您可以从 [Node.js 官方网站](https://nodejs.org/) 下载并安装最新版本。

2. **检查Node.js和npm是否正确安装**： 打开命令行工具（Windows 用户可以使用 `cmd` 或 `PowerShell`，Mac 和 Linux 用户可以使用终端），然后输入以下命令来验证安装：


   ```bash
   node -v
   npm -v
   ```

#### 创建Cordova项目

1. **全局安装Cordova**： 如果您还没有安装 Cordova，可以通过 npm 来安装它。打开命令行工具，执行以下命令：


   ```bash
   npm install -g cordova
   ```

2. **创建新项目**： 使用 `cordova create` 命令创建一个新的 Cordova 项目。此命令需要三个参数：项目目录、包名和应用名称。


   ```bash
   cordova create MyApp com.example.myapp MyApp
   ```

   这个命令会在当前目录下创建一个名为 `MyApp` 的文件夹，其中包含了一个基础的 Cordova 项目结构。

3. **进入项目目录**：


   ```bash
   cd MyApp
   ```

#### 添加Android平台

1. 添加Android平台

   ： 在项目根目录下，运行以下命令来添加 Android 平台支持：


   ```bash
   cordova platform add android
   ```

#### 安装插件

1. 添加权限插件

   ： 某些应用可能需要访问设备上的特定资源，比如相机或位置信息。为了请求这些权限，我们可以安装

    

   ```bash
   cordova-plugin-android-permissions
   ```

    

   插件：


   ```bash
   cordova plugin add cordova-plugin-android-permissions
   ```

#### 运行应用

1. 运行应用到模拟器或设备

   ： 要在连接的 Android 设备上运行应用，或是在模拟器中启动应用，请使用以下命令：


   ```bash
   cordova run android
   ```

   如果这是第一次运行，Cordova 可能会提示您安装一些必要的 Android SDK 组件。请按照提示操作。

#### 查看已安装的依赖

如果您想查看当前项目中已经安装的 Cordova 相关依赖，可以使用 npm 的 `list` 命令：

```bash
npm list --depth=0
```

这个命令会列出项目中顶层的 npm 包，包括 Cordova 及其插件。

#### 总结

通过以上步骤，您已经成功创建了一个简单的 Cordova 应用程序，并将其部署到了 Android 设备或模拟器上。接下来，您可以开始自定义您的应用，添加更多的功能和插件，以满足您的需求。

#### 注意事项

- 确保您的开发环境已经配置好了 Android 开发所需的工具链，包括 JDK、Android SDK 和 Android Studio。

- 在实际开发过程中，可能需要根据项目的具体需求调整 Cordova 版本。例如，您可能想要安装特定版本的 Cordova：


  ```bash
  npm install -g cordova@9.0.0
  ```

- 如果遇到任何问题，可以查阅 [Cordova 官方文档](https://cordova.apache.org/docs/en/latest/) 获取更多信息和支持。
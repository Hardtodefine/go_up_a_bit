先从一道面试题说起,Yarn解决了npm的什么问题?

1.安装速度

从安装速度来看，Yarn 比 npm 更快，因为它使用了并行下载机制，可以在下载时同时安装多个包。

而npm安装插件是从国外服务器进行下载,而且是处理完一个包再处理下一个包,这造成了两个包管理器安装的差异

目前yarn官方源和npm官方源的地址都在cloudflare,可以通过改为国内源或者使用cnpm来提升单个包下载速度

2.安装版本差异

"1.0.1"   # 表示安装指定的1.0.1版本
"~1.0.1"  # 表示安装1.0.X中最新的版本
"^1.0.1"  # 表示安装1.X.X中最新的版本
这造成不同时间安装的1.x.x的最新版本可能不同,而yarn在安装包时候会在lock file文件记下每一个包的安装版本,换句话yarn会默认生成锁定文件

目前也有package-lock.json实现类似的功能npm 5已经支持

3.早期npm的树形结构,后续npm@3.x已经支持(2015)

早期node_modules是嵌套的,这种结构问题在于会复制同样的依赖很多次,占据大量空间

还会超过windows路径最多260个字符的路径长度限制

yarn给出了扁平化的目录结构

4.不支持离线模式,后续npm@5已经支持(2017.5)

离线模式指安装过的包会被保存进缓存目录,下次安装直接从文件夹缓存中复制过来

这样会提升安装速度,避免不必要的重复下载,但是会占用一些空间

yarn支持而早期npm不支持

5.简洁的输出

npm的输出信息较为复杂,而且在安装时会不断打印出所有被安装上的依赖

而yarn的输出就仅是必要而简洁的输出

6.语义化的命令

早期npm安装时会有--save等参数来确定是否是开发时依赖

yarn的命令语义化更为直观,例如增加包是add,安装所有包是install,移除包是remove

7.npx命令npm@5.2已经支持(2017.7)

下面是AI自动生成的一些回答

npm 安装包（packages）的速度不够快，拉取的 packages 可能版本不同。Yarn 解决了早期 npm 的一些问题，

如：不支持离线模式、树形结构的依赖、依赖安装不确定性、项目版本不一致问题等 。

从安装速度来看，Yarn 比 npm 更快，因为它使用了并行下载机制，可以在下载时同时安装多个包。从命令简洁性来看，Yarn 和 npm 都很强大，但是 Yarn 的命令更加简洁明了。从 yarn.lock 特性来看，yarn.lock 是一个锁定文件，用于确保在不同环境中安装相同的依赖版本。

参考资料

https://blog.csdn.net/qq_22187895/article/details/128922310
https://blog.csdn.net/qq_36213140/article/details/122587887
https://www.zhihu.com/question/279744446
https://blog.csdn.net/vcit102/article/details/124407207
https://zhuanlan.zhihu.com/p/598365176
https://zhuanlan.zhihu.com/p/346998633
https://www.nowcoder.com/discuss/491681563780956160
https://zhuanlan.zhihu.com/p/571182880?utm_id=0

### 基础 

CSS2.1中只有BFC和IFC
 CSS3中才有GFC和FFC

###  BFC 

BFC（Block Formatting Contexts）直译为“块级格式化上下文”。Block Formatting Contexts就是页面
上的一个隔离 的渲染区域，容器里面的子元素不会在布局上影响到外面的元素，反之也是如此。如何产
生BFC？
float的值不为none。 overflow的值不为visible。 position的值不为relative和static。
display的值为table-cell，table-caption，inline-block中的任何一个。
那BFC一般有什么用呢？比如常见的多栏布局，结合块级别元素浮动，里面的元素则是在一个相对隔离
的环境里运行。

### IFC 

IFC（Inline Formatting Contexts）直译为“内联格式化上下文”，IFC的line box（线框）高度由其包含行
内元素中最 高的实际高度计算而来（不受到竖直方向的padding／margin影响）
IFC中的line box一般左右都贴紧整个IFC，但是会因为float元素而扰乱。float元素会位于IFC与与line 
box之间，使 得line box宽度缩短。同个lfc下的多个line box高度会不同。IFC中时不可能有块级元素
的，当插入块级元素时
（如p中插入div）会产生两个匿名块与div分隔开，即产生两个IFC，每个IFC对外表现为块级元素，与div
垂直排列。
那么IFC一般有什么用呢？
水平居中：当一个块要在环境中水平居中时，设置其为inline—block则会在外层产生IFC，通过text—
 align则可以使其水平居中。
垂直居中：创建一个IFC，用其中一个元素撑开父元素的高度，然后设置其vertical—align：middle，其
他行内元素则可以在此父元素下垂直居中。

### GFC 

GFC（GridLayout Formatting Contexts）直译为“网格布局格式化上下文”，当为一个元素设置display
值为grid的时 候，此元素将会获得一个独立的渲染区域，我们可以通过在网格容器（grid container）上
定义网格定义行（griddefinition rows）和网格定义列（grid definition columns）属性各在网格项目
（grid item）上定义网格行（grid row）和网格列（grid columns）为每一个网格项目（grid item）定
义位置和空间。
那么GFC有什么用呢，和table又有什么区别呢？首先同样是一个二维的表格，但GridLayout会有更加丰
富的属性来控制行列，控制对齐以及更为精细的渲染语义和控制。

### FFC 

FFC（Flex Formatting Contexts）直译为“自适应格式化上下文”，display值为flex或者inline-flex的元素
将会生成自 适应容器（flex container），可惜这个牛逼的属性只有谷歌和火狐支持，不过在移动端也
足够了，至少safari和chrome还是OK的，毕竟这俩在移动端才是王道。
Flex Box 由伸缩容器和伸项目组成。通过设置元素的display属性为flex或 inline—flex 可以得到一个伸
缩容器。设置为flex的容器被渲染为一个块级元素，而设置为inline—flex的容器则渲染为一个行内元
素。
伸缩容器中的每一个子元素都是一个伸缩项目。伸缩项目可以是任意数量的。伸缩容器外和伸缩项目内
的一切元素都不受影响。简单地说，Flexbox定义了伸缩容器内伸缩项目该如何布局。
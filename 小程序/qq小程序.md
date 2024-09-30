#### 获取qq群api

```js
// 获取小程序的启动参数
const launchOptions = qq.getLaunchOptionsSync();

// 检查启动场景是否为特定值（1008 或 1044）
if ([1008, 1044].includes(launchOptions.scene)) {
    const entryDataHash = launchOptions.entryDataHash;

    // 监听小程序显示事件，以便在小程序前台运行时更新入口数据哈希值
    qq.onAppShow((res) => {
        entryDataHash = res.entryDataHash;
    });

    // 根据入口数据哈希值获取群信息
    qq.getGroupInfo({
        entryDataHash,
        success: function (groupInfo) {
            // 如果当前用户是群管理员，则设置全局数据标志位为true
            if (groupInfo.isGroupManager) {
                _this.globalData.isGroupManager = true;
            }
        },
        fail: function () {
            // 处理获取群信息失败的情况（这里可以添加错误处理逻辑）
            console.error('Failed to get group info');
        }
    });
}
```

#### 初始化生命周期(注意ios安卓不一样)

```js
// onLaunch:
// onShow:
// 这两个生命周期中调用getSystemInfo在安卓和ios不一样,建议测试后决定放在哪个生命周期里面
let menuButton = qq.getMenuButtonBoundingClientRect();

qq.getSystemInfo({
    success: res => {
        const isIOS = res.platform === 'ios';
        const model = isIOS ? res.model : '';
        
        // 判断是否为特定设备
        this.globalData.newIphone = isIOS && (
            model.slice(7, 8) === 'X' || 
            (model.slice(7, 8) === '1' && Number(model.slice(8, 9)) >= 1)
        );

        const statusBarHeight = res.statusBarHeight;
        let navTop = Math.max(menuButton.top, statusBarHeight);
        let navHeight = navTop + 40 + (statusBarHeight > 30 ? (statusBarHeight > 40 ? 10 : 5) : 0);

        // 更新全局数据
        Object.assign(this.globalData, {
            navHeight,
            navTop,
            screenHeight: res.windowHeight - navHeight,
            screenWidth: res.screenWidth,
            pixelRatio: res.pixelRatio
        });
    },
    fail(err) {
        console.error(err);
    }
});

```

#### 竖向时间线

```js
<view class="progress-module" wx:for="{{dataList}}" wx:key="index">
  <view class="progress-module-title" wx:if="{{index === 0 ? '0' : '54'}}">{{titles[index]}}</view>
  <view class="progress-timeline-container" wx:for="{{dataList[index]}}" wx:key="{{item.time}}" bindtap="navigateToDetail" data-type="{{item.type}}" data-id="{{item.id}}" data-time="{{item.time}}">
    <view class="progress-timeline">
      <view class="progress-timeline-line"></view>
      <view class="progress-timeline-circle"></view>
      <view class="progress-timeline-icon">
        <image src="../../images/{{item.type}}.png" />
        <text wx:if="{{item.minute !== '00:00'}}">{{item.minute}}</text>
      </view>
      <view class="progress-timeline-cover" wx:if="{{index === dataList.length - 1}}"></view>
    </view>
    <view class="progress-content">
      <view class="hot-comment" wx:if="{{item.type !== 1 && item.comments.length > 0}}">
        <image src="../../images/pagecurrent/hot.png" />
        <view>
          <i>{{item.comments[0].name}}：</i>
          {{item.comments[0].text}}
        </view>
      </view>
    </view>
  </view>
</view>
```

```css

.progress-module {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.progress-module-title {
  font-weight: bold;
  padding-top: 54rpx;
  padding-bottom: 20rpx;
  font-size: 26rpx;
}

.progress-timeline {
  display: flex;
  position: relative;
  width: 80rpx;
  padding-top: 40rpx;
}

.progress-timeline-line {
  position: absolute;
  left: 28rpx;
  height: 100%;
  width: 2rpx;
  bottom: 0;
  background-color: #dde1e7;
}

.progress-timeline-circle {
  position: relative;
  z-index: 1;
  width: 14rpx;
  height: 14rpx;
  margin-left: 22rpx;
  margin-top: 0;
  border-radius: 50%;
  background-color: #dde1e7;
  display: none;
}

.progress-timeline-icon {
  position: relative;
  z-index: 1;
  margin-left: 4rpx;
  margin-top: 38rpx;
  width: 50rpx;
  padding-top: 10rpx;
  padding-bottom: 5rpx;
  background-color: #f8f8f8;
  font-size: 20rpx;
}

.progress-timeline-icon image {
  border-radius: 50%;
  width: 50rpx;
  height: 50rpx;
}

.progress-timeline-cover {
  position: relative;
  z-index: 1;
  width: 100%;
  flex-grow: 1;
  background-color: #f8f8f8;
  display: none;
}

.progress-content {
  width: 100%;
  padding: 32rpx 40rpx 34rpx 40rpx;
  background-color: #fff;
  border-radius: 16rpx;
  margin-left: 20rpx;
  box-shadow: 3rpx 5rpx 12rpx 0rpx rgba(0, 0, 0, 0.03);
}

.progress-timeline-last .progress-timeline-cover {
  display: block;
}

.progress-no-padding {
  padding-top: 0;
}

.progress-circle-visible .progress-timeline-circle {
  display: block;
}
```

#### 横向点击自动滑动

```html
<scroll-view class="topbar" scroll-with-animation="true" scroll-x="{{true}}" scroll-left="{{thisLeft}}">
  <view class="mytabs-nav">
    <view
      bindtap="selectTab"
      wx:for="{{list}}"
      wx:for-item="item"
      class="mytabs-nav-item"
      data-num="{{index}}"
      wx:key="index"
    >
      <image class="{{nav_item_num===index?'selected':''}}" src="{{ item }}" />
      <text class="{{nav_item_num===index?'bold':''}}">{{ item }}</text>
    </view>
  </view>
</scroll-view>
<style>
..mytabs-nav {
  display: flex;
  position: relative;
  height: 180rpx;
  width: max-content;
}
</style>
```

```js
methods:{
selectTab: function (e) {
  const index = e.currentTarget.dataset.num;
  this.scrollMove(index);
},

scrollMove: function (index) {
  const query = qq.createSelectorQuery();
  const _this = this;
  
  query.selectAll('.mytabs-nav-item').boundingClientRect().exec(function (res) {
    const items = res[0];
    
    if (items.length > 0) {
      const targetItem = items[index];
      const screenWidth = app.globalData.screenWidth;
      const targetLeft = targetItem.left;
      const itemWidth = targetItem.width;
      
      // 设置scroll-left属性，使目标元素居中显示
      const newLeft = targetLeft - screenWidth / 2 + itemWidth / 2;
      _this.setData({ thisLeft: newLeft });
    }
  });
}
}
```
#### 阻止穿透

```html
<view class="container">
  <view class="overlay" catchtouchmove="stopPropagation" hidden="{{!isModalVisible}}">
    <view class="modal" bindtap="toggleModal">
      <text>这是一个模态框</text>
    </view>
  </view>
  <button bindtap="showModal">显示模态框</button>
</view>
```
```js
Page({
  data: {
    isModalVisible: false
  },

  // 显示模态框
  showModal() {
    this.setData({ isModalVisible: true });
  },

  // 切换模态框显示
  toggleModal() {
    this.setData({ isModalVisible: !this.data.isModalVisible });
  },

  // 阻止事件穿透
  stopPropagation() {
    return; // 仅需返回即可阻止事件
  }
});

```

#### 处理C端时间

```js
// 计算标题数据
calcTitleData(array) {
    const result = [];
    const now = new Date();
    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1); // 获取昨天的日期

    for (const item of array) {
        const dateString = item[0].day; // 获取日期字符串
        const time = item[0].time; // 获取时间
        const date = new Date(time); // 创建日期对象

        const year = dateString.slice(0, 4);
        const monthDay = dateString.slice(4); // 获取月份和日期
        const month = monthDay.slice(0, 2);
        const day = monthDay.slice(2);

        // 特殊情况：元旦
        if (monthDay === '0101') {
            result.push(`${year}-${month}-${day}`);
        } 
        // 判断今天
        else if (this.isSameDate(date, now)) {
            result.push('今天');
        } 
        // 判断昨天
        else if (this.isSameDate(date, yesterday)) {
            result.push('昨天');
        } 
        // 其他情况：格式化为 MM-DD
        else {
            result.push(`${month}-${day}`);
        }
    }
    return result;
},

// 辅助函数：检查两个日期是否相同
isSameDate(date1, date2) {
    return date1.getFullYear() === date2.getFullYear() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getDate() === date2.getDate();
}

```

#### 跳转小程序

```js
let path = e.currentTarget.dataset.path
wx.navigateToMiniProgram({
    appId: 'wx',
    path: path,
    extraData: {},
    envVersion: 'release',
    success(res) {
    }
})
```


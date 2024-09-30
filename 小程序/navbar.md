以下是一个精简的通用 Navbar 组件示例，适用于小程序：

Navbar 组件

```html
<view class="navbar" style="height: {{navHeight}}px; background: {{bgcolor}};">
  <view wx:if="{{show}}" class="navbar-action-wrap">
    <image bindtap="navBack" src="icon_url" class="back-icon"></image>
  </view>
  <view class="navbar-title" bindtap="toTop">{{pageName}}</view>
</view>
```

```js
Component({
  properties: {
    bgcolor: { type: String, value: '#ffffff' },
    color: { type: String, value: '#000000' },
    pageName: { type: String, value: '' },
    show: { type: Boolean, value: true },
  },
  data: {
    navHeight: 0,
  },
  methods: {
    show() {
      const data = wx.getMenuButtonBoundingClientRect();
      this.setData({
        navHeight: data.top + data.height + (data.height / 2)
      });
    },
    navBack() {
      wx.navigateBack();
    },
    toTop() {
      // 返回顶部逻辑
    }
  },
  lifetimes: {
    attached() {
      this.show();
    }
  }
});
```

样式

```css
.navbar {
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  transition: background linear 0.3s;
}
.navbar-title {
  width: 100%;
  padding: 0 30rpx;
  height: 50px;
  line-height: 50px;
  font-weight: bold;
  font-size: 36rpx;
  color: {{color}};
  text-align: center;
}

.navbar-action-wrap {
  position: absolute;
  left: 10rpx;
  display: flex;
  align-items: center;
}

.back-icon {
  height: 37rpx;
  width: 37rpx;
}
```


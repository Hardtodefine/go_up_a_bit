#### 创建页面的函数

```js
import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import './index.scss'

const app = createApp(App)
app.config.globalProperties.$jsonpGet = 'test'
app.use(router)
app.mount('#app')
```

#### 创建router

```js
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: "/", name: "C", component: () => import('../views/C.vue') },
  { path: "/cm", name: "Cm", component: () => import('../views/Cm.vue') },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  try {
    var tok = localStorage.getItem('uid')
    var tokType = typeof (tok)
  } catch (err) {
    console.log(err)
    return
  }
  if (tok && tokType === 'string') {
    next()
  } else {
    if (to.name === 'Login') {
      next()
    } else {
      next({path:'login'})
    }
  }
})

export default router
```

#### vite.config.js

```js
export default{
  port:15241,
  optimizeDeps:{
    include: ["swiper/swiper-vue.esm.js","./md5/md5.js"]
  }
}
/*
Thanks Jack-rainbow<GitHub>
*/
```

#### setup

```html
<script>
import { getCurrentInstance, onMounted, ref } from "vue";
export default {
  setup() {
    const internalInstance = getCurrentInstance();
    const instance = internalInstance.appContext.config.globalProperties;
    onMounted(() => {
      init();
    });
    const init = () => {
      //init
      instance
        .$jsonpGet(tst2, "init")
        .then((res) => {
          userdata.value = res.data;
        })
        .catch(function (error) {
          alert("用户初始化失败");
        });
    };
    const userdata = ref("");
    const pagedata = ref("");
    const toMain = (arg) => {
      if(arg){
        localStorage.setItem('id',arg)
      }
      instance.$router.push({ name: "Main", query: '' });
    };
    return { toMain, userdata, pagedata };
  },
};
</script>
```


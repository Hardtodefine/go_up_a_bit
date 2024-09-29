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

#### swiper6.3 in vue3

```html
<template>
  <main>
    <swiper :slides-per-view="1.5" :space-between="50" :centeredSlides="true" effect="coverflow" :coverflowEffect="swiperOption">
      <swiper-slide v-for="item in pagedata" :key="item.id" :virtualIndex="item.id">
        <div @click="collections(item)" class="show">
          <img :src="item.pic_list[0].pic_url" alt="" />
        </div>
      </swiper-slide>
    </swiper>
  </main>
</template>
<script>
import SwiperCore, { EffectCoverflow } from "swiper";
SwiperCore.use([EffectCoverflow]);
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/swiper.scss";
import { getCurrentInstance, onMounted, ref } from "vue";
export default {
  components: {
    Swiper,
    SwiperSlide,
  },
  setup() {
    const internalInstance = getCurrentInstance();
    const instance = internalInstance.appContext.config.globalProperties;
    const userdata = instance.$route.query;
    onMounted(() => {
      getAlbum();
    });
    const swiperOption = {
      rotate: 0,
      stretch: 10,
      depth: 100,
      modifier: 1,
      slideShadows: false,
    };
    const pagedata = ref([]);
    const getAlbum = () => {
      let md5 = instance.$MD5(es);
      let es2 = { sign: 'md5' };
      instance
        .$jsonpGet(es2, "Pic")
        .then((res) => {
          pagedata.value = res.data;
        })
        .catch(function (error) {
          alert("获取图集失败");
        });
    };
    const collections = (item) => {
      instance.$router.push({ name: "Main" ,query:userdata});
    };
    return {
      pagedata,
      collections,
      swiperOption,
      userdata,
    };
  },
};
</script>
<style lang="scss" scoped>
main {
  display: flex;
  background-size: cover;
  background-position: top;
  width: 100vw;
  height: 100vh;
  display: flex;
  .swiper-container {
    position: fixed;
    top: 14vh;
    width: 100%;
    left: 0;
    height: 60vh;
    .swiper-slide {
      display: none;
      display: flex;
      flex-direction: column;
      align-items: center;
      .show {
        position: relative;
        overflow: hidden;
        display: flex;
        justify-content: center;
        height: 49vh;
        width: 57vw;
        border-radius: 2vw;
        box-shadow: 2vw 1vw 2vw 0vw rgba(254, 72, 102, 0.137);
        z-index: 2;
        img {
          object-fit: cover;
          height: 100%;
          width: 60vw;
          position: absolute;
        }
      }
      @media screen and (max-height: 700px) {
        .div{
          margin-top: 2vh;
        }
      }
    }
  }
}
</style>
```

#### swiper in html with jquery

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title></title>
  <script src="https://cdn.bootcdn.net/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <link href="https://cdn.bootcdn.net/ajax/libs/Swiper/5.4.5/css/swiper.min.css" rel="stylesheet">
  <script src="https://cdn.bootcdn.net/ajax/libs/Swiper/5.4.5/js/swiper.min.js"></script>
</head>
<body>
  <div class="app">
    <div class="container">
      <div class="swiper-container firstClass">
        <div class="swiper-wrapper" id="swiper-wrapper">
        </div>
      </div>
    </div>
  </div>
</body>
 $(function () {
    $.ajax({
      url: "https://",
      type: "GET",
      dataType: "jsonp", //指定服务器返回的数据类型
      success: function (data) {
        var data = data.data
        var str = '';
        for (let index = 0; index < data.length; index++) {
          const element = data[index];
          // console.log(index,'c1')
          let index2 = index + 1
          var str2 = '';
          for (let index = 0; index < element.pic_list.length; index++) {
            const elementson = element.pic_list[index];
            str2 += `<div class="swiper-slide"><img class="secImg" src="${elementson.pic_url}" insrc="${elementson.large_pic_url}" alt=""><div class="window flexCenter"><span>${item.pic_num}/${item.pic_total_num}</span></div></div>`
          }
          str += `
          <div class="swiper-slide slideSec">
            <div class="swiper-container secondClass secondClass${index2}">
              <div class="swiper-wrapper">
                ${str2}
              </div>
            </div>
            <span>${element.star_name}</span>
            <span>《${element.label_name}》</span>
          </div>`
        }
        $('#swiper-wrapper').html(str);
        swiperInit()
      },
      error: function (a1, a2, a3) {
        console.log(a1, a2, a3)
      }
    });
    function swiperInit() {
      var main_swiper = new Swiper('.firstClass', {
        slidesPerView: 1.5,
        spaceBetween: 40,
        centeredSlides: true,
        effect: 'coverflow',
        coverflowEffect: {
          rotate: 0,
          stretch: 10,
          depth: 100,
          modifier: 1,
          slideShadows: false
        }
      });
      var first_swiper = new Swiper('.secondClass1', {
        direction: 'vertical'
      });
      var second_swiper = new Swiper('.secondClass2', {
        direction: 'vertical'
      });
      var third_swiper = new Swiper('.secondClass3', {
        direction: 'vertical'
      });


  })
</script>

</html>
```

#### swiper in vue 2.x

```html
<template>
  <div class="swiper-box">
    <div class="swiper-wrapper">
      <div
        class="swiper-slide"
        style="
          background-image:url(https://swiperjs.com/demos/images/nature-1.jpg)
        "
      ></div>
      <div
        class="swiper-slide"
        style="
          background-image:url(https://swiperjs.com/demos/images/nature-1.jpg)
        "
      ></div>
      <div
        class="swiper-slide"
        style="
          background-image:url(https://swiperjs.com/demos/images/nature-1.jpg)
        "
      ></div>
      <div
        class="swiper-slide"
        style="
          background-image:url(https://swiperjs.com/demos/images/nature-1.jpg)
        "
      ></div>
    </div>
  </div>
</template>
<script>
import "swiper/swiper-bundle.min.css";
import "swiper/swiper-bundle.min.js";
import Swiper from "swiper";
export default {
  methods: {
    onSwiper(swiper) {
      console.log(swiper);
    },
    onSlideChange() {
      console.log("slide change");
    },
    initSwiper() {
      var mySwiper = new Swiper(".swiper-box", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        spaceBetween: 300,
        
        slidesPerView: "auto",
        coverflowEffect: {
          rotate: 50,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: true,
        },
      });
    },
  },
  mounted() {
    this.initSwiper();
  },
};
</script>
<style>
.swiper-box {
  width: 100vw;
  height: 100vh;
}
.swiper-slide {
  width: 30vw;
  height: 60vh;
  text-align: center;
  font-size: 18px;
  background: #fff;
  display: flex;
  align-items: center;
  transform: scale(0.9);
opacity: 0.6;
}
</style>
```


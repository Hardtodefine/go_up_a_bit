```html
<template>
    <div class="bgc">
        <div class="inner">
            <canvas ref="main" id="main"></canvas> <!-- 使用canvas元素 -->
        </div>
    </div>
</template>

<script>
import { onMounted, getCurrentInstance, ref, nextTick } from "vue";
export default {
    setup() {
        const main = ref(null);
        const internalInstance = getCurrentInstance();
        const instance = internalInstance.appContext.config.globalProperties;
        const sheetdata1 = ref([]); // x轴数据
        const sheetdata2 = ref([]); // y轴数据

        // 绘制图表
        const paint = () => {
            console.log("绘制图表");
            try {
                const myChart = instance.$echarts.init(main.value); // 初始化ECharts
                myChart.setOption({
                    xAxis: {
                        type: "category", // x轴类型为分类
                        boundaryGap: false, // 不留边界空隙
                        data: sheetdata1.value, // x轴数据
                    },
                    yAxis: {
                        type: "value", // y轴类型为数值
                        show: true, // 显示y轴
                    },
                    dataZoom: [ // 数据缩放控制
                        {
                            type: "inside", // 内部缩放
                            minValueSpan: 12, // 最小范围
                            start: 70, // 起始位置
                            end: 100, // 结束位置
                        },
                        {
                            start: 0,
                            end: 10,
                        },
                    ],
                    series: [
                        {
                            data: sheetdata2.value, // y轴数据
                            type: "line", // 线图类型
                            connectNulls: false, // 不连接空数据
                            areaStyle: {
                                color: { // 区域填充颜色
                                    type: "linear",
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [
                                        { offset: 0, color: "rgb(216, 232, 252)" }, // 起始颜色
                                        { offset: 0.7, color: "rgb(234, 245, 253)" }, // 中间颜色
                                        { offset: 1, color: "rgb(255, 255, 255)" }, // 结束颜色
                                    ],
                                },
                            },
                            lineStyle: {
                                width: 4, // 线宽
                                color: { // 线条颜色
                                    type: "linear",
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [
                                        { offset: 0, color: "rgb(52, 76, 255)" }, // 起始颜色
                                        { offset: 1, color: "rgb(109, 158, 250)" }, // 结束颜色
                                    ],
                                },
                                cap: "round", // 线条端点为圆形
                                shadowColor: "rgb(200, 217, 252)", // 阴影颜色
                                shadowBlur: 4, // 阴影模糊度
                                shadowOffsetY: 4, // 阴影垂直偏移
                            },
                            label: {
                                show: true, // 显示数据标签
                                position: "top", // 标签位置
                                distance: 6, // 距离
                                color: "rgb(53, 78, 255)", // 标签颜色
                                fontSize: 10, // 字体大小
                            },
                        },
                    ],
                });
            } catch (error) {
                console.log(error); // 错误处理
            }
        };
    
        // 生成随机负数数据
        const generateNegativeData = (hours = 24) => {
            return Array.from({ length: hours }, (_, hour) => {
                return {
                    hour: hour > 23 ? hour % 24 : hour, // 保证小时数在24小时内
                    negative_num: Math.floor(Math.random() * 81), // 随机生成0到80之间的整数
                };
            });
        };
    
        // 设置数据
        const sheetData = () => {
            const negative_data = generateNegativeData(48);
            sheetdata1.value = negative_data.map(el => el.hour + "时"); // x轴数据
            sheetdata2.value = negative_data.map(el => el.negative_num); // y轴数据
        };
    
        sheetData(); // 初始化数据
    
        // 在组件挂载后绘制图表
        onMounted(() => {
            nextTick(() => {
                paint();
            });
        });
    
        return {
            sheetdata1,
            sheetdata2,
            paint,
            main,
        };
    },
};
</script>

<style lang="scss" scoped>
.bgc {
    height: 100vh;
    width: 100vw;
    .inner {
        transform: translateY(-20px);
        display: flex;
        flex-direction: column;
        width: 37.5rem;
        background-color: #ffffff;
        border-radius: 1.6rem 1.6rem 0rem 0rem;
        #main {
            display: block;
            width: 37.5rem;
            height: 37.5rem;
        }
    }
}
</style>

```


<template>
  <div class="data-analysis-dashboard">
  <!-- 顶部标题 -->
  <div class="h2">
    <h2>统计分析模块</h2>
  </div>
  <div calss="h6">
    <router-link to="/disaster-list" style="position: fixed; top: 70px; left: 40px; z-index: 1000; color: #ffffff; text-decoration: none; font-size: 14px;">
  退出统计分析模块
</router-link>
  </div>

    <!-- 主内容区域 -->
    <div class="dashboard-content">
      <!-- 左侧图表 -->
      <div class="dashboard-chart left-chart">
        <div class="chart-container" id="left-chart" style="width: 100%; height: 100%;"></div>
      </div>

      <!-- 中间地图 -->
      <div class="dashboard-chart center-chart">
        <div class="chart-title"> </div>
        <div class="map-controls">

          <!-- 模态框 -->
          <div v-if="showModal" class="modal">
            <div class="modal-content">
              <span class="close" @click="showModal = false">&times;</span>
              <h2>修改数据</h2>
              <table>
                <thead>
                  <tr>
                    <th>省份</th>
                    <th>应急避难场所数量</th>
                    <th>灾害强度</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in data" :key="index">
                    <td>{{ item.name }}</td>
                    <td><input type="number" v-model.number="item.shelter" /></td>
                    <td><input type="number" v-model.number="item.disaster" /></td>
                  </tr>
                </tbody>
              </table>
              <button @click="updateData">更新数据</button>
            </div>
          </div>

        </div>
        <div class="chart-container" id="map" style="width: 100%; height: 100%;"></div>
      </div>

      <!-- 右侧图表 -->
      <div class="dashboard-chart right-chart">
        <div class="chart-container" id="right-chart" style="width: 100%; height: 100%;"></div>
      </div>
    </div>

   <!-- 底部数据展示 -->
   <div class="dashboard-footer">
      <!-- 左侧图表1 -->
      <div class="footer-chart footer-chart-1">
        <div class="chart-container" id="footer-chart-1" style="width: 100%; height: 100%;"></div>
      </div>
      <!-- 左侧图表2 -->
      <div class="footer-chart footer-chart-2">
        <div class="chart-container" id="footer-chart-2" style="width: 100%; height: 100%;"></div>
      </div>
      <!-- 右侧图表1 -->
      <div class="footer-chart footer-chart-3">
        <div class="chart-container" id="footer-chart-3" style="width: 100%; height: 100%;"></div>
      </div>
      <!-- 右侧图表2 -->
      <div class="footer-chart footer-chart-4">
        <div class="chart-container" id="footer-chart-4" style="width: 100%; height: 100%;"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/pie';
import 'echarts/lib/chart/bar';
import 'echarts/lib/chart/map';
import 'echarts/lib/component/geo';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/visualMap';
import 'echarts/map/js/china.js';

export default {
  name: 'GeoDistributionMap',
  data() {
    return {
      showModal: false,
      provinces: [
        { name: '北京', value: 1200 },
        { name: '天津', value: 800 },
        { name: '河北', value: 2000 },
        { name: '山西', value: 1500 },
        { name: '内蒙古', value: 1000 },
        { name: '辽宁', value: 1800 },
        { name: '吉林', value: 1200 },
        { name: '黑龙江', value: 1200 },
        { name: '上海', value: 1000 },
        { name: '江苏', value: 2500 },
        { name: '浙江', value: 2200 },
        { name: '安徽', value: 1800 },
        { name: '福建', value: 1800 },
        { name: '江西', value: 1500 },
        { name: '山东', value: 2200 },
        { name: '河南', value: 2000 },
        { name: '湖北', value: 1800 },
        { name: '湖南', value: 1800 },
        { name: '广东', value: 2500 },
        { name: '广西', value: 1500 },
        { name: '海南', value: 800 },
        { name: '重庆', value: 1500 },
        { name: '四川', value: 2000 },
        { name: '贵州', value: 1200 },
        { name: '云南', value: 1500 },
        { name: '西藏', value: 500 },
        { name: '陕西', value: 1500 },
        { name: '甘肃', value: 1000 },
        { name: '青海', value: 800 },
        { name: '宁夏', value: 500 },
        { name: '新疆', value: 1200 }
      ],
      disasterData: [
        100, 80, 150, 120, 90, 110, 85, 75, 95, 180, 160, 140, 130, 120, 170, 190, 155, 145, 200, 135, 80, 165, 185, 125, 115, 70, 150, 95, 85, 75, 90
      ],
      mapChart: null
    };
  },
  mounted() {
    this.initLeftChart();
    this.initRightChart();
    this.initMap();
    this.initFooterChart1();
    this.initFooterChart2();
    this.initFooterChart3();
    this.initFooterChart4();
  },
  methods: {
    initMap() {
      const mapChart = echarts.init(document.getElementById('map'));
      this.mapChart = mapChart;
      this.showShelterMap();
    },
    showShelterMap() {
      /*const data = [
        { name: '北京', value: 1200 },
        { name: '天津', value: 800 },
        { name: '河北', value: 2000 },
        { name: '山西', value: 1500 },
        { name: '内蒙古', value: 1000 },
        { name: '辽宁', value: 1800 },
        { name: '吉林', value: 1200 },
        { name: '黑龙江', value: 1200 },
        { name: '上海', value: 1000 },
        { name: '江苏', value: 2500 },
        { name: '浙江', value: 2200 },
        { name: '安徽', value: 1800 },
        { name: '福建', value: 1800 },
        { name: '江西', value: 1500 },
        { name: '山东', value: 2200 },
        { name: '河南', value: 2000 },
        { name: '湖北', value: 1800 },
        { name: '湖南', value: 1800 },
        { name: '广东', value: 2500 },
        { name: '广西', value: 1500 },
        { name: '海南', value: 800 },
        { name: '重庆', value: 1500 },
        { name: '四川', value: 2000 },
        { name: '贵州', value: 1200 },
        { name: '云南', value: 1500 },
        { name: '西藏', value: 500 },
        { name: '陕西', value: 1500 },
        { name: '甘肃', value: 1000 },
        { name: '青海', value: 800 },
        { name: '宁夏', value: 500 },
        { name: '新疆', value: 1200 }
      ];*/

      const option = {
        backgroundColor: '#0a1a2f',
        title: {
          text: '全国应急避难场所地理分布',
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold',
            color: '#00e5ff'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}<br/>应急避难场所数量：{c}'
        },
        visualMap: {
          min: 0,
          max: 3000,
          text: ['高', '低'],
          realtime: false,
          calculable: true,
          inRange: {
            color: ['#e0ffff', '#006edd']
          },
          textStyle: {
            color: '#ffffff'
          }
        },
        geo: {
          map: 'china',
          roam: true,
          label: {
            normal: {
              show: true,
              fontSize: 10,
              color: '#ffffff'
            },
            emphasis: {
              show: true
            }
          },
          itemStyle: {
            normal: {
              areaColor: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(0, 110, 221, 0.2)' },
                  { offset: 1, color: 'rgba(0, 110, 221, 0.6)' }
                ],
                global: false
              },
              borderColor: '#006edd',
              borderWidth: 1.5,
              shadowColor: 'rgba(0, 110, 221, 0.5)',
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowOffsetY: 5
            },
            emphasis: {
              areaColor: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  { offset: 0, color: 'rgba(0, 110, 221, 0.4)' },
                  { offset: 1, color: 'rgba(0, 110, 221, 0.8)' }
                ],
                global: false
              },
              shadowColor: 'rgba(0, 110, 221, 0.8)',
              shadowBlur: 20
            }
          }
        },
        series: [
      {
        name: '应急避难场所数量',
        type: 'map',
        map: 'china',
        roam: true,
        label: {
          normal: {
            show: true,
            fontSize: 10,
            color: '#ffffff'
          },
          emphasis: {
            show: true
          }
        },
        data: this.provinces.map(item => ({ name: item.name, value: item.value }))
      }
        ]
      };

      this.mapChart.setOption(option);
    },
    showDisasterImpactMap() {
  // 各省份灾害影响等级数据（示例数据，根据实际数据调整）
  const data = [
    { name: '北京', value: 4 }, // 中高风险
    { name: '天津', value: 4 }, // 中高风险
    { name: '河北', value: 3 }, // 中风险
    { name: '山西', value: 3 }, // 中风险
    { name: '内蒙古', value: 2 }, // 中低风险
    { name: '辽宁', value: 3 }, // 中风险
    { name: '吉林', value: 2 }, // 中低风险
    { name: '黑龙江', value: 2 }, // 中低风险
    { name: '上海', value: 4 }, // 中高风险
    { name: '江苏', value: 4 }, // 中高风险
    { name: '浙江', value: 4 }, // 中高风险
    { name: '安徽', value: 3 }, // 中风险
    { name: '福建', value: 4 }, // 中高风险
    { name: '江西', value: 3 }, // 中风险
    { name: '山东', value: 4 }, // 中高风险
    { name: '河南', value: 3 }, // 中风险
    { name: '湖北', value: 3 }, // 中风险
    { name: '湖南', value: 3 }, // 中风险
    { name: '广东', value: 4 }, // 中高风险
    { name: '广西', value: 3 }, // 中风险
    { name: '海南', value: 2 }, // 中低风险
    { name: '重庆', value: 3 }, // 中风险
    { name: '四川', value: 3 }, // 中风险
    { name: '贵州', value: 3 }, // 中风险
    { name: '云南', value: 3 }, // 中风险
    { name: '西藏', value: 2 }, // 中低风险
    { name: '陕西', value: 3 }, // 中风险
    { name: '甘肃', value: 2 }, // 中低风险
    { name: '青海', value: 2 }, // 中低风险
    { name: '宁夏', value: 2 }, // 中低风险
    { name: '新疆', value: 2 } // 中低风险
  ];

  const option = {
    title: {
      text: '全国各省份灾害影响等级图',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#00e5ff'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        return `${params.name}：灾害影响等级 ${params.value}`;
      }
    },
    visualMap: {
      min: 1,
      max: 5,
      text: ['高', '低'],
      realtime: false,
      calculable: true,
      inRange: {
        color: ['#4ECDC4', '#483D8B', '#FF6B6B']
      },
      textStyle: {
        color: '#ffffff'
      }
    },
    geo: {
      map: 'china',
      roam: true,
      label: {
        normal: {
          show: true,
          fontSize: 10,
          color: '#ffffff'
        },
        emphasis: {
          show: true
        }
      },
      itemStyle: {
        normal: {
          borderColor: '#ffffff',
          borderWidth: 0.5
        },
        emphasis: {
          borderColor: '#ffffff',
          borderWidth: 1
        }
      }
    },
    series: [
      {
        name: '灾害影响等级',
        type: 'map',
        mapType: 'china',
        geoIndex: 0,
        data: data
      }
    ]
  };

  this.mapChart.setOption(option);
},
    switchToShelterMap() {
      this.showShelterMap();
    },
    switchToDisasterHeatmap() {
      this.showDisasterHeatmap();
    },
    updateData() {
    this.showShelterMap();
    this.showDisasterHeatmap();
  },
  initLeftChart() {
  const leftChart = echarts.init(document.getElementById('footer-chart-4'));
  this.leftChart = leftChart;

  // 各区域避难所数量数据（示例数据，根据实际数据调整）
  const shelterRegionData = [
    { name: '东北地区', value: 1200 }, // 较高数量
    { name: '华北地区', value: 1500 }, // 较高数量
    { name: '华东地区', value: 1800 }, // 较高数量
    { name: '华中地区', value: 1300 }, // 中等数量
    { name: '华南地区', value: 1400 }, // 中等数量
    { name: '西南地区', value: 1100 }, // 中等数量
    { name: '西北地区', value: 900 }  // 较低数量
  ];

  const option = {
    title: {
      text: '全国各区域避难所数量分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#00e5ff' // 亮蓝色标题
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    series: [
      {
        name: '避难所数量',
        type: 'pie',
        radius: '55%',
        center: ['50%', '60%'], // 将图表往下移动
        data: shelterRegionData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        itemStyle: {
          borderRadius: 4, // 添加圆角效果
          borderColor: '#000000', // 边框颜色
          borderWidth: 1 // 边框宽度
        }
      }
    ],
    color: [
      '#0D47A1', '#1976D2', '#2196F3', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB'
    ], // 新的配色方案
    backgroundColor: '#0F1B29' // 深色背景
  };

  this.leftChart.setOption(option);
},
    initRightChart() {
  const rightChart = echarts.init(document.getElementById('right-chart'));
  this.rightChart = rightChart;

  const disasterTypeData = [
    { name: '地震', value: 10 },
    { name: '洪水', value: 40 },
    { name: '火灾', value: 120 },
    { name: '其他', value: 60 }
  ];

  const option = {
    title: {
      text: '灾害类型分布',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#00e5ff' // 亮蓝色，科技感十足
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
        shadowStyle: {
          color: 'rgba(0, 229, 255, 0.3)' // 与标题颜色相呼应的淡蓝色阴影
        }
      }
    },
    xAxis: {
      type: 'category',
      data: disasterTypeData.map(item => item.name),
      axisLine: {
        lineStyle: {
          color: '#409EFF' // 深蓝色，增强对比
        }
      },
      axisLabel: {
        textStyle: {
          color: '#FFFFFF' // 白色字体，清晰易读
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#409EFF' // 深蓝色，与X轴一致
        }
      },
      axisLabel: {
        textStyle: {
          color: '#FFFFFF' // 白色字体
        }
      },
      splitLine: {
        lineStyle: {
          color: '#1F497D', // 深蓝色网格线，增强层次感
          type: 'dashed' // 虚线样式
        }
      }
    },
    series: [
      {
        name: '次数',
        type: 'bar',
        data: disasterTypeData.map(item => item.value),
        itemStyle: {
          color: function (params) {
            // 根据数据值动态设置柱状图颜色，增强视觉效果
            if (params.value >= 100) {
              return '#FF5722'; // 橙红色，突出高值
            } else if (params.value >= 50) {
              return '#2196F3'; // 蓝色，中等值
            } else {
              return '#43A047'; // 绿色，低值
            }
          }
        },
        barWidth: '20%', // 设置柱状图宽度
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderColor: '#00e5ff', // 高亮时的边框颜色
            borderWidth: 2
          }
        }
      }
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top :'20%',
      containLabel: true
    },
    backgroundColor: '#0F1B29' // 深色背景，增强科技感
  };

  this.rightChart.setOption(option);
},
initFooterChart1() {
  const chart = echarts.init(document.getElementById('footer-chart-1'));
  this.chart = chart;

  // 各区域城市灾害数量数据（示例数据，根据实际数据调整）
  const disasterRegionData = [
    { name: '东北地区', value: 120 }, // 较高数量
    { name: '华北地区', value: 150 }, // 较高数量
    { name: '华东地区', value: 180 }, // 较高数量
    { name: '华中地区', value: 130 }, // 中等数量
    { name: '华南地区', value: 140 }, // 中等数量
    { name: '西南地区', value: 110 }, // 中等数量
    { name: '西北地区', value: 90 }  // 较低数量
  ];

  const option = {
    title: {
      text: '全国各区域城市灾害数量分布',
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#00e5ff' // 亮蓝色标题
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    series: [
      {
        name: '城市灾害数量',
        type: 'pie',
        radius: '55%',
        center: ['50%', '60%'], // 将图表往下移动
        data: disasterRegionData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        itemStyle: {
          borderRadius: 4, // 添加圆角效果
          borderColor: '#000000', // 边框颜色
          borderWidth: 1 // 边框宽度
        }
      }
    ],
    color: [
      '#0D47A1', '#1976D2', '#2196F3', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB'
    ], // 新的配色方案
    backgroundColor: '#0F1B29' // 深色背景
  };

  this.chart.setOption(option);
},


    // 初始化模块2图表（避难所容纳人数柱状图）
    initFooterChart2() {
  const chart = echarts.init(document.getElementById('footer-chart-2'));
  const shelterCapacityData = [
    { name: '0-1000', value: 50 },
    { name: '1000-3000', value: 20 },
    { name: '3000-5000', value: 15 },
    { name: '5000-10000', value: 10 },
    { name: '>10000', value: 5 }
  ];

  const option = {
    title: {
      text: '避难所容纳人数分布',
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#00e5ff' // 亮蓝色标题
      }
    },
    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        return `${params[0].name}：${params[0].data}%`;
      }
    },
    grid: {
      left: '0%',
      top: '30%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      name:'人数',
      data: shelterCapacityData.map(item => item.name),
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {
        lineStyle: {
          color: '#2196F3' // 横坐标轴线颜色为浅蓝色
        }
      },
      axisLabel: {
        textStyle: {
          color: '#2196F3' // 横坐标文字颜色为浅蓝色
        }
      }
    },
    yAxis: {
      type: 'value',
      name: '占比',
      min: 0,
      max: 100, // 设置最大值为100，表示100%
      axisLabel: {
        formatter: '{value}%', // 在数字后面加上百分号
        textStyle: {
          color: '#2196F3' // 纵坐标文字颜色为浅蓝色
        }
      },
      axisLine: {
        lineStyle: {
          color: '#2196F3' // 纵坐标轴线颜色为浅蓝色
        }
      }
    },
    series: [
      {
        name: '人数占比',
        type: 'bar',
        barWidth: '60%',
        data: shelterCapacityData.map(item => item.value),
        itemStyle: {
          color: '#009688' // 柱状图颜色
        }
      }
    ],
    backgroundColor: '#0F1B29' // 深色背景
  };

  chart.setOption(option);
},
    // 初始化模块3图表（灾害发生时间趋势线图）
    initFooterChart3() {
  const chart = echarts.init(document.getElementById('footer-chart-3'));
  const disasterTimeData = [
    { name: '2021', value: 0.46 },
    { name: '2023', value: 0.61 },
    { name: '2024', value: 0.55 }
  ];

  const option = {
    title: {
      text: '历年受灾程度概况',
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#00e5ff' // 亮蓝色标题
      }
    },
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '5%',
      top: '30%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: disasterTimeData.map(item => item.name),
      axisTick: {
        alignWithLabel: true
      },
      axisLine: {
        lineStyle: {
          color: '#2196F3' // 横坐标轴线颜色为浅蓝色
        }
      },
      axisLabel: {
        textStyle: {
          color: '#2196F3' // 横坐标文字颜色为浅蓝色
        }
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      axisLine: {
        lineStyle: {
          color: '#2196F3' // 纵坐标轴线颜色为浅蓝色
        }
      },
      axisLabel: {
        show: false // 不显示纵轴数字
      },
      splitLine: {
        lineStyle: {
          color: '#2196F3', // 网格线颜色为浅蓝色
          type: 'dashed' // 虚线样式
        }
      }
    },
    series: [
      {
        name: '次数',
        type: 'line',
        data: disasterTimeData.map(item => item.value),
        smooth: true,
        itemStyle: {
          color: '#ff5722' // 橙红色折线
        },
        lineStyle: {
          color: '#ff5722' // 橙红色折线
        }
      }
    ],
    backgroundColor: '#0F1B29' // 深色背景
  };

  chart.setOption(option);
},
     // 初始化模块4图表（避难所类型分布饼图）
     initFooterChart4() {
  const chart = echarts.init(document.getElementById('left-chart'));
  const shelterTypeData = [
    { name: 'Ⅰ', value: 20 },
    { name: 'Ⅱ', value: 15 },
    { name: 'Ⅲ', value: 10 }
  ];

  const option = {
    title: {
      text: '避难所类型分布',
      left: 'center',
      textStyle: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#00e5ff' // 亮蓝色标题
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
        shadowStyle: {
 // 与标题颜色相呼应的淡蓝色阴影
        }
      }
    },
    xAxis: {
      type: 'category',
      data: shelterTypeData.map(item => item.name),
      axisLine: {
        lineStyle: {
          color: '#2196F3' // 深蓝色坐标轴
        }
      },
      axisLabel: {
        textStyle: {
          color: '#FFFFFF' // 白色字体
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#2196F3' // 深蓝色坐标轴
        }
      },
      axisLabel: {
        textStyle: {
          color: '#FFFFFF' // 白色字体
        }
      },
      splitLine: {
        lineStyle: {
          color: '#2196F3', // 深蓝色网格线
          type: 'dashed' // 虚线样式
        }
      }
    },
    series: [
      {
        name: '数量',
        type: 'bar',
        data: shelterTypeData.map(item => item.value),
        itemStyle: {
          color: function (params) {
            // 根据数据值动态设置柱状图颜色，与 initRightChart 一致
            if (params.value >=20) {
              return '#FF5722'; // 橙红色，突出高值
            } else if (params.value >=15) {
              return '#2196F3'; // 蓝色，中等值
            } else {
              return '#43A047'; // 绿色，低值
            }
          }
        },
        barWidth: '20%', // 柱状图宽度
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderColor: '#2196F3', // 高亮时的边框颜色
            borderWidth: 2
          }
        }
      }
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top:'20%',
      containLabel: true
    },
    backgroundColor: '#0F1B29' // 深色背景
  };

  chart.setOption(option);
}        
  }
};

</script>

<style scoped>


.data-analysis-dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #030810;
  color: #ffffff;
  padding: 20px;
  font-family: 'Arial', sans-serif;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 20px;
  flex: 1;
  margin-bottom: 10px;
  height: 50px;
}

.dashboard-chart {
  background-color: rgba(15, 33, 56, 0.65);
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  position: relative;
  height: 350px;
}

.chart-title {
  font-size: 16px;
  margin-bottom: 10px;
  color: #00e5ff;
  text-align: center;
}

.chart-container {
  width: 100%;
  height: 280px;
}

.dashboard-footer {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr; /* 四个模块，每列大小相同 */
  gap: 20px;
  border-radius: 8px;
  padding: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  left: 0px;
}

.footer-chart {
  background-color: rgba(15, 33, 56, 0.65);
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  height: 200px; /* 根据需要调整高度 */
}
.footer-chart.chart-title {
  font-size: 14px;
  margin-bottom: 10px;
  color: #00e5ff;
  text-align: center;
}

.map-controls {
  position: absolute;
  top: 5px;
  left: 5px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 100;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

button {
  background: linear-gradient(135deg, #135d93, #11374e);
  color: white;
  border: none;
  padding: 10px 18px;
  margin: 0;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  width: 140px;
  text-align: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

button:hover {
  background: linear-gradient(135deg, #5dade2, #2980b9);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

button:active {
  transform: translateY(1px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

button:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5);
}
h2 {
  text-align: center;
  margin: 10;
  font-size: 24px;
  color: #96c6f6; /* 初始颜色为亮蓝色 */
  transition: color 0.3s ease; /* 添加颜色过渡效果 */

}


</style>
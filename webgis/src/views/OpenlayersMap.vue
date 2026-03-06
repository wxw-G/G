<template>
  <div class="map-container">
    <div class="map" id="map"></div>
        <div class="search-panel">
            <div class="module">
              <div class="search-row">
                <input
                    type="text"
                    v-model="searchQuery"
                    placeholder="输入搜索区域"
                    @keyup.enter="searchCity"
                />
                <button @click="searchCity">搜索</button>
              </div>
            </div>
          </div>

          <!-- 独立地图图层模块（脱离search-container） -->
          <div class="layer-panel">
            <div class="module">

              <button @click="toggleSatelliteLayer">
                {{ satelliteLayerVisible ? '显示矢量图' : '显示卫星图' }}
              </button>
            </div>
          </div>

    <div class="search-container">
        <!-- 应急避难场所模块 -->
        <div class="module">
          <h4>应急避难场所</h4>
          <button @click="loadShelters">加载应急避难场所</button>
          <button @click="clearShelters" class="clear-button">关闭显示应急避难场所</button>
          <button @click="goToShelterList">查看应急避难场所列表</button>
        </div>

        <!-- 受灾地点模块 -->
        <div class="module">
          <h4>受灾地点管理</h4>
          <button @click="showDisasters">加载受灾地点</button>
          <button @click="clearDisasters" class="clear-button">关闭显示受灾地点</button>
          <button @click="toggleAddDisaster" style="margin-left: 5px;">添加受灾地点</button>
          <button @click="goToDisasterList">查看受灾地点列表</button>
        </div>

        <!-- 灾害范围模拟模块 -->
        <div class="module">
          <h4>灾害范围模拟</h4>
          <button @click="enableMapClick">灾害范围模拟</button>
          <button @click="clearImpactArea">清除灾害范围</button>
        </div>

        <!-- 路径规划模块 -->
        <div class="module">
          <h4>路径规划</h4>
          <button @click="enablePathPlanning">路径规划</button>
          <button @click="clearPathPlanning">清除路径规划</button>
        </div>
    
    </div>
    <div class="disaster-container">
      <input
          type="text"
          v-model="disasterLat"
          placeholder="纬度"
          @keyup.enter="addDisasterLocation"
      />
      <input
          type="text"
          v-model="disasterLon"
          placeholder="经度"
          @keyup.enter="addDisasterLocation"
      />
      <button @click="jumpToLocation(disasterLat, disasterLon)">
        跳转到该位置
      </button>
    </div>

    <!-- 显示应急避难所数量 -->
    <div class="shelter-count-container">
      <h4>应急避难所数量：{{ shelterCount }}</h4>
    </div>

    <!-- 灾害地点模态窗口 -->
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal">
        <h3>添加灾害地点</h3>
        <div>
          <label for="disaster-name">受灾地名称：</label>
          <input type="text" id="disaster-name" v-model="disasterName" />
        </div>
        <div>
          <label for="disaster-type">灾害类型：</label>
          <select id="disaster-type" v-model="disasterType">
            <option value="地震">地震</option>
            <option value="洪水">洪水</option>
            <option value="火灾">火灾</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <div>
          <label for="disaster-description">灾害描述：</label>
          <textarea id="disaster-description" v-model="disasterDescription"></textarea>
        </div>
        <div>
          <label for="disaster-time">添加时间：</label>
          <input type="datetime-local" id="disaster-time" v-model="disasterTime" />
        </div>
        <button @click="confirmDisasterLocation">确认</button>
        <button @click="closeModal">取消</button>
      </div>
    </div>
    <!-- 弹出窗口用于显示受灾信息 -->
    <div v-if="popupVisible" class="popup" :style="{ top: popupPosition.y + 'px', left: popupPosition.x + 'px' }">
    <div class="popup-content">
      <h4>{{ selectedDisaster.name }}</h4>
      <p><strong>类型：</strong>{{ selectedDisaster.type }}</p>
      <p><strong>描述：</strong>{{ selectedDisaster.description }}</p>
      <p><strong>时间：</strong>{{ selectedDisaster.time }}</p>
      <p><strong>经纬度：</strong>{{ selectedDisaster.coordinates }}</p>
      <button @click="closePopup">关闭</button>
    </div>
  </div>
    <!-- 影响范围设置模态窗口 -->
    <div v-if="showImpactModal" class="modal-overlay">
    <div class="modal">
      <h3>设置影响范围</h3>
      <div>
        <label for="impact-radius">影响半径（公里）：</label>
        <input
          type="range"
          id="impact-radius"
          min="1"
          max="50"
          v-model.number="impactRadius"
        />
        <span>{{ impactRadius }} 公里</span>
      </div>
      <button @click="setImpactArea">确认</button> <!-- 确保绑定了 setImpactArea -->
      <button @click="showImpactModal = false">取消</button>
    </div>
  </div>
  <!-- 显示成功提示信息 -->
  <div v-if="successMessage" class="success-message">
    {{ successMessage }}
  </div>
  </div>

</template>

<script setup>
import { ref } from 'vue';
import { onMounted } from 'vue';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import XYZ from 'ol/source/XYZ';
import { transform, fromLonLat,toLonLat } from 'ol/proj';
import { LineString } from 'ol/geom';
import { Vector as VectorSource } from 'ol/source';
import { Vector as VectorLayer } from 'ol/layer';
import { Point } from 'ol/geom';
import Feature from 'ol/Feature';
import { Circle as CircleStyle, Fill, Stroke, Style, Text } from 'ol/style';
//import Overlay from 'ol/Overlay'; // 导入 Overlay
import router from "@/router";
import { getAllDisasters, addDisaster } from '@/api/disasterApi.js';
import { getAllShelters} from '@/api/shelterApi.js';
//import OlCircle from 'ol'
import CircleGeometry from 'ol/geom/Circle'; // 确保正确导入 CircleGeometry
import axios from 'axios';


// 替换为你的天地图密钥
const tiandituKey = '39a68c9063e97d2272bca97f274372b4';
// 替换为你的高德地图API密钥
const gaodeKey = 'f05d1846707de074210bd8750fd13ac2';

// 搜索相关的变量
const searchQuery = ref('');
const map = ref(null);
const satelliteLayerVisible = ref(false);
const shelterLayer = ref(null);
const disasterLayer = ref(null);
const disasterLat = ref('');
const disasterLon = ref('');
const shelterCount = ref(0); // 新增变量，用于存储应急避难所数量
const canAddDisaster = ref(false); // 控制是否可以添加受灾地点
const canAddDisaster2 = ref(false); // 控制是否可以进行灾害模拟
// 模态窗口相关的变量
const isModalOpen = ref(false);
const disasterName = ref('');
const disasterType = ref('地震');
const disasterDescription = ref('');
const disasterTime = ref('');
const disasterImage = ref(null);


const popupVisible = ref(false); // 控制弹出窗口的显示和隐藏
const popupPosition = ref({ x: 0, y: 0 }); // 弹出窗口的位置
const selectedDisaster = ref(null); // 当前选中的受灾点信息

const showImpactModal=ref(false);
const clickCoordinate = ref(null);
const impactLayer = ref(null); // 用于显示波纹图的图层
const impactRadius = ref(10); // 默认影响半径
const successMessage=ref(false);

const canAddPathPlanning = ref(false); // 控制是否允许路径规划
const clickCoordinate2 = ref(null); // 存储点击的坐标
const nearestShelter = ref(null); // 存储最近的避难所信息
const routeLayer = ref(null); // 用于显示波纹图的图层


// 切换卫星图层的可见性
const toggleSatelliteLayer = () => {
  satelliteLayerVisible.value = !satelliteLayerVisible.value; // 切换布尔值
  const satelliteLayer = map.value.getLayers().item(2); // 假设卫星图层是第三个图层（索引为2）
  if (satelliteLayer) {
    satelliteLayer.setVisible(satelliteLayerVisible.value); // 设置图层的可见性
  }
};

// 启用路径规划功能
const enablePathPlanning = () => {
  canAddPathPlanning.value = true;
  console.log('路径规划功能已启用，现在可以点击地图选择起点');
};

// 地图点击事件处理函数
const handleMapClick2 = (event) => {
  if (canAddPathPlanning.value) {
    console.log('地图被点击，坐标:', event.coordinate);
    clickCoordinate2.value = event.coordinate;
    console.log('开始查找最近的避难所');
    findNearestShelter(clickCoordinate2.value);
    canAddPathPlanning.value = false; // 禁用再次点击
  } else {
    console.log('路径规划功能未启用，无法处理点击事件');
  }
};

// 查找最近的避难所
const findNearestShelter = (coordinate) => {
  const [lon, lat] = toLonLat(coordinate); // 转换为经纬度
  console.log('点击位置的经纬度:', lat, lon);

  const shelters = shelterLayer.value.getSource().getFeatures();
  let nearest = null;
  let minDistance = Infinity;

  if (shelters.length === 0) {
    alert('没有找到任何避难所数据，请检查避难所图层是否加载');
    return;
  }

  shelters.forEach((shelter) => {
    const shelterCoord = shelter.getGeometry().getCoordinates();
    const [shelterLon, shelterLat] = toLonLat(shelterCoord);
    const distance = calculateDistance(lat, lon, shelterLat, shelterLon); // 计算距离
    console.log('避难所名称:', shelter.get('name'), '距离:', distance);

    if (distance < minDistance) {
      minDistance = distance;
      nearest = {
        name: shelter.get('name'),
        coordinate: shelterCoord,
      };
    }
  });

  if (nearest) {
    nearestShelter.value = nearest;
    console.log('最近的避难所:', nearest.name, '坐标:', nearest.coordinate);
    planPath(coordinate, nearest.coordinate);
  } else {
    alert('未找到最近的避难所');
  }
};

// 计算两点之间的距离（单位：米）
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const R = 6371e3; // 地球半径（米）
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) *
      Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
};

// 路径规划
const planPath = (startCoord, endCoord) => {
  const [startLon, startLat] = toLonLat(startCoord);
  const [endLon, endLat] = toLonLat(endCoord);

  const url = `https://restapi.amap.com/v3/direction/driving?key=${gaodeKey}&origin=${startLon},${startLat}&destination=${endLon},${endLat}&extensions=all`;

  axios.get(url)
    .then(response => {
      const result = response.data;
      if (result.status === '1') {
        console.log('路径规划成功，返回结果:', result);
        displayRoute(result.route.paths[0]);
      } else {
        alert('路径规划失败: ' + result.info);
      }
    })
    .catch(error => {
      console.error('路径规划失败:', error);
      alert('路径规划请求失败，请检查网络连接或API密钥是否正确');
    });
};

// 在地图上展示路径
const displayRoute = (path) => {
  console.log('开始解析路径数据并绘制路径');
  const steps = path.steps;
  const routeCoordinates = [];

  steps.forEach(step => {
    const polyline = step.polyline.split(';');
    polyline.forEach(point => {
      const [lon, lat] = point.split(',').map(Number);
      routeCoordinates.push(fromLonLat([lon, lat]));
    });
  });

  routeLayer.value = new VectorLayer({
    source: new VectorSource({
      features: [
        new Feature({
          type: 'route',
          geometry: new LineString(routeCoordinates),
        }),
      ],
    }),
    style: new Style({
      stroke: new Stroke({
        color: '#ff0000',
        width: 5,
      }),
    }),
  });

  if (map.value.getLayers().item(1)) {
    map.value.removeLayer(map.value.getLayers().item(1)); // 移除旧的路径图层
  }
  map.value.addLayer(routeLayer.value); // 添加新的路径图层
  console.log('路径绘制完成');
};



// 清除路径规划
const clearPathPlanning = () => {
  if (routeLayer.value) {
    map.value.removeLayer(routeLayer.value); // 移除路径图层
    routeLayer.value = null; // 重置路径图层引用
    console.log('路径规划已清除');
  }
};


//灾害影响范围模拟
const setImpactArea = () => {
  // 检查必要的输入是否有效
  if (!clickCoordinate.value) {
    alert('点击坐标不存在，请先选择一个位置');
    return;
  }
  if (!impactRadius.value || impactRadius.value <= 0) {
    alert('请输入有效的影响半径');
    return;
  }

  // 构造影响范围数据
  const impactData = {
    coordinate: clickCoordinate.value,
    radius: impactRadius.value
  };

  // 调用绘制函数
  drawImpactCircle(impactData.coordinate, impactData.radius);
  // 关闭模态窗口
  showImpactModal.value = false;
};

// 绘制波纹图的方法
const drawImpactCircle = (coordinate, radius) => {
  console.log('绘制波纹图，坐标:', coordinate, '半径:', radius);
  const radiusInMeters = radius * 1000;
  const circleGeometry = new CircleGeometry(coordinate, radiusInMeters);
  const impactFeature = new Feature({
    geometry: circleGeometry,
    type: 'impact-circle',
  });
  const impactStyle = new Style({
    fill: new Fill({ color: 'rgba(255, 0, 0, 0.2)' }),
    stroke: new Stroke({ color: '#ff0000', width: 2 }),
  });

  if (impactLayer.value) {
    impactLayer.value.getSource().clear();
  } else {
    impactLayer.value = new VectorLayer({
      source: new VectorSource(),
    });
    map.value.addLayer(impactLayer.value);
  }

  impactLayer.value.getSource().addFeature(impactFeature);
  impactLayer.value.setStyle(impactStyle);
};
// 清除灾害模拟
const clearImpactArea = () => {
  if (impactLayer.value) {
    impactLayer.value.getSource().clear(); // 清除图层中的所有要素
    map.value.removeLayer(impactLayer.value); // 从地图中移除图层
    impactLayer.value = null; // 重置图层引用
  }
};
// 搜索城市
const searchCity = async () => {
  if (!searchQuery.value) {
    alert('请输入城市名称');
    return;
  }

  try {
    // 确保URL是正确的
    const url = `http://api.tianditu.gov.cn/geocoder?ds=${encodeURIComponent(JSON.stringify({"keyWord": searchQuery.value}))}&tk=${tiandituKey}`;
    const response = await fetch(url);
    const data = await response.json();

    if (data && data.location) {
      const { lon, lat } = data.location;
      const center = transform([lon, lat], 'EPSG:4326', 'EPSG:3857');

      map.value.getView().animate({
        center: center,
        zoom: 16,
        duration: 1000,
      });
      // 存储搜索内容

      currentSearchCity.value = searchQuery.value;
    } else {
      alert('未找到该城市');
    }
  } catch (error) {
    console.error('搜索失败:', error);
    alert('搜索失败，请检查输入或网络连接');
  }
};

const currentSearchCity = ref(''); // 用于存储当前搜索的城市名称



// 加载应急避难场所
const loadShelters = async () => {
  if (!shelterLayer.value) {
    shelterLayer.value = new VectorLayer({
      source: new VectorSource(),
      style: (feature) => {
        const name = feature.get('name') || '未知';
        return new Style({
          image: new CircleStyle({
            radius: 12,
            fill: new Fill({ color: '#007bff' }), // 修改颜色以区分
            stroke: new Stroke({ color: '#ffffff', width: 3 }),
          }),
          text: new Text({
            font: '16px Calibri, sans-serif',
            fill: new Fill({ color: '#ffffff' }),
            stroke: new Stroke({ color: '#007bff', width: 2 }), // 修改颜色以区分
            text: name,
          }),
        });
      },
    });
    map.value.addLayer(shelterLayer.value);
  }

  try {
    const response = await getAllShelters(); // 调用后端接口获取数据
    console.log('后端返回的应急避难场所数据:', response.data);

    if (response.status === 200) {
      const shelters = response.data.data;

      shelterLayer.value.getSource().clear();
      const sheltersData = []; // 用于存储应急避难场所信息

      if (shelters.length === 0) {
        alert('没有找到应急避难场所数据');
        return;
      }

      shelters.forEach((shelter) => {
        console.log('处理应急避难场所:', shelter);
        const [lat, lon] = [shelter.latitude, shelter.longitude]; // 后端返回的经纬度
        const point = new Point(fromLonLat([lon, lat]));
        const feature = new Feature({
          geometry: point,
          name: shelter.name || '未知',
        });
        shelterLayer.value.getSource().addFeature(feature);

        // 将数据存储到数组中
        sheltersData.push({
          搜索地: searchQuery.value,
          名称: shelter.name,
          坐标: `${lat.toFixed(6)}, ${lon.toFixed(6)}`,
        });
      });

      // 将数据存储到 localStorage 中
      localStorage.setItem('emergencySheltersData', JSON.stringify(sheltersData));

      // 更新应急避难所数量
      shelterCount.value = sheltersData.length;

      alert('应急避难场所加载成功，已高亮显示');
    } else {
      alert('加载应急避难场所失败: ' + response.data.message);
    }
  } catch (error) {
    console.error('加载应急避难场所失败:', error);
    alert('加载应急避难场所失败，请检查网络连接或后端接口是否正常');
  }
};

// 打开模态窗口
const openModal = (lat, lon) => {
  disasterLat.value = lat;
  disasterLon.value = lon;
  isModalOpen.value = true;
};

// 关闭模态窗口
const closeModal = () => {
  isModalOpen.value = false;
  disasterName.value = '';
  disasterType.value = '地震';
  disasterDescription.value = '';
  disasterTime.value = '';
  disasterImage.value = null;
};



// 移除地图的点击事件监听器
const removeMapClickListener = () => {
  map.value.un('click', handleMapClick);
};

// 地图点击事件处理函数
const handleMapClick = (event) => {
  if (canAddDisaster.value) {
    const coordinate = event.coordinate;
    const [lon, lat] = transform(coordinate, 'EPSG:3857', 'EPSG:4326');
    openModal(lat.toFixed(6), lon.toFixed(6));
    canAddDisaster.value = false; // 点击后设置为 false，禁用再次点击添加
    removeMapClickListener(); // 移除地图的点击事件监听器
    canAddDisaster.value = false;
  }
};
const toggleAddDisaster = () => {
  canAddDisaster.value = !canAddDisaster.value;
  if (canAddDisaster.value) {
    map.value.on('click', handleMapClick);
  } else {
    map.value.un('click', handleMapClick);
  }
};
// 确认添加灾害地点
const confirmDisasterLocation = async () => {
  if (!disasterName.value) {
    alert('请输入受灾地名称');
    return;
  }

  const newDisaster = {
    name: disasterName.value,
    type: disasterType.value,
    description: disasterDescription.value,
    time: disasterTime.value,
    coordinates: `${disasterLat.value},${disasterLon.value}`
  };

  try {
    const response = await addDisaster(newDisaster);
    if (response.status === 201) {
      alert('灾害地点添加成功');
      closeModal();
      showDisasters(); // 刷新地图上的受灾地点
    } else {
      alert('添加受灾地点失败: ' + response.data.message);
    }
  } catch (error) {
    console.error('添加受灾地点失败:', error);
    alert('添加受灾地点失败，请检查网络连接或后端接口是否正常');
  }
};
//显示受灾地
const showDisasters = async () => {
  try {
    const response = await getAllDisasters();
    if (response.status === 200) {
      const disasters = response.data.data;

      if (!disasterLayer.value) {
        disasterLayer.value = new VectorLayer({
          source: new VectorSource(),
          style: () => {
            return new Style({
              image: new CircleStyle({
                radius: 10,
                fill: new Fill({ color: '#ff0000' }),
                stroke: new Stroke({ color: '#ffffff', width: 2 }),
              }),
            });
          },
        });
        map.value.addLayer(disasterLayer.value);
      }

      disasterLayer.value.getSource().clear();

      disasters.forEach((disaster) => {
        const [lat, lon] = disaster.coordinates.split(',').map(Number);
        const point = new Point(fromLonLat([lon, lat]));
        const feature = new Feature({
          geometry: point,
        });
        disasterLayer.value.getSource().addFeature(feature);
      });
    }
  } catch (error) {
    console.error('加载受灾地点失败:', error);
  }
};
// 清除受灾地点
const clearDisasters = () => {
  if (disasterLayer.value) {
    disasterLayer.value.getSource().clear();
  }
};
// 添加受灾地点按钮点击事件
const addDisasterLocation = () => {
  canAddDisaster.value = true; // 设置为 true，允许添加受灾地点
  map.value.on('click', handleMapClick); // 添加地图的点击事件监听器
};

// 定义深色模式的 tileLoadFunction
const tileLoadFunction = (imageTile, src) => {
  const img = new Image();
  img.setAttribute("crossOrigin", "anonymous");
  img.onload = function () {
    const canvas = document.createElement("canvas");
    const w = img.width;
    const h = img.height;
    canvas.width = w;
    canvas.height = h;
    const context = canvas.getContext("2d");
    if (context) {
      context.filter =
          "grayscale(98%) invert(100%) sepia(20%) hue-rotate(180deg) saturate(1600%) brightness(80%) contrast(90%)";
      context.drawImage(img, 0, 0, w, h, 0, 0, w, h);
      imageTile.getImage().src = canvas.toDataURL("image/png");
    }
  };
  img.src = src;
};

onMounted(() => {
  map.value = new Map({
    target: 'map',
    layers: [
      new TileLayer({
        title: '天地图矢量图层',
        source: new XYZ({
          url: `http://t0.tianditu.gov.cn/DataServer?T=vec_w&x={x}&y={y}&l={z}&tk=${tiandituKey}`,
          wrapX: false,
          tileLoadFunction: tileLoadFunction, // 应用深色模式的 tileLoadFunction
        }),
      }),
      new TileLayer({
        title: "天地图矢量注记图层",
        source: new XYZ({
          url: `http://t0.tianditu.gov.cn/DataServer?T=cva_w&x={x}&y={y}&l={z}&tk=${tiandituKey}`,
          wrapX: false,
          tileLoadFunction: tileLoadFunction,
        }),
      }),
      new TileLayer({
        title: '天地图卫星图层',
        source: new XYZ({
          url: `http://t0.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=${tiandituKey}`,
          wrapX: false,
        }),
        visible: false,
      }),
    ],
    view: new View({
      center: transform([104.114129, 35.715135], "EPSG:4326", "EPSG:3857"), // 定位到中国中心点
      zoom: 4.5, // 缩放级别调整为4，以显示整个中国范围
    }),
  });

  /*map.value.on('click', (event) => {
    const coordinate = event.coordinate;
    const [lon, lat] = transform(coordinate, 'EPSG:3857', 'EPSG:4326');
    openModal(lat.toFixed(6), lon.toFixed(6));
    canAddDisaster.value = false; // 点击后设置为 false，禁用再次点击添加
    // 添加地图点击事件监听器
    map.value.on('click', handleMapClick);
  });*/
    // 添加点击事件监听器
    map.value.on('click', handleMapClick);
    map.value.on('click', handleMapClick1);
    map.value.on('click', handleMapClick2);
 
});

// 按钮点击事件，启用地图点击
const enableMapClick = () => {
  canAddDisaster2.value = true; // 允许地图点击
};
// 地图点击事件
const handleMapClick1 = (event) => {
  if (canAddDisaster2.value) {
  console.log('地图被点击，坐标:', event.coordinate);
  clickCoordinate.value = event.coordinate;
  showImpactModal.value = true;
  canAddDisaster2.value = false; 
  }
};
// 跳转到受灾地点列表页面
const goToDisasterList = () => {
  router.push('/disaster-list'); 
};
//跳转到避难所列表页面
const goToShelterList = () => {
  router.push('/shelter'); 
};


// 清除应急避难场所
const clearShelters = () => {
  localStorage.removeItem('emergencySheltersData');
  if (shelterLayer.value) {
    shelterLayer.value.getSource().clear();
  }
};

// 跳转到指定经纬度位置
const jumpToLocation = (lat, lon) => {
  if (!lat || !lon) {
    alert('请输入有效的纬度和经度');
    return;
  }




};
</script>

<style scoped>
.map-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  position: relative;
}

.map {
  flex: 1;
  margin: 0; /* 移除外边距 */
  border-radius: 0; /* 移除圆角 */
  box-shadow: none; /* 移除阴影 */
}

.search-container {
  position: absolute;
  top: 52px;
  bottom: 0px;
  left: 0px; /* 修改为左侧 */
  z-index: 1000;
  background: rgba(0, 0, 0, 0.2);
  padding: 5px 5px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 200px; /* 关键调整 */
  max-height: 100vh;
  overflow-y: auto; /* 超出时显示滚动条 */
}

.module {
  width: 100%;
  margin-bottom: 6px;; /* 模块间距 */
}

.module h4 {
  color: rgb(11, 45, 104);
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3); /* 模块标题分隔线 */
  width: 100%;
  text-align: left;
}

.search-container input {
  /* 原有样式保留 */
  background: transparent;
  border: none;
  margin-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  color: white;
  font-size: 14px;
  padding: 0 10px;
  width: 140px;
  outline: none;
}

.search-container button {
  width: 100%; /* 按钮恢复全宽 */
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 8px;
  padding: 6px 12px; /* 添加内边距 */
  border-radius: 4px; /* 添加圆角 */
  transition: all 0.3s ease;
}

.search-container button:hover {
  background-color: #FFFFFF;
  color: #000000;
}

.search-container .search-row {
  display: flex;
  align-items: center;
  width: 100%;
}

.search-container .search-row input {
  flex-grow: 1;
  margin-right: 5px;
  width: auto; /* 让输入框根据内容自适应 */
}

.search-container .search-row button {
  width: auto; /* 搜索按钮恢复非全宽 */
  margin-left: 0;
}

.clear-button {
  color: #ff4444; /* 清除按钮颜色区分 */
}
.disaster-container {
  position: absolute;
  bottom: 20px;
  right: 10px; /* 右侧 */
  z-index: 1000;
  background: rgba(0, 0, 0, 0.2);
  padding: 5px;
  border-radius: 5px;
  display: flex;
  align-items: center;
}

.disaster-container input {
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  color: white;
  font-size: 14px;
  padding: 0 10px;
  width: 100px;
  outline: none;
}

.disaster-container input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.disaster-container button {
  background: transparent;
  border: none;
  color: white;
  margin-left: 5px;
  cursor: pointer;
}

.disaster-container button:hover {
  color: #007bff;
}

.shelter-count-container {
  position: absolute;
  top: 0px;
  right: 0px; /* 修改为左侧 */
  z-index: 1000;
  background: linear-gradient(135deg, #000f2c, #1c2b4d);
  padding: 10px;
  border-radius: 5px;
  color: white;
  font-family: 'Courier New', Courier, monospace;
  font-size: 20px;
  font-weight: bold;
  width: 170px;
  text-align: center;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
}

.modal h3 {
  margin: 0 0 10px;
}

.modal div {
  margin-bottom: 10px;
}

.modal label {
  display: block;
  margin-bottom: 5px;
}

.modal input, .modal select, .modal textarea {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
}

.modal button {
  margin-right: 10px;
  padding: 5px 10px;
  cursor: pointer;
}

.modal button:last-child {
  margin-right: 0;
}

/* 独立搜索面板样式 */
.search-panel {
  position: absolute;
  top: 0px;
  left: 30;
  z-index: 1000;
  background: rgba(0, 0, 0);
  padding: 20px 0px;
  border-radius: 10px;
  /* 继承原search-container的核心样式 */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* 独立地图图层面板样式 */
.layer-panel {
  position: absolute;
  top: 0px;
  left: 220px; /* 示例位置：右上角，可自由调整 */
  z-index: 1000;
  background: rgba(0, 0, 0);
  padding: 20px 10px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
/* 共享模块样式（与原search-container一致） */
.module {
  width: 100%;
  margin-bottom: 12px;
}

.module h4 {
  color: rgb(151, 189, 246);
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 8px;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.search-panel input,
.layer-panel input {
  /* 输入框样式与原一致 */
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  color: white;
  font-size: 14px;
  padding: 0 10px;
  width: 140px;
  outline: none;
}

.search-panel button,
.layer-panel button {
  /* 按钮样式与原一致 */
  width: auto;
  background: transparent;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 8px;
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.search-panel button:hover,
.layer-panel button:hover {
  background-color: #FFFFFF;
  color: #000000;
}

.search-panel .search-row,
.layer-panel .search-row {
  display: flex;
  align-items: center;
  width: 100%;
}

.search-panel .search-row input,
.layer-panel .search-row input {
  flex-grow: 1;
  margin-right: 5px;
}

/* 覆盖层 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* 半透明背景 */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000; /* 确保在地图控件之上 */
    animation: fadeIn 0.3s ease; /* 淡入动画 */
}

/* 模态框主体 */
.modal {
    background: white;
    padding: 24px;
    border-radius: 12px;
    width: 90%;
    max-width: 500px; /* 最大宽度 */
    max-height: 90vh; /* 最大高度 */
    overflow-y: auto; /* 内容过多时滚动 */
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15); /* 阴影提升层次感 */
    animation: slideIn 0.3s ease; /* 滑入动画 */
}

/* 标题 */
.modal h3 {
    color: #2D3748;
    font-size: 20px;
    font-weight: 600;
    margin: 0 0 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid #EDF2F7; /* 底部分隔线 */
}

/* 表单行 */
.modal div {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column; /* 标签在上，输入在下 */
    gap: 8px; /* 标签与输入间距 */
}

/* 标签 */
.modal label {
    color: #4A5568;
    font-size: 14px;
    font-weight: 500;
}

/* 输入框/选择框/文本域 */
.modal input,
.modal select,
.modal textarea {
    padding: 8px 12px;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    font-size: 14px;
    color: #2D3748;
    width: 100%; /* 占满父容器宽度 */
    transition: border-color 0.3s ease;
}

/* 输入框聚焦状态 */
.modal input:focus,
.modal select:focus,
.modal textarea:focus {
    outline: none;
    border-color: #4299E1; /* 蓝色高亮 */
    box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.1); /* 焦点阴影 */
}

/* 文本域 */
.modal textarea {
    min-height: 80px;
    resize: vertical; /* 仅允许垂直调整大小 */
}

/* 文件上传按钮 */
.modal input[type="file"] {
    padding: 6px 12px;
    background: #F7FAFC;
    border-color: #EDF2F7;
}

/* 按钮组 */
.modal button {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 8px;
}

/* 确认按钮 */
.modal button:first-of-type {
    background: #4299E1;
    color: white;
    margin-right: 12px;
}

/* 确认按钮悬停 */
.modal button:first-of-type:hover {
    background: #3182CE;
}

/* 取消按钮 */
.modal button:last-of-type {
    background: #E2E8F0;
    color: #4A5568;
}

/* 取消按钮悬停 */
.modal button:last-of-type:hover {
    background: #CBD5E0;
}

</style>
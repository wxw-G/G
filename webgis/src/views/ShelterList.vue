<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <nav class="top-nav">
      <div class="nav-title">避难所管理</div>
    </nav>

    <!-- 主内容区域 -->
    <div class="content-container">
      <!-- 侧边菜单栏 -->
      <aside class="sidebar">
        <router-link class="menu-item" to="/map">地图服务</router-link>
        <router-link class="menu-item" to="/disaster-list">受灾地点管理</router-link>
        <router-link class="menu-item" to="/shelter">避难场所管理</router-link>
        <router-link class="menu-item" to="/analysis">统计分析</router-link>
      </aside>

      <!-- 避难所列表 -->
      <main class="main-content">
        <div class="shelter-list-container">
          <div class="header">
            <h2 class="title">避难所列表</h2>
            <button @click="openAddShelterModal" class="add-button">添加避难所</button>
          </div>
          <div class="filter-container">
            <input v-model="searchName" placeholder="输入避难所名称" class="filter-input" />
            <input v-model="searchCoordinates" placeholder="输入经纬度" class="filter-input" />
            <select v-model="searchType" class="filter-select">
              <option value="">选择避难所类型</option>
              <option value="Ⅰ">Ⅰ</option>
              <option value="Ⅱ">Ⅱ</option>
              <option value="Ⅲ">Ⅲ</option>
              
            </select>
            <button @click="applyFilters" class="filter-button">筛选</button>
            <button @click="clearFilters" class="filter-button">清除筛选</button>
          </div>
          <table class="shelter-table">
            <thead>
              <tr>
                <th>避难所名称</th>
                <th>类型</th>
                <th>地址</th>
                <th>容量</th>
                <th>联系电话</th>
                <th>经纬度</th>
                <th>无障碍设施</th>
                <th>描述</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(shelter, index) in filteredShelters" :key="index">
                <td>{{ shelter.name }}</td>
                <td>{{ shelter.type }}</td>
                <td>{{ shelter.address }}</td>
                <td>{{ shelter.capacity }}</td>
                <td>{{ shelter.contact }}</td>
                <td>{{ `${shelter.latitude},${shelter.longitude}` }}</td>
                <td>{{ shelter.accessible ? '是' : '否' }}</td>
                <td>{{ shelter.description }}</td>
                <td>
                  <button @click="editShelter(index)" class="edit-button">编辑</button>&emsp;
                  <button @click="deleteShelter1(index)" class="delete-button">删除</button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- 添加避难所的模态窗口 -->
          <div v-if="isAddModalOpen" class="modal-overlay">
            <div class="modal">
              <h3 class="modal-title">添加避难所</h3>
              <div class="form-group">
                <label for="add-shelter-name" class="label">避难所名称：</label>
                <input
                    type="text"
                    id="add-shelter-name"
                    v-model="newShelter.name"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-type" class="label">类型：</label>
                <select
                    id="add-shelter-type"
                    v-model="newShelter.type"
                    class="select"
                >
                  <option value="Ⅰ">Ⅰ</option>
                  <option value="Ⅱ">Ⅱ</option>
                  <option value="Ⅲ">Ⅲ</option>
                </select>
              </div>
              <div class="form-group">
                <label for="add-shelter-address" class="label">地址：</label>
                <input
                    type="text"
                    id="add-shelter-address"
                    v-model="newShelter.address"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-capacity" class="label">容量：</label>
                <input
                    type="number"
                    id="add-shelter-capacity"
                    v-model="newShelter.capacity"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-contact" class="label">联系电话：</label>
                <input
                    type="text"
                    id="add-shelter-contact"
                    v-model="newShelter.contact"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-latitude" class="label">纬度：</label>
                <input
                    type="number"
                    id="add-shelter-latitude"
                    v-model="newShelter.latitude"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-longitude" class="label">经度：</label>
                <input
                    type="number"
                    id="add-shelter-longitude"
                    v-model="newShelter.longitude"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-accessible" class="label">无障碍设施：</label>
                <input
                    type="checkbox"
                    id="add-shelter-accessible"
                    v-model="newShelter.accessible"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="add-shelter-description" class="label">描述：</label>
                <textarea
                    id="add-shelter-description"
                    v-model="newShelter.description"
                    class="textarea"
                ></textarea>
              </div>
              <button @click="addNewShelter" class="save-button">保存</button>
              <button @click="closeAddModal" class="cancel-button">取消</button>
            </div>
          </div>

          <!-- 编辑避难所的模态窗口 -->
          <div v-if="isEditModalOpen" class="modal-overlay">
            <div class="modal">
              <h3 class="modal-title">编辑避难所</h3>
              <div class="form-group">
                <label for="edit-shelter-name" class="label">避难所名称：</label>
                <input
                    type="text"
                    id="edit-shelter-name"
                    v-model="currentShelter.name"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-type" class="label">类型：</label>
                <select
                    id="edit-shelter-type"
                    v-model="currentShelter.type"
                    class="select">
                <option value="Ⅰ">Ⅰ</option>
                  <option value="Ⅱ">Ⅱ</option>
                  <option value="Ⅲ">Ⅲ</option>
                </select>
              </div>
              <div class="form-group">
                <label for="edit-shelter-address" class="label">地址：</label>
                <input
                    type="text"
                    id="edit-shelter-address"
                    v-model="currentShelter.address"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-capacity" class="label">容量：</label>
                <input
                    type="number"
                    id="edit-shelter-capacity"
                    v-model="currentShelter.capacity"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-contact" class="label">联系电话：</label>
                <input
                    type="text"
                    id="edit-shelter-contact"
                    v-model="currentShelter.contact"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-latitude" class="label">纬度：</label>
                <input
                    type="number"
                    id="edit-shelter-latitude"
                    v-model="currentShelter.latitude"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-longitude" class="label">经度：</label>
                <input
                    type="number"
                    id="edit-shelter-longitude"
                    v-model="currentShelter.longitude"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-accessible" class="label">无障碍设施：</label>
                <input
                    type="checkbox"
                    id="edit-shelter-accessible"
                    v-model="currentShelter.accessible"
                    class="input"
                />
              </div>
              <div class="form-group">
                <label for="edit-shelter-description" class="label">描述：</label>
                <textarea
                    id="edit-shelter-description"
                    v-model="currentShelter.description"
                    class="textarea"
                ></textarea>
              </div>
              <button @click="saveShelter" class="save-button">保存</button>
              <button @click="closeEditModal" class="cancel-button">取消</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { getAllShelters, addShelter, updateShelter, deleteShelter } from '@/api/shelterApi.js';

const shelterList = ref([]);
const filteredShelters = ref([]);
const isEditModalOpen = ref(false);
const isAddModalOpen = ref(false);
const currentShelter = ref({});
const currentShelterIndex = ref(-1);
const newShelter = ref({ name: '', type: '', address: '', capacity: null, contact: '', latitude: null, longitude: null, accessible: false, description: '' });

// 筛选条件
const searchName = ref('');
const searchCoordinates = ref('');
const searchType = ref('');

// 从数据库中读取数据
const loadShelterLocations = () => {
  getAllShelters().then(response => {
    shelterList.value = response.data.data;
    filteredShelters.value = shelterList.value; // 初始化筛选结果
  }).catch(error => {
    console.error('Error fetching shelters:', error);
  });
};

// 在组件挂载时读取数据
onMounted(() => {
  loadShelterLocations();
});

const editShelter = (index) => {
  currentShelterIndex.value = index;
  currentShelter.value = { ...shelterList.value[index] };
  isEditModalOpen.value = true;
};

const saveShelter = () => {
  if (currentShelterIndex.value !== -1) {
    updateShelter(currentShelter.value.id, currentShelter.value).then(() => {
      console.log('Shelter updated');
      loadShelterLocations(); // Reload the list
    }).catch(error => {
      console.error('Error updating shelter:', error);
    });
  } else {
    addShelter(newShelter.value).then(() => {
      console.log('Shelter added');
      loadShelterLocations(); // Reload the list
    }).catch(error => {
      console.error('Error adding shelter:', error);
    });
  }
  closeEditModal();
};

const closeEditModal = () => {
  isEditModalOpen.value = false;
  currentShelter.value = {};
  currentShelterIndex.value = -1;
};

const openAddShelterModal = () => {
  isAddModalOpen.value = true;
};

const addNewShelter = () => {
  addShelter(newShelter.value).then(() => {
    console.log('Shelter added');
    loadShelterLocations(); // Reload the list
  }).catch(error => {
    console.error('Error adding shelter:', error);
  });
  closeAddModal();
};

const closeAddModal = () => {
  isAddModalOpen.value = false;
  newShelter.value = { name: '', type: '', address: '', capacity: null, contact: '', latitude: null, longitude: null, accessible: false, description: '' };
};

// 应用筛选条件
const applyFilters = () => {
  filteredShelters.value = shelterList.value.filter(shelter => {
    return (
      (!searchName.value || shelter.name.includes(searchName.value)) &&
      (!searchCoordinates.value || `${shelter.latitude},${shelter.longitude}`.includes(searchCoordinates.value)) &&
      (!searchType.value || shelter.type === searchType.value)
    );
  });
};

// 清除筛选条件
const clearFilters = () => {
  searchName.value = '';
  searchCoordinates.value = '';
  searchType.value = '';
  filteredShelters.value = shelterList.value; // 重置筛选结果为全部数据
};

// 删除避难所
const deleteShelter1 = async (index) => {
  if (!confirm('确定要删除这个避难所吗？')) {
    console.log('用户取消了删除操作');
    return;
  }

  const shelterId = shelterList.value[index].id; // 从shelterList中获取当前行的避难所ID
  console.log('尝试删除的避难所ID:', shelterId); // 打印shelterId

  try {
    const response = await deleteShelter(shelterId);
    console.log('完整响应:', response);

    // 检查HTTP状态码
    if (response.status === 200) {
      // 检查后端返回的自定义状态
      if (response.data?.status === 'success') {
        alert('避难所已成功删除');
        loadShelterLocations(); // 重新加载列表
      } else {
        throw new Error(response.data?.message || '删除操作未成功');
      }
    } else {
      throw new Error(`服务器返回状态码: ${response.status}`);
    }
  } catch (error) {
    console.error('删除过程中出错:', error);
    
    let errorMessage = '删除失败: ';
    if (error.response) {
      // 服务器有响应但状态码不是2xx
      errorMessage += `服务器错误 (${error.response.status})`;
      if (error.response.data?.message) {
        errorMessage += `: ${error.response.data.message}`;
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      errorMessage += '无法连接到服务器';
    } else {
      // 其他错误
      errorMessage += error.message;
    }
    
    alert(errorMessage);
    
    // 如果是405错误，特别提示
    if (error.response?.status === 405) {
      console.error('请检查:');
      console.error('1. 后端路由是否正确配置了DELETE方法');
      console.error('2. 前端是否正确发送了DELETE请求');
      console.error('3. 是否存在跨域问题');
    }
  }
};

</script>
<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.top-nav {
  background-color: #003344;
  color: white;
  padding: 10px 20px;
  font-size: 20px;
  font-weight: bold;
}

.content-container {
  display: flex;
  flex: 1;
}

.sidebar {
  background-color: #003344;
  width: 200px;
  padding: 20px;
  border-right: 1px solid #ccc;
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 菜单项聚集在顶部 */
  height: 100%;
}

.menu-item {
  position: relative; /* 用于绝对定位分割线 */
  padding: 10px 0; /* 上下内边距 */
  cursor: pointer;
  font-size: 16px;
  color: #FFFFFF; /* 默认字体颜色 */
  text-decoration: none; /* 移除下划线 */
}

.menu-item:hover {
  background-color: #e0e0e0; /* 鼠标悬停时的背景颜色 */
  color: #007bff; /* 鼠标悬停时的字体颜色 */
}

.menu-item::after {
  content: ""; /* 创建伪元素 */
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px; /* 分割线高度 */
  background-color: #ccc; /* 分割线颜色 */
}

/* 最后一个菜单项不需要分割线 */
.menu-item:last-child::after {
  display: none;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow: auto;
}

.shelter-list-container {
  max-width: 100%;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  font-size: 20px;
  font-weight: bold;
  text-align: left;
}

.add-button {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.add-button:hover {
  background-color: #1e6e35;
}

.shelter-table {
  width: 100%;
  border-collapse: collapse;
}

.shelter-table th,
.shelter-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
}

.shelter-table th {
  background-color: #f2f2f2;
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-input, .filter-select, .filter-button {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.filter-button {
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.filter-button:hover {
  background-color: #0056b3;
}

.edit-button {
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-button:hover {
  background-color: #0056b3;
}

.delete-button {
  background-color: #ff0000;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:hover {
  background-color: #b3000f;
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



.form-group {
  margin-bottom: 15px;
}

.label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
}

.input, .select, .textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.save-button, .cancel-button {
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #1e6e35;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #a71d2a;
}
</style>
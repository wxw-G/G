import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000',  // 修正baseURL
    withCredentials: true,
    timeout: 5000
});

// 获取所有受灾地点
export const getAllDisasters = () => {
    return api.get('/auth/disaster-list');
};

// 添加受灾地点
export const addDisaster = (disasterData) => {
    // 前端已经提供了正确的字段名称，不需要重命名
    // 只需直接传递数据即可
    const payload = {
        location_name: disasterData.location_name,
        disaster_type: disasterData.disaster_type,
        description: disasterData.description,
        timestamp: disasterData.timestamp,
        latitude: parseFloat(disasterData.latitude),
        longitude: parseFloat(disasterData.longitude)
    };
    
    console.log("发送到API的数据:", payload); // 调试用
    
    return api.post('/auth/disaster-list', payload);
};

// 更新受灾地点
export const updateDisaster = (id, disasterData) => {
    const [latitude, longitude] = disasterData.coordinates.split(',').map(coord => coord.trim());
    
    const payload = {
        location_name: disasterData.name,
        disaster_type: disasterData.type,
        description: disasterData.description,
        timestamp: disasterData.time,
        latitude,
        longitude
    };
    
    return api.put(`/auth/disaster-list/${id}`, payload);
};

// 删除受灾地点
export const deleteDisaster = (id) => {
    return api.delete(`/auth/disaster-list/${id}`);
};
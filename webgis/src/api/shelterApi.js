import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000',  // 修正baseURL
    withCredentials: true,
    timeout: 5000
});

// 获取所有应急避难所
export const getAllShelters = () => {
    return api.get('/auth/shelter-list');
};

// 添加应急避难所
export const addShelter = (shelterData) => {
    const payload = {
        name: shelterData.name,
        type: shelterData.type,
        capacity: shelterData.capacity,
        address: shelterData.address,
        contact_number: shelterData.contactNumber,
        latitude: shelterData.latitude,
        longitude: shelterData.longitude,
        is_accessible: shelterData.isAccessible,
        description: shelterData.description
    };
    
    return api.post('/auth/shelter-list', payload);
};

// 更新应急避难所
export const updateShelter = (id, shelterData) => {
    const payload = {
        name: shelterData.name,
        type: shelterData.type,
        capacity: shelterData.capacity,
        address: shelterData.address,
        contact_number: shelterData.contactNumber,
        latitude: shelterData.latitude,
        longitude: shelterData.longitude,
        is_accessible: shelterData.isAccessible,
        description: shelterData.description
    };
    
    return api.put(`/auth/shelter-list/${id}`, payload);
};

// 删除应急避难所
export const deleteShelter = (id) => {
    return api.delete(`/auth/shelter-list/${id}`);
};
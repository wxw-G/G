import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:5000',  // 指向Flask后端
    withCredentials: true,  // 允许携带cookie
    timeout: 5000
})

// 用户登录
export const login = (username, password) => {
    return api.post('/auth/login', {
        username,
        password
    })
}

// 用户注册
export const register = (username, password, email) => {
    return api.post('/auth/register', {
        username,
        password,
        email
    })
}

// 检查会话
export const checkSession = () => {
    return api.get('/auth/check-session')
}
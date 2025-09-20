import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('ycrm_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // token 过期或无效，清除本地存储并跳转到登录页
          localStorage.removeItem('ycrm_token')
          localStorage.removeItem('ycrm_user')
          ElMessage.error('登录已过期，请重新登录')
          router.push('/login')
          break
        case 422:
          // 请求参数错误
          ElMessage.error('请求参数错误')
          break
        case 500:
          // 服务器错误
          ElMessage.error('服务器内部错误')
          break
        default:
          // 其他错误
          ElMessage.error('请求失败')
      }
    } else if (error.request) {
      // 网络错误
      ElMessage.error('网络连接失败')
    } else {
      // 其他错误
      ElMessage.error('请求失败')
    }
    return Promise.reject(error)
  }
)

// 认证相关 API
export const authAPI = {
  // 用户注册
  register: (userData) => api.post('/register', userData),
  
  // 用户登录
  login: (credentials) => api.post('/login', credentials)
}

// 用户相关 API
export const userAPI = {
  // 获取所有用户
  getUsers: () => api.get('/users'),
  
  // 创建用户
  createUser: (userData) => api.post('/users', userData),
  
  // 更新用户
  updateUser: (id, userData) => api.put(`/users/${id}`, userData),
  
  // 删除用户
  deleteUser: (id) => api.delete(`/users/${id}`)
}

// 客户相关 API
export const customerAPI = {
  // 获取所有客户
  getCustomers: () => api.get('/customers'),
  
  // 创建客户
  createCustomer: (customerData) => api.post('/customers', customerData),
  
  // 更新客户
  updateCustomer: (id, customerData) => api.put(`/customers/${id}`, customerData),
  
  // 删除客户
  deleteCustomer: (id) => api.delete(`/customers/${id}`)
}

// 跟进记录相关 API
export const followupAPI = {
  // 获取所有跟进记录
  getFollowups: () => api.get('/followups'),
  
  // 创建跟进记录
  createFollowup: (followupData) => api.post('/followups', followupData),
  
  // 更新跟进记录
  updateFollowup: (id, followupData) => api.put(`/followups/${id}`, followupData),
  
  // 删除跟进记录
  deleteFollowup: (id) => api.delete(`/followups/${id}`)
}

// 商机相关 API
export const opportunityAPI = {
  // 获取所有商机
  getOpportunities: () => api.get('/opportunities'),
  
  // 创建商机
  createOpportunity: (opportunityData) => api.post('/opportunities', opportunityData),
  
  // 更新商机
  updateOpportunity: (id, opportunityData) => api.put(`/opportunities/${id}`, opportunityData),
  
  // 删除商机
  deleteOpportunity: (id) => api.delete(`/opportunities/${id}`)
}

// 订单相关 API
export const orderAPI = {
  // 获取所有订单
  getOrders: () => api.get('/orders'),
  
  // 创建订单
  createOrder: (orderData) => api.post('/orders', orderData),
  
  // 更新订单
  updateOrder: (id, orderData) => api.put(`/orders/${id}`, orderData),
  
  // 删除订单
  deleteOrder: (id) => api.delete(`/orders/${id}`)
}

// 任务相关 API
export const taskAPI = {
  // 获取所有任务
  getTasks: () => api.get('/tasks'),
  
  // 创建任务
  createTask: (taskData) => api.post('/tasks', taskData)
}

// 部门相关 API
export const departmentAPI = {
  // 获取所有部门
  getDepartments: () => api.get('/departments'),
  
  // 创建部门
  createDepartment: (departmentData) => api.post('/departments', departmentData),
  
  // 更新部门
  updateDepartment: (id, departmentData) => api.put(`/departments/${id}`, departmentData),
  
  // 删除部门
  deleteDepartment: (id) => api.delete(`/departments/${id}`)
}

// 角色相关 API
export const roleAPI = {
  // 获取所有角色
  getRoles: () => api.get('/roles'),
  
  // 创建角色
  createRole: (roleData) => api.post('/roles', roleData),
  
  // 更新角色
  updateRole: (id, roleData) => api.put(`/roles/${id}`, roleData),
  
  // 删除角色
  deleteRole: (id) => api.delete(`/roles/${id}`)
}

export default api
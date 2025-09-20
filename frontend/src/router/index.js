import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/layout',
    name: 'Layout',
    component: Layout,
    children: [
      {
        path: 'dashboard',  // 修复：移除开头的斜杠
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'customers',  // 修复：移除开头的斜杠
        name: 'Customers',
        component: () => import('../views/Customers.vue')
      },
      {
        path: 'followups',  // 修复：移除开头的斜杠
        name: 'FollowUps',
        component: () => import('../views/FollowUps.vue')
      },
      {
        path: 'opportunities',  // 修复：移除开头的斜杠
        name: 'Opportunities',
        component: () => import('../views/Opportunities.vue')
      },
      {
        path: 'orders',  // 修复：移除开头的斜杠
        name: 'Orders',
        component: () => import('../views/Orders.vue')
      },
      {
        path: 'tasks',  // 修复：移除开头的斜杠
        name: 'Tasks',
        component: () => import('../views/Tasks.vue')
      },
      {
        path: 'users',  // 添加用户管理路由
        name: 'Users',
        component: () => import('../views/Users.vue')
      },
      {
        path: 'departments',  // 添加部门管理路由
        name: 'Departments',
        component: () => import('../views/Departments.vue')
      },
      {
        path: 'roles',  // 添加角色管理路由
        name: 'Roles',
        component: () => import('../views/Roles.vue')
      }
    ],
    meta: { requiresAuth: true } // 添加需要认证的标记
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查用户是否已登录（检查本地存储中的token）
    const token = localStorage.getItem('ycrm_token')
    if (!token) {
      // 如果没有token，重定向到登录页面
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // 如果有token，允许访问
      next()
    }
  } else {
    // 如果路由不需要认证，直接允许访问
    next()
  }
})

export default router
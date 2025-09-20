<template>
  <el-container class="layout-container">
    <el-header class="layout-header">
      <div class="header-left">
        <h1>YCRM 客户关系管理系统</h1>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleUserCommand">
          <span class="user-info">
            <el-avatar :size="30" icon="UserFilled" />
            <span class="username">{{ currentUser.username }}</span>
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="settings">系统设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-container>
      <el-aside width="220px" class="layout-aside">
        <el-menu
          :default-active="activeMenu"
          class="layout-menu"
          @select="handleMenuSelect"
          router
        >
          <el-menu-item index="/layout/dashboard">
            <el-icon><Odometer /></el-icon>
            <span>仪表板</span>
          </el-menu-item>
          <el-menu-item index="/layout/customers">
            <el-icon><User /></el-icon>
            <span>客户管理</span>
          </el-menu-item>
          <el-menu-item index="/layout/followups">
            <el-icon><ChatDotRound /></el-icon>
            <span>销售跟进</span>
          </el-menu-item>
          <el-menu-item index="/layout/opportunities">
            <el-icon><Trophy /></el-icon>
            <span>商机管理</span>
          </el-menu-item>
          <el-menu-item index="/layout/orders">
            <el-icon><Document /></el-icon>
            <span>订单管理</span>
          </el-menu-item>
          <el-menu-item index="/layout/tasks">
            <el-icon><Check /></el-icon>
            <span>任务管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Odometer, 
  User, 
  ChatDotRound, 
  Trophy, 
  Document, 
  Check,
  ArrowDown
} from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: {
    Odometer,
    User,
    ChatDotRound,
    Trophy,
    Document,
    Check,
    ArrowDown
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const activeMenu = ref(route.name?.toLowerCase() || 'dashboard')
    const currentUser = ref({ username: '管理员' })
    
    // 页面加载时获取当前用户信息
    onMounted(() => {
      const user = localStorage.getItem('ycrm_user')
      if (user) {
        currentUser.value = JSON.parse(user)
      }
      
      // 设置当前激活的菜单项
      activeMenu.value = route.name?.toLowerCase() || 'dashboard'
    })
    
    const handleMenuSelect = (index) => {
      activeMenu.value = index
      router.push(index)
    }
    
    const handleUserCommand = (command) => {
      if (command === 'logout') {
        // 退出登录
        localStorage.removeItem('ycrm_token')
        localStorage.removeItem('ycrm_user')
        router.push('/login')
      } else if (command === 'profile') {
        // 个人中心
        router.push('/profile')
      } else if (command === 'settings') {
        // 系统设置
        router.push('/settings')
      }
    }
    
    return {
      activeMenu,
      currentUser,
      handleMenuSelect,
      handleUserCommand
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.layout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  color: #303133;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #ebeef5;
}

.header-left h1 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #409EFF;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #606266;
}

.username {
  margin: 0 8px;
  font-size: 14px;
}

.layout-aside {
  background-color: #ffffff;
  box-shadow: 1px 0 4px rgba(0, 0, 0, 0.1);
  border-right: 1px solid #ebeef5;
}

.layout-menu {
  border-right: none;
  height: 100%;
}

.layout-main {
  background-color: #f5f7fa;
  padding: 20px;
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}

:deep(.el-menu-item.is-active) {
  background-color: #ecf5ff;
  color: #409EFF;
}
</style>
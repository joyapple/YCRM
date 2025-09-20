<template>
  <div id="app">
    <el-container v-if="isLoggedIn">
      <el-header>
        <div class="header-content">
          <h1>YCRM 客户关系管理系统</h1>
          <div class="user-info">
            <span>欢迎, {{ currentUser.username }}</span>
            <el-button type="text" @click="handleLogout">退出</el-button>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical"
            @select="handleMenuSelect"
          >
            <el-menu-item index="dashboard">
              <i class="el-icon-menu"></i>
              <span slot="title">仪表板</span>
            </el-menu-item>
            <el-menu-item index="customers">
              <i class="el-icon-user"></i>
              <span slot="title">客户管理</span>
            </el-menu-item>
            <el-menu-item index="followups">
              <i class="el-icon-chat-dot-round"></i>
              <span slot="title">销售跟进</span>
            </el-menu-item>
            <el-menu-item index="opportunities">
              <i class="el-icon-trophy"></i>
              <span slot="title">商机管理</span>
            </el-menu-item>
            <el-menu-item index="orders">
              <i class="el-icon-document"></i>
              <span slot="title">订单管理</span>
            </el-menu-item>
            <el-menu-item index="tasks">
              <i class="el-icon-check"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <Dashboard v-if="activeMenu === 'dashboard'" />
          <Customers v-if="activeMenu === 'customers'" />
          <FollowUps v-if="activeMenu === 'followups'" />
          <Opportunities v-if="activeMenu === 'opportunities'" />
          <Orders v-if="activeMenu === 'orders'" />
          <Tasks v-if="activeMenu === 'tasks'" />
        </el-main>
      </el-container>
    </el-container>
    <Login 
      v-else-if="showLogin" 
      @login-success="handleLoginSuccess" 
      @switch-to-register="showLogin = false; showRegister = true"
    />
    <Register 
      v-else 
      @register-success="handleRegisterSuccess" 
      @switch-to-login="showRegister = false; showLogin = true"
    />
  </div>
</template>

<script>
import Login from './Login.vue'
import Register from './Register.vue'
import Dashboard from './Dashboard.vue'
import Customers from './Customers.vue'
import FollowUps from './FollowUps.vue'
import Opportunities from './Opportunities.vue'
import Orders from './Orders.vue'
import Tasks from './Tasks.vue'

export default {
  name: 'App',
  components: {
    Login,
    Register,
    Dashboard,
    Customers,
    FollowUps,
    Opportunities,
    Orders,
    Tasks
  },
  data() {
    return {
      isLoggedIn: false,
      showLogin: true,
      showRegister: false,
      currentUser: {},
      activeMenu: 'dashboard'
    }
  },
  methods: {
    handleLoginSuccess(user) {
      this.isLoggedIn = true
      this.currentUser = user
    },
    handleRegisterSuccess(user) {
      this.showRegister = false
      this.showLogin = true
      // 可以显示注册成功的提示信息
    },
    handleLogout() {
      this.isLoggedIn = false
      this.currentUser = {}
    },
    handleMenuSelect(index) {
      this.activeMenu = index
    }
  }
}
</script>

<style scoped>
#app {
  height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: white;
  line-height: 60px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 15px;
}

.el-aside {
  background-color: #f5f5f5;
}

.el-menu-vertical {
  height: 100%;
}
</style>
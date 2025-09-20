<template>
  <div class="login-container">
    <div class="login-card">
      <el-card class="login-box">
        <div class="login-header">
          <h2>YCRM 系统登录</h2>
          <p class="subtitle">企业客户关系管理系统</p>
        </div>
        
        <el-form 
          :model="loginForm" 
          :rules="loginRules" 
          ref="loginFormRef" 
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input 
              v-model="loginForm.username" 
              placeholder="请输入用户名" 
              prefix-icon="User"
              size="large"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="请输入密码" 
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              native-type="submit"
              :loading="loading"
              class="login-button"
              style="width: 100%"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="login-footer">
          <span>还没有账号？</span>
          <el-button type="primary" link @click="handleRegister">立即注册</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../services/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const loading = ref(false)
    
    const loginForm = reactive({
      username: 'admin',
      password: 'admin123'
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
      ]
    }
    
    const handleLogin = () => {
      loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 调用后端登录接口
            const response = await authAPI.login({
              username: loginForm.username,
              password: loginForm.password
            })
            
            if (response.data.status === 'success') {
              // 保存 token 和用户信息到 localStorage
              localStorage.setItem('ycrm_token', response.data.access_token)
              localStorage.setItem('ycrm_user', JSON.stringify(response.data.user))
              
              // 登录成功，跳转到主页面
              ElMessage.success('登录成功')
              router.push('/layout/dashboard')
            } else {
              ElMessage.error(response.data.message || '登录失败')
            }
          } catch (error) {
            console.error('Login error:', error)
            ElMessage.error('登录失败，请检查用户名和密码')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const handleRegister = () => {
      router.push('/register')
    }
    
    return {
      loginForm,
      loginRules,
      loginFormRef,
      loading,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 450px;
}

.login-box {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  margin: 0 0 10px 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-button {
  margin-top: 10px;
}

.login-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #606266;
  font-size: 14px;
}

:deep(.el-card__body) {
  padding: 40px;
}

@media (max-width: 768px) {
  :deep(.el-card__body) {
    padding: 30px 20px;
  }
  
  .login-card {
    max-width: 100%;
  }
}
</style>
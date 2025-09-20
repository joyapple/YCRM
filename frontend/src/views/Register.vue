<template>
  <div class="register-container">
    <div class="register-card">
      <el-card class="register-box">
        <div class="register-header">
          <h2>YCRM 用户注册</h2>
          <p class="subtitle">创建您的账户</p>
        </div>
        
        <el-form 
          :model="registerForm" 
          :rules="registerRules" 
          ref="registerFormRef" 
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input 
              v-model="registerForm.username" 
              placeholder="请输入用户名" 
              prefix-icon="User"
              size="large"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="email">
            <el-input 
              v-model="registerForm.email" 
              placeholder="请输入邮箱" 
              prefix-icon="Message"
              size="large"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input 
              v-model="registerForm.password" 
              type="password" 
              placeholder="请输入密码" 
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input 
              v-model="registerForm.confirmPassword" 
              type="password" 
              placeholder="请确认密码" 
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
              class="register-button"
              style="width: 100%"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="register-footer">
          <span>已有账号？</span>
          <el-button type="primary" link @click="handleLogin">立即登录</el-button>
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
  name: 'Register',
  setup() {
    const router = useRouter()
    const registerFormRef = ref(null)
    const loading = ref(false)
    
    const registerForm = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const validatePassword = (rule, value, callback) => {
      if (value !== registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    const registerRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        { validator: validatePassword, trigger: 'blur' }
      ]
    }
    
    const handleRegister = () => {
      registerFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 调用后端注册接口
            const response = await authAPI.register({
              username: registerForm.username,
              email: registerForm.email,
              password: registerForm.password
            })
            
            if (response.data.status === 'success') {
              ElMessage.success('注册成功')
              // 注册成功，跳转到登录页面
              router.push('/login')
            } else {
              ElMessage.error(response.data.message || '注册失败')
            }
          } catch (error) {
            console.error('Register error:', error)
            ElMessage.error('注册失败，请稍后重试')
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const handleLogin = () => {
      router.push('/login')
    }
    
    return {
      registerForm,
      registerRules,
      registerFormRef,
      loading,
      handleRegister,
      handleLogin
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 450px;
}

.register-box {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
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

.register-form {
  margin-bottom: 20px;
}

.register-button {
  margin-top: 10px;
}

.register-footer {
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
  
  .register-card {
    max-width: 100%;
  }
}
</style>
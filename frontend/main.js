import { createApp, ref } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 创建 Vue 应用实例
const app = createApp({
  setup() {
    const isLoggedIn = ref(false);
    const showLogin = ref(true);
    const showRegister = ref(false);
    const currentUser = ref({});
    
    const loginForm = ref({
      username: '',
      password: ''
    });
    
    const registerForm = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    });
    
    const handleLogin = () => {
      showLogin.value = true;
      showRegister.value = false;
    };
    
    const handleRegister = () => {
      showRegister.value = true;
      showLogin.value = false;
    };
    
    const handleLoginSubmit = () => {
      console.log('登录表单:', loginForm.value);
      // 这里应该调用后端API进行登录
      // 模拟登录成功
      isLoggedIn.value = true;
      currentUser.value = { username: loginForm.value.username };
    };
    
    const handleRegisterSubmit = () => {
      console.log('注册表单:', registerForm.value);
      // 这里应该调用后端API进行注册
      // 模拟注册成功并直接登录
      isLoggedIn.value = true;
      currentUser.value = { username: registerForm.value.username };
    };
    
    const handleLogout = () => {
      isLoggedIn.value = false;
      currentUser.value = {};
      loginForm.value = { username: '', password: '' };
    };
    
    return {
      isLoggedIn,
      showLogin,
      showRegister,
      currentUser,
      loginForm,
      registerForm,
      handleLogin,
      handleRegister,
      handleLoginSubmit,
      handleRegisterSubmit,
      handleLogout
    };
  }
})

// 使用 Element Plus
app.use(ElementPlus)

// 挂载应用
app.mount('#app')
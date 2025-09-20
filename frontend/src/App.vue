<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  height: 100vh;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', Arial, sans-serif;
}

/* 全局卡片样式 */
:root {
  --el-card-border-radius: 8px;
  --el-box-shadow-light: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 全局按钮样式 */
:root {
  --el-border-radius-base: 4px;
}

/* 全局表单样式 */
:root {
  --el-form-label-font-size: 14px;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .el-form-item {
    margin-bottom: 18px;
  }
  
  .el-card {
    margin-bottom: 15px;
  }
}
</style>
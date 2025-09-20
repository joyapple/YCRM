<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-user stat-icon"></i>
            <div class="stat-info">
              <p class="stat-title">客户总数</p>
              <p class="stat-number">128</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-chat-dot-round stat-icon"></i>
            <div class="stat-info">
              <p class="stat-title">今日跟进</p>
              <p class="stat-number">24</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-trophy stat-icon"></i>
            <div class="stat-info">
              <p class="stat-title">进行中商机</p>
              <p class="stat-number">15</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <i class="el-icon-document stat-icon"></i>
            <div class="stat-info">
              <p class="stat-title">本月订单</p>
              <p class="stat-number">32</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="16">
        <el-card>
          <div slot="header">
            <span>销售趋势</span>
          </div>
          <div class="chart-container">
            <p>销售趋势图表将在这里显示</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">
            <span>最新活动</span>
          </div>
          <div class="activity-list">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in activities"
                :key="index"
                :timestamp="activity.timestamp">
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      activities: [
        {
          content: '张三 创建了新客户 - ABC公司',
          timestamp: '2023-05-20'
        },
        {
          content: '李四 完成了客户跟进 - XYZ集团',
          timestamp: '2023-05-19'
        },
        {
          content: '王五 创建了新订单 - ORD20230519001',
          timestamp: '2023-05-19'
        },
        {
          content: '赵六 更新了商机状态 - 重要项目',
          timestamp: '2023-05-18'
        }
      ]
    }
  }
}
</script>

<style scoped>
.stat-card {
  border-radius: 8px;
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  font-size: 36px;
  color: #409EFF;
  margin-right: 15px;
}

.stat-info {
  text-align: center;
}

.stat-title {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.stat-number {
  margin: 5px 0 0;
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.chart-container {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-list {
  height: 300px;
  overflow-y: auto;
}
</style>
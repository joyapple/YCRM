<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon customers">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.customers }}</div>
              <div class="stat-label">客户数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon followups">
              <el-icon><ChatLineRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.followups }}</div>
              <div class="stat-label">跟进记录</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon opportunities">
              <el-icon><Trophy /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.opportunities }}</div>
              <div class="stat-label">商机数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon orders">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stats.orders }}</div>
              <div class="stat-label">订单数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="charts-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>客户增长趋势</span>
            </div>
          </template>
          <div ref="customerChart" class="chart-container"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>销售业绩</span>
            </div>
          </template>
          <div ref="salesChart" class="chart-container"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { customerAPI, followupAPI, opportunityAPI, orderAPI } from '../services/api'
import { ElMessage } from 'element-plus'
import { User, ChatLineRound, Trophy, Document } from '@element-plus/icons-vue'

export default {
  name: 'Dashboard',
  components: {
    User,
    ChatLineRound,
    Trophy,
    Document
  },
  setup() {
    const stats = ref({
      customers: 0,
      followups: 0,
      opportunities: 0,
      orders: 0
    })
    
    const customerChart = ref(null)
    const salesChart = ref(null)
    let customerChartInstance = null
    let salesChartInstance = null
    
    // 获取统计数据
    const fetchStats = async () => {
      try {
        // 检查用户是否已登录
        const token = localStorage.getItem('ycrm_token')
        if (!token) {
          ElMessage.error('请先登录')
          return
        }
        
        // 并行获取所有统计数据
        const [customersRes, followupsRes, opportunitiesRes, ordersRes] = await Promise.all([
          customerAPI.getCustomers(),
          followupAPI.getFollowups(),
          opportunityAPI.getOpportunities(),
          orderAPI.getOrders()
        ])
        
        stats.value.customers = customersRes.data.customers?.length || 0
        stats.value.followups = followupsRes.data.followups?.length || 0
        stats.value.opportunities = opportunitiesRes.data.opportunities?.length || 0
        stats.value.orders = ordersRes.data.orders?.length || 0
      } catch (error) {
        console.error('Fetch stats error:', error)
        ElMessage.error('获取统计数据失败')
      }
    }
    
    // 初始化图表
    const initCharts = () => {
      if (customerChart.value) {
        customerChartInstance = echarts.init(customerChart.value)
        customerChartInstance.setOption({
          xAxis: {
            type: 'category',
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              data: [120, 200, 150, 80, 70, 110, 130],
              type: 'bar',
              color: '#409EFF'
            }
          ]
        })
      }
      
      if (salesChart.value) {
        salesChartInstance = echarts.init(salesChart.value)
        salesChartInstance.setOption({
          tooltip: {
            trigger: 'item'
          },
          legend: {
            top: '5%',
            left: 'center'
          },
          series: [
            {
              name: '销售额',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '18',
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: [
                { value: 1048, name: '产品A' },
                { value: 735, name: '产品B' },
                { value: 580, name: '产品C' },
                { value: 484, name: '产品D' },
                { value: 300, name: '产品E' }
              ]
            }
          ]
        })
      }
    }
    
    // 窗口大小改变时重置图表
    const handleResize = () => {
      if (customerChartInstance) {
        customerChartInstance.resize()
      }
      if (salesChartInstance) {
        salesChartInstance.resize()
      }
    }
    
    onMounted(() => {
      fetchStats()
      initCharts()
      window.addEventListener('resize', handleResize)
    })
    
    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize)
      if (customerChartInstance) {
        customerChartInstance.dispose()
      }
      if (salesChartInstance) {
        salesChartInstance.dispose()
      }
    })
    
    return {
      stats,
      customerChart,
      salesChart
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.stat-content {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 24px;
}

.stat-icon.customers {
  background-color: #ecf5ff;
  color: #409eff;
}

.stat-icon.followups {
  background-color: #f0f9eb;
  color: #67c23a;
}

.stat-icon.opportunities {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.stat-icon.orders {
  background-color: #f4f4f5;
  color: #909399;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.charts-row {
  margin-top: 20px;
}

.chart-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  font-weight: bold;
  color: #303133;
}

.chart-container {
  width: 100%;
  height: 300px;
}
</style>
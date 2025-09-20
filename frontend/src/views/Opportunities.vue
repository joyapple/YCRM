<template>
  <div class="opportunities">
    <el-card class="opportunities-card">
      <div slot="header" class="clearfix">
        <span>商机管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增商机</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="商机名称">
          <el-input v-model="searchForm.name" placeholder="商机名称" clearable />
        </el-form-item>
        <el-form-item label="客户">
          <el-select v-model="searchForm.customerId" placeholder="请选择客户" clearable>
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="进行中" value="open" />
            <el-option label="已成交" value="won" />
            <el-option label="已丢失" value="lost" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 商机列表 -->
      <el-table :data="opportunities" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="商机名称" />
        <el-table-column prop="customerName" label="客户名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="estimatedAmount" label="预估金额" width="120">
          <template #default="scope">
            ¥{{ scope.row.estimatedAmount }}
          </template>
        </el-table-column>
        <el-table-column prop="probability" label="成交概率" width="100">
          <template #default="scope">
            {{ scope.row.probability }}%
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        class="pagination"
      />
    </el-card>
    
    <!-- 商机编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="currentOpportunity" :rules="opportunityRules" ref="opportunityFormRef" label-width="120px">
        <el-form-item label="商机名称" prop="name">
          <el-input v-model="currentOpportunity.name" />
        </el-form-item>
        <el-form-item label="客户" prop="customerId">
          <el-select v-model="currentOpportunity.customerId" placeholder="请选择客户" style="width: 100%;">
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="currentOpportunity.description" :rows="3" />
        </el-form-item>
        <el-form-item label="预估金额" prop="estimatedAmount">
          <el-input-number v-model="currentOpportunity.estimatedAmount" :min="0" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="成交概率(%)" prop="probability">
          <el-slider v-model="currentOpportunity.probability" :min="0" :max="100" show-input />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentOpportunity.status" placeholder="请选择状态">
            <el-option label="进行中" value="open" />
            <el-option label="已成交" value="won" />
            <el-option label="已丢失" value="lost" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveOpportunity">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { customerAPI, opportunityAPI } from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'Opportunities',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const opportunityFormRef = ref(null)
    
    const searchForm = reactive({
      name: '',
      customerId: '',
      status: ''
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    const currentOpportunity = reactive({
      id: null,
      name: '',
      customerId: null,
      description: '',
      estimatedAmount: 0,
      probability: 50,
      status: 'open'
    })
    
    const opportunityRules = {
      name: [
        { required: true, message: '请输入商机名称', trigger: 'blur' }
      ],
      customerId: [
        { required: true, message: '请选择客户', trigger: 'change' }
      ],
      estimatedAmount: [
        { required: true, message: '请输入预估金额', trigger: 'blur' }
      ]
    }
    
    const opportunities = ref([])
    const customers = ref([])
    
    // 获取客户列表
    const fetchCustomers = async () => {
      try {
        const response = await customerAPI.getCustomers()
        if (response.data.status === 'success') {
          customers.value = response.data.customers
        } else {
          ElMessage.error(response.data.message || '获取客户列表失败')
        }
      } catch (error) {
        console.error('Fetch customers error:', error)
        ElMessage.error('获取客户列表失败')
      }
    }
    
    // 获取商机列表
    const fetchOpportunities = async () => {
      try {
        const response = await opportunityAPI.getOpportunities()
        if (response.data.status === 'success') {
          // 将客户名称添加到商机中，并转换字段名
          const opportunitiesData = response.data.opportunities.map(opportunity => {
            const customer = customers.value.find(c => c.id === opportunity.customer_id)
            return {
              id: opportunity.id,
              name: opportunity.name,
              customerId: opportunity.customer_id,
              customerName: customer ? customer.name : '未知客户',
              description: opportunity.description,
              estimatedAmount: opportunity.estimated_amount,
              probability: opportunity.probability,
              status: opportunity.status
            }
          })
          opportunities.value = opportunitiesData
          pagination.total = opportunitiesData.length
        } else {
          ElMessage.error(response.data.message || '获取商机失败')
        }
      } catch (error) {
        console.error('Fetch opportunities error:', error)
        ElMessage.error('获取商机失败')
      }
    }
    
    // 页面加载时获取数据
    onMounted(() => {
      fetchCustomers()
      fetchOpportunities()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增商机'
      Object.assign(currentOpportunity, {
        id: null,
        name: '',
        customerId: null,
        description: '',
        estimatedAmount: 0,
        probability: 50,
        status: 'open'
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑商机'
      Object.assign(currentOpportunity, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除该商机, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // 调用后端API删除商机
          const response = await opportunityAPI.deleteOpportunity(row.id)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            // 重新获取数据以更新列表
            await fetchOpportunities()
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete opportunity error:', error)
          ElMessage.error('删除失败')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
    
    const handleSearch = () => {
      // 执行搜索
      ElMessage({
        message: '执行搜索操作',
        type: 'info'
      })
    }
    
    const handleRefresh = async () => {
      // 刷新数据
      await fetchCustomers()
      await fetchOpportunities()
      ElMessage.success('数据刷新成功')
    }
    
    const saveOpportunity = async () => {
      opportunityFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            let response
            if (currentOpportunity.id) {
              // 更新商机
              const opportunityData = {
                customer_id: currentOpportunity.customerId,
                name: currentOpportunity.name,
                description: currentOpportunity.description,
                estimated_amount: currentOpportunity.estimatedAmount,
                probability: currentOpportunity.probability,
                status: currentOpportunity.status
              }
              
              response = await opportunityAPI.updateOpportunity(currentOpportunity.id, opportunityData)
            } else {
              // 创建新的商机
              const opportunityData = {
                customer_id: currentOpportunity.customerId,
                name: currentOpportunity.name,
                description: currentOpportunity.description,
                estimated_amount: currentOpportunity.estimatedAmount,
                probability: currentOpportunity.probability,
                status: currentOpportunity.status
              }
              
              response = await opportunityAPI.createOpportunity(opportunityData)
            }
            
            if (response && response.data.status === 'success') {
              ElMessage.success(currentOpportunity.id ? '商机更新成功' : '商机创建成功')
              dialogVisible.value = false
              // 重新获取数据以更新列表
              await fetchOpportunities()
            } else {
              ElMessage.error(response.data.message || (currentOpportunity.id ? '商机更新失败' : '商机创建失败'))
            }
          } catch (error) {
            console.error('Save opportunity error:', error)
            ElMessage.error(currentOpportunity.id ? '商机更新失败' : '商机创建失败')
          }
        } else {
          return false
        }
      })
    }
    
    const handleSizeChange = (val) => {
      pagination.pageSize = val
      // 重新加载数据
    }
    
    const handleCurrentChange = (val) => {
      pagination.currentPage = val
      // 重新加载数据
    }
    
    const getStatusType = (status) => {
      const statusMap = {
        'open': 'warning',
        'won': 'success',
        'lost': 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'open': '进行中',
        'won': '已成交',
        'lost': '已丢失'
      }
      return statusMap[status] || '未知状态'
    }
    
    return {
      dialogVisible,
      dialogTitle,
      opportunityFormRef,
      searchForm,
      pagination,
      currentOpportunity,
      opportunityRules,
      opportunities,
      customers,
      handleCreate,
      handleEdit,
      handleDelete,
      handleSearch,
      handleRefresh,
      saveOpportunity,
      handleSizeChange,
      handleCurrentChange,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.opportunities-card {
  border-radius: 8px;
  border: none;
}

.header-actions {
  float: right;
}

.search-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
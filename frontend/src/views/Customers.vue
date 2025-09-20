<template>
  <div class="customers">
    <el-card class="customers-card">
      <template #header>
        <div class="clearfix">
          <span>客户管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="handleCreate">新增客户</el-button>
            <el-button @click="handleRefresh">刷新</el-button>
          </div>
        </div>
      </template>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="客户名称">
          <el-input v-model="searchForm.name" placeholder="客户名称" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="潜在客户" value="potential" />
            <el-option label="意向客户" value="intention" />
            <el-option label="成交客户" value="converted" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 客户列表 -->
      <el-table :data="customers" style="width: 100%" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="客户名称" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column prop="company" label="公司" />
        <el-table-column prop="source" label="来源" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="small" @click="handleViewDetails(scope.row)">详情</el-button>
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
    
    <!-- 客户编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form :model="currentCustomer" :rules="customerRules" ref="customerFormRef" label-width="100px">
        <el-form-item label="客户名称" prop="name">
          <el-input v-model="currentCustomer.name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="currentCustomer.email" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="currentCustomer.phone" />
        </el-form-item>
        <el-form-item label="公司" prop="company">
          <el-input v-model="currentCustomer.company" />
        </el-form-item>
        <el-form-item label="来源" prop="source">
          <el-select v-model="currentCustomer.source" placeholder="请选择来源">
            <el-option label="网站咨询" value="website" />
            <el-option label="线下推广" value="offline" />
            <el-option label="转介绍" value="referral" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentCustomer.status" placeholder="请选择状态">
            <el-option label="潜在客户" value="potential" />
            <el-option label="意向客户" value="intention" />
            <el-option label="成交客户" value="converted" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveCustomer" :loading="saveLoading">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 客户详情对话框 -->
    <el-dialog title="客户详情" v-model="detailDialogVisible" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ detailCustomer.id }}</el-descriptions-item>
        <el-descriptions-item label="客户名称">{{ detailCustomer.name }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ detailCustomer.email }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ detailCustomer.phone }}</el-descriptions-item>
        <el-descriptions-item label="公司">{{ detailCustomer.company }}</el-descriptions-item>
        <el-descriptions-item label="来源">{{ getSourceText(detailCustomer.source) }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(detailCustomer.status)">
            {{ getStatusText(detailCustomer.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ detailCustomer.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ detailCustomer.updated_at }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { customerAPI } from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'Customers',
  setup() {
    const dialogVisible = ref(false)
    const detailDialogVisible = ref(false)
    const dialogTitle = ref('')
    const customerFormRef = ref(null)
    const loading = ref(false)
    const saveLoading = ref(false)
    
    const searchForm = reactive({
      name: '',
      status: ''
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    const currentCustomer = reactive({
      id: null,
      name: '',
      email: '',
      phone: '',
      company: '',
      source: '',
      status: 'potential'
    })
    
    const detailCustomer = reactive({
      id: null,
      name: '',
      email: '',
      phone: '',
      company: '',
      source: '',
      status: 'potential',
      created_at: '',
      updated_at: ''
    })
    
    const customerRules = {
      name: [
        { required: true, message: '请输入客户名称', trigger: 'blur' }
      ],
      email: [
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ]
    }
    
    const customers = ref([])
    
    // 获取客户列表
    const fetchCustomers = async () => {
      loading.value = true
      try {
        const response = await customerAPI.getCustomers()
        if (response.data.status === 'success') {
          customers.value = response.data.customers
          pagination.total = response.data.customers.length
        } else {
          ElMessage.error(response.data.message || '获取客户列表失败')
        }
      } catch (error) {
        console.error('Fetch customers error:', error)
        ElMessage.error('获取客户列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 页面加载时获取客户列表
    onMounted(() => {
      fetchCustomers()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增客户'
      Object.assign(currentCustomer, {
        id: null,
        name: '',
        email: '',
        phone: '',
        company: '',
        source: '',
        status: 'potential'
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑客户'
      Object.assign(currentCustomer, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除客户 "${row.name}", 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          const response = await customerAPI.deleteCustomer(row.id)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            fetchCustomers() // 刷新列表
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete customer error:', error)
          ElMessage.error('删除失败')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
    
    const handleViewDetails = (row) => {
      // 查看客户详情
      Object.assign(detailCustomer, row)
      detailDialogVisible.value = true
    }
    
    const handleSearch = () => {
      // 执行搜索
      ElMessage.info('执行搜索操作')
    }
    
    const handleRefresh = () => {
      fetchCustomers()
    }
    
    const saveCustomer = () => {
      customerFormRef.value.validate(async (valid) => {
        if (valid) {
          saveLoading.value = true
          try {
            let response
            if (currentCustomer.id) {
              // 更新客户
              response = await customerAPI.updateCustomer(currentCustomer.id, currentCustomer)
            } else {
              // 创建客户
              response = await customerAPI.createCustomer(currentCustomer)
            }
            
            if (response.data.status === 'success') {
              ElMessage.success(currentCustomer.id ? '客户更新成功' : '客户创建成功')
              dialogVisible.value = false
              fetchCustomers() // 刷新列表
            } else {
              ElMessage.error(response.data.message || (currentCustomer.id ? '客户更新失败' : '客户创建失败'))
            }
          } catch (error) {
            console.error('Save customer error:', error)
            ElMessage.error(currentCustomer.id ? '客户更新失败' : '客户创建失败')
          } finally {
            saveLoading.value = false
          }
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
        'potential': 'info',
        'intention': 'warning',
        'converted': 'success'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'potential': '潜在客户',
        'intention': '意向客户',
        'converted': '成交客户'
      }
      return statusMap[status] || '未知状态'
    }
    
    const getSourceText = (source) => {
      const sourceMap = {
        'website': '网站咨询',
        'offline': '线下推广',
        'referral': '转介绍',
        'other': '其他'
      }
      return sourceMap[source] || '未知来源'
    }
    
    return {
      dialogVisible,
      detailDialogVisible,
      dialogTitle,
      customerFormRef,
      searchForm,
      pagination,
      currentCustomer,
      detailCustomer,
      customerRules,
      customers,
      loading,
      saveLoading,
      handleCreate,
      handleEdit,
      handleDelete,
      handleViewDetails,
      handleSearch,
      handleRefresh,
      saveCustomer,
      handleSizeChange,
      handleCurrentChange,
      getStatusType,
      getStatusText,
      getSourceText
    }
  }
}
</script>

<style scoped>
.customers-card {
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
<template>
  <div class="followups">
    <el-card class="followups-card">
      <div slot="header" class="clearfix">
        <span>销售跟进</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增跟进</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="客户名称">
          <el-input v-model="searchForm.customerName" placeholder="客户名称" clearable />
        </el-form-item>
        <el-form-item label="跟进方式">
          <el-select v-model="searchForm.followupType" placeholder="请选择跟进方式" clearable>
            <el-option label="电话" value="call" />
            <el-option label="邮件" value="email" />
            <el-option label="面谈" value="meeting" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待跟进" value="pending" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 跟进列表 -->
      <el-table :data="followups" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="customerName" label="客户名称" />
        <el-table-column prop="content" label="跟进内容" />
        <el-table-column prop="followupType" label="跟进方式" width="100">
          <template #default="scope">
            {{ getFollowupTypeText(scope.row.followupType) }}
          </template>
        </el-table-column>
        <el-table-column prop="followupTime" label="跟进时间" width="120" />
        <el-table-column prop="nextFollowupDate" label="下次跟进" width="120" />
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
    
    <!-- 跟进编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="currentFollowup" :rules="followupRules" ref="followupFormRef" label-width="120px">
        <el-form-item label="客户" prop="customerId">
          <el-select v-model="currentFollowup.customerId" placeholder="请选择客户" style="width: 100%;">
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="跟进内容" prop="content">
          <el-input type="textarea" v-model="currentFollowup.content" :rows="4" />
        </el-form-item>
        <el-form-item label="跟进方式" prop="followupType">
          <el-select v-model="currentFollowup.followupType" placeholder="请选择跟进方式">
            <el-option label="电话" value="call" />
            <el-option label="邮件" value="email" />
            <el-option label="面谈" value="meeting" />
          </el-select>
        </el-form-item>
        <el-form-item label="跟进时间" prop="followupTime">
          <el-date-picker
            v-model="currentFollowup.followupTime"
            type="datetime"
            placeholder="选择跟进时间"
            style="width: 100%;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="下次跟进时间" prop="nextFollowupDate">
          <el-date-picker
            v-model="currentFollowup.nextFollowupDate"
            type="datetime"
            placeholder="选择下次跟进时间"
            style="width: 100%;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentFollowup.status" placeholder="请选择状态">
            <el-option label="待跟进" value="pending" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveFollowup">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { customerAPI, followupAPI } from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'FollowUps',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const followupFormRef = ref(null)
    
    const searchForm = reactive({
      customerName: '',
      followupType: '',
      status: ''
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    const currentFollowup = reactive({
      id: null,
      customerId: null,
      content: '',
      followupType: '',
      followupTime: '',
      nextFollowupDate: '',
      status: 'pending'
    })
    
    const followupRules = {
      customerId: [
        { required: true, message: '请选择客户', trigger: 'change' }
      ],
      content: [
        { required: true, message: '请输入跟进内容', trigger: 'blur' }
      ],
      followupType: [
        { required: true, message: '请选择跟进方式', trigger: 'change' }
      ]
    }
    
    const followups = ref([])
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
    
    // 获取跟进记录列表
    const fetchFollowups = async () => {
      try {
        const response = await followupAPI.getFollowups()
        if (response.data.status === 'success') {
          // 将客户名称添加到跟进记录中
          const followupsData = response.data.followups.map(followup => {
            const customer = customers.value.find(c => c.id === followup.customer_id)
            return {
              ...followup,
              customerName: customer ? customer.name : '未知客户'
            }
          })
          followups.value = followupsData
          pagination.total = followupsData.length
        } else {
          ElMessage.error(response.data.message || '获取跟进记录失败')
        }
      } catch (error) {
        console.error('Fetch followups error:', error)
        ElMessage.error('获取跟进记录失败')
      }
    }
    
    // 页面加载时获取数据
    onMounted(() => {
      fetchCustomers()
      fetchFollowups()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增跟进'
      Object.assign(currentFollowup, {
        id: null,
        customerId: null,
        content: '',
        followupType: '',
        followupTime: '',
        nextFollowupDate: '',
        status: 'pending'
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑跟进'
      Object.assign(currentFollowup, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除该跟进记录, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // 调用后端API删除跟进记录
          const response = await followupAPI.deleteFollowup(row.id)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            // 重新获取数据以更新列表
            await fetchFollowups()
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete followup error:', error)
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
      await fetchFollowups()
      ElMessage.success('数据刷新成功')
    }
    
    const saveFollowup = async () => {
      followupFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            let response
            if (currentFollowup.id) {
              // 更新跟进记录
              const followupData = {
                customer_id: currentFollowup.customerId,
                user_id: 1, // 这里应该从当前登录用户获取
                content: currentFollowup.content,
                followup_type: currentFollowup.followupType,
                followup_time: currentFollowup.followupTime,
                next_followup_date: currentFollowup.nextFollowupDate,
                status: currentFollowup.status
              }
              
              response = await followupAPI.updateFollowup(currentFollowup.id, followupData)
            } else {
              // 创建新的跟进记录
              const followupData = {
                customer_id: currentFollowup.customerId,
                user_id: 1, // 这里应该从当前登录用户获取
                content: currentFollowup.content,
                followup_type: currentFollowup.followupType,
                followup_time: currentFollowup.followupTime,
                next_followup_date: currentFollowup.nextFollowupDate,
                status: currentFollowup.status
              }
              
              response = await followupAPI.createFollowup(followupData)
            }
            
            if (response && response.data.status === 'success') {
              ElMessage.success(currentFollowup.id ? '跟进记录更新成功' : '跟进记录创建成功')
              dialogVisible.value = false
              // 重新获取数据以更新列表
              await fetchFollowups()
            } else {
              ElMessage.error(response.data.message || (currentFollowup.id ? '跟进记录更新失败' : '跟进记录创建失败'))
            }
          } catch (error) {
            console.error('Save followup error:', error)
            ElMessage.error(currentFollowup.id ? '跟进记录更新失败' : '跟进记录创建失败')
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
    
    const getFollowupTypeText = (type) => {
      const typeMap = {
        'call': '电话',
        'email': '邮件',
        'meeting': '面谈'
      }
      return typeMap[type] || '未知'
    }
    
    const getStatusType = (status) => {
      const statusMap = {
        'pending': 'warning',
        'completed': 'success'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待跟进',
        'completed': '已完成'
      }
      return statusMap[status] || '未知状态'
    }
    
    return {
      dialogVisible,
      dialogTitle,
      followupFormRef,
      searchForm,
      pagination,
      currentFollowup,
      followupRules,
      followups,
      customers,
      handleCreate,
      handleEdit,
      handleDelete,
      handleSearch,
      handleRefresh,
      saveFollowup,
      handleSizeChange,
      handleCurrentChange,
      getFollowupTypeText,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.followups-card {
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
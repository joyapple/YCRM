<template>
  <div class="departments">
    <el-card class="departments-card">
      <div slot="header" class="clearfix">
        <span>部门管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增部门</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 部门列表 -->
      <el-table :data="departments" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="部门名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 部门编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form :model="currentDepartment" :rules="departmentRules" ref="departmentFormRef" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <el-input v-model="currentDepartment.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="currentDepartment.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveDepartment">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../services/api'

export default {
  name: 'Departments',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const departmentFormRef = ref(null)
    
    const currentDepartment = reactive({
      id: null,
      name: '',
      description: ''
    })
    
    const departmentRules = {
      name: [
        { required: true, message: '请输入部门名称', trigger: 'blur' }
      ]
    }
    
    const departments = ref([])
    
    // 获取部门列表
    const fetchDepartments = async () => {
      try {
        const response = await api.get('/departments')
        if (response.data.status === 'success') {
          departments.value = response.data.departments
        } else {
          ElMessage.error(response.data.message || '获取部门列表失败')
        }
      } catch (error) {
        console.error('Fetch departments error:', error)
        ElMessage.error('获取部门列表失败')
      }
    }
    
    // 页面加载时获取数据
    onMounted(() => {
      fetchDepartments()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增部门'
      Object.assign(currentDepartment, {
        id: null,
        name: '',
        description: ''
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑部门'
      Object.assign(currentDepartment, {
        id: row.id,
        name: row.name,
        description: row.description
      })
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除该部门, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // 调用后端API删除部门
          const response = await api.delete(`/departments/${row.id}`)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            // 重新获取数据以更新列表
            await fetchDepartments()
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete department error:', error)
          ElMessage.error('删除失败')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
    
    const handleRefresh = async () => {
      // 刷新数据
      await fetchDepartments()
      ElMessage.success('数据刷新成功')
    }
    
    const saveDepartment = async () => {
      departmentFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            let response
            if (currentDepartment.id) {
              // 更新部门
              const departmentData = {
                name: currentDepartment.name,
                description: currentDepartment.description
              }
              
              response = await api.put(`/departments/${currentDepartment.id}`, departmentData)
            } else {
              // 创建新部门
              const departmentData = {
                name: currentDepartment.name,
                description: currentDepartment.description
              }
              
              response = await api.post('/departments', departmentData)
            }
            
            if (response && response.data.status === 'success') {
              ElMessage.success(currentDepartment.id ? '部门更新成功' : '部门创建成功')
              dialogVisible.value = false
              // 重新获取数据以更新列表
              await fetchDepartments()
            } else {
              ElMessage.error(response.data.message || (currentDepartment.id ? '部门更新失败' : '部门创建失败'))
            }
          } catch (error) {
            console.error('Save department error:', error)
            ElMessage.error(currentDepartment.id ? '部门更新失败' : '部门创建失败')
          }
        } else {
          return false
        }
      })
    }
    
    return {
      dialogVisible,
      dialogTitle,
      departmentFormRef,
      currentDepartment,
      departmentRules,
      departments,
      handleCreate,
      handleEdit,
      handleDelete,
      handleRefresh,
      saveDepartment
    }
  }
}
</script>

<style scoped>
.departments-card {
  border-radius: 8px;
  border: none;
}

.header-actions {
  float: right;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
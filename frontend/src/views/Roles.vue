<template>
  <div class="roles">
    <el-card class="roles-card">
      <div slot="header" class="clearfix">
        <span>角色管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增角色</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 角色列表 -->
      <el-table :data="roles" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="permissions" label="权限" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 角色编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="currentRole" :rules="roleRules" ref="roleFormRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="currentRole.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="currentRole.description" type="textarea" />
        </el-form-item>
        <el-form-item label="权限" prop="permissions">
          <el-select 
            v-model="currentRole.permissions" 
            multiple 
            placeholder="请选择权限" 
            style="width: 100%;">
            <el-option label="查看客户" value="view_customer" />
            <el-option label="创建客户" value="create_customer" />
            <el-option label="编辑客户" value="edit_customer" />
            <el-option label="删除客户" value="delete_customer" />
            <el-option label="查看销售跟进" value="view_followup" />
            <el-option label="创建销售跟进" value="create_followup" />
            <el-option label="编辑销售跟进" value="edit_followup" />
            <el-option label="删除销售跟进" value="delete_followup" />
            <el-option label="查看商机" value="view_opportunity" />
            <el-option label="创建商机" value="create_opportunity" />
            <el-option label="编辑商机" value="edit_opportunity" />
            <el-option label="删除商机" value="delete_opportunity" />
            <el-option label="查看订单" value="view_order" />
            <el-option label="创建订单" value="create_order" />
            <el-option label="编辑订单" value="edit_order" />
            <el-option label="删除订单" value="delete_order" />
            <el-option label="查看任务" value="view_task" />
            <el-option label="创建任务" value="create_task" />
            <el-option label="编辑任务" value="edit_task" />
            <el-option label="删除任务" value="delete_task" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveRole">确 定</el-button>
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
  name: 'Roles',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const roleFormRef = ref(null)
    
    const currentRole = reactive({
      id: null,
      name: '',
      description: '',
      permissions: []
    })
    
    const roleRules = {
      name: [
        { required: true, message: '请输入角色名称', trigger: 'blur' }
      ]
    }
    
    const roles = ref([])
    
    // 获取角色列表
    const fetchRoles = async () => {
      try {
        const response = await api.get('/roles')
        if (response.data.status === 'success') {
          // 将权限字符串转换为数组
          const rolesData = response.data.roles.map(role => {
            return {
              ...role,
              permissions: role.permissions ? JSON.parse(role.permissions) : []
            }
          })
          roles.value = rolesData
        } else {
          ElMessage.error(response.data.message || '获取角色列表失败')
        }
      } catch (error) {
        console.error('Fetch roles error:', error)
        ElMessage.error('获取角色列表失败')
      }
    }
    
    // 页面加载时获取数据
    onMounted(() => {
      fetchRoles()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增角色'
      Object.assign(currentRole, {
        id: null,
        name: '',
        description: '',
        permissions: []
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑角色'
      Object.assign(currentRole, {
        id: row.id,
        name: row.name,
        description: row.description,
        permissions: Array.isArray(row.permissions) ? row.permissions : []
      })
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除该角色, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // 调用后端API删除角色
          const response = await api.delete(`/roles/${row.id}`)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            // 重新获取数据以更新列表
            await fetchRoles()
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete role error:', error)
          ElMessage.error('删除失败')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
    
    const handleRefresh = async () => {
      // 刷新数据
      await fetchRoles()
      ElMessage.success('数据刷新成功')
    }
    
    const saveRole = async () => {
      roleFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            let response
            if (currentRole.id) {
              // 更新角色
              const roleData = {
                name: currentRole.name,
                description: currentRole.description,
                permissions: JSON.stringify(currentRole.permissions)
              }
              
              response = await api.put(`/roles/${currentRole.id}`, roleData)
            } else {
              // 创建新角色
              const roleData = {
                name: currentRole.name,
                description: currentRole.description,
                permissions: JSON.stringify(currentRole.permissions)
              }
              
              response = await api.post('/roles', roleData)
            }
            
            if (response && response.data.status === 'success') {
              ElMessage.success(currentRole.id ? '角色更新成功' : '角色创建成功')
              dialogVisible.value = false
              // 重新获取数据以更新列表
              await fetchRoles()
            } else {
              ElMessage.error(response.data.message || (currentRole.id ? '角色更新失败' : '角色创建失败'))
            }
          } catch (error) {
            console.error('Save role error:', error)
            ElMessage.error(currentRole.id ? '角色更新失败' : '角色创建失败')
          }
        } else {
          return false
        }
      })
    }
    
    return {
      dialogVisible,
      dialogTitle,
      roleFormRef,
      currentRole,
      roleRules,
      roles,
      handleCreate,
      handleEdit,
      handleDelete,
      handleRefresh,
      saveRole
    }
  }
}
</script>

<style scoped>
.roles-card {
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
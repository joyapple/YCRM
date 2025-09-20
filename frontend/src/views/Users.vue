<template>
  <div class="users">
    <el-card class="users-card">
      <div slot="header" class="clearfix">
        <span>用户管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增用户</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 用户列表 -->
      <el-table :data="users" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="departmentName" label="部门" width="120" />
        <el-table-column prop="roleName" label="角色" width="120">
          <template #default="scope">
            <el-tag :type="getRoleType(scope.row.role)">
              {{ scope.row.roleName }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="dataScopeText" label="数据权限" width="120" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)" :disabled="scope.row.role === 'admin' && adminsCount <= 1">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 用户编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form :model="currentUser" :rules="userRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="currentUser.username" :disabled="!!currentUser.id" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="currentUser.email" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!currentUser.id">
          <el-input v-model="currentUser.password" type="password" />
        </el-form-item>
        <el-form-item label="部门" prop="department_id">
          <el-select v-model="currentUser.department_id" placeholder="请选择部门" style="width: 100%;">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="角色" prop="role_id">
          <el-select v-model="currentUser.role_id" placeholder="请选择角色" style="width: 100%;">
            <el-option
              v-for="role in roles"
              :key="role.id"
              :label="role.name"
              :value="role.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据权限" prop="data_scope">
          <el-select v-model="currentUser.data_scope" placeholder="请选择数据权限范围" style="width: 100%;">
            <el-option label="仅自己" value="own" />
            <el-option label="本部门" value="department" />
            <el-option label="全部" value="all" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveUser">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { userAPI, departmentAPI, roleAPI } from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'Users',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const userFormRef = ref(null)
    
    const currentUser = reactive({
      id: null,
      username: '',
      email: '',
      password: '',
      department_id: null,
      role_id: null,
      data_scope: 'own'
    })
    
    const userRules = {
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
      department_id: [
        { required: true, message: '请选择部门', trigger: 'change' }
      ],
      role_id: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ],
      data_scope: [
        { required: true, message: '请选择数据权限范围', trigger: 'change' }
      ]
    }
    
    const users = ref([])
    const departments = ref([])
    const roles = ref([])
    
    // 获取管理员数量
    const adminsCount = computed(() => {
      return users.value.filter(user => user.role === 'admin').length
    })
    
    // 获取用户列表
    const fetchUsers = async () => {
      try {
        const response = await userAPI.getUsers()
        if (response.data.status === 'success') {
          // 将部门和角色名称添加到用户数据中
          const usersData = response.data.users.map(user => {
            return {
              ...user,
              departmentName: user.department_name || '未分配',
              roleName: user.role_name || '未分配',
              dataScopeText: getDataScopeText(user.data_scope)
            }
          })
          users.value = usersData
        } else {
          ElMessage.error(response.data.message || '获取用户列表失败')
        }
      } catch (error) {
        console.error('Fetch users error:', error)
        ElMessage.error('获取用户列表失败')
      }
    }
    
    // 获取部门列表
    const fetchDepartments = async () => {
      try {
        const response = await departmentAPI.getDepartments()
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
    
    // 获取角色列表
    const fetchRoles = async () => {
      try {
        const response = await roleAPI.getRoles()
        if (response.data.status === 'success') {
          roles.value = response.data.roles
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
      fetchDepartments()
      fetchRoles()
      fetchUsers()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增用户'
      Object.assign(currentUser, {
        id: null,
        username: '',
        email: '',
        password: '',
        department_id: null,
        role_id: null,
        data_scope: 'own'
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑用户'
      Object.assign(currentUser, {
        id: row.id,
        username: row.username,
        email: row.email,
        password: '', // 编辑时不显示密码
        department_id: row.department_id,
        role_id: row.role_id,
        data_scope: row.data_scope
      })
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      // 检查是否是最后一个管理员
      if (row.role === 'admin' && adminsCount.value <= 1) {
        ElMessage.warning('系统至少需要保留一个管理员')
        return
      }
      
      ElMessageBox.confirm(
        `此操作将永久删除该用户, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // 调用后端API删除用户
          const response = await userAPI.deleteUser(row.id)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            // 重新获取数据以更新列表
            await fetchUsers()
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete user error:', error)
          ElMessage.error('删除失败')
        }
      }).catch(() => {
        ElMessage.info('已取消删除')
      })
    }
    
    const handleRefresh = async () => {
      // 刷新数据
      await fetchDepartments()
      await fetchRoles()
      await fetchUsers()
      ElMessage.success('数据刷新成功')
    }
    
    const saveUser = async () => {
      userFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            let response
            if (currentUser.id) {
              // 更新用户（密码字段为空时不更新密码）
              const userData = {
                username: currentUser.username,
                email: currentUser.email,
                department_id: currentUser.department_id,
                role_id: currentUser.role_id,
                data_scope: currentUser.data_scope
              }
              
              // 如果密码不为空，则更新密码
              if (currentUser.password) {
                userData.password = currentUser.password
              }
              
              response = await userAPI.updateUser(currentUser.id, userData)
            } else {
              // 创建新用户
              const userData = {
                username: currentUser.username,
                email: currentUser.email,
                password: currentUser.password,
                department_id: currentUser.department_id,
                role_id: currentUser.role_id,
                data_scope: currentUser.data_scope
              }
              
              response = await userAPI.createUser(userData)
            }
            
            if (response && response.data.status === 'success') {
              ElMessage.success(currentUser.id ? '用户更新成功' : '用户创建成功')
              dialogVisible.value = false
              // 重新获取数据以更新列表
              await fetchUsers()
            } else {
              ElMessage.error(response.data.message || (currentUser.id ? '用户更新失败' : '用户创建失败'))
            }
          } catch (error) {
            console.error('Save user error:', error)
            ElMessage.error(currentUser.id ? '用户更新失败' : '用户创建失败')
          }
        } else {
          return false
        }
      })
    }
    
    const getRoleType = (role) => {
      const roleMap = {
        'admin': 'danger',
        'employee': 'primary'
      }
      return roleMap[role] || 'info'
    }
    
    const getDataScopeText = (scope) => {
      const scopeMap = {
        'own': '仅自己',
        'department': '本部门',
        'all': '全部'
      }
      return scopeMap[scope] || '未知'
    }
    
    return {
      dialogVisible,
      dialogTitle,
      userFormRef,
      currentUser,
      userRules,
      users,
      departments,
      roles,
      adminsCount,
      handleCreate,
      handleEdit,
      handleDelete,
      handleRefresh,
      saveUser,
      getRoleType,
      getDataScopeText
    }
  }
}
</script>

<style scoped>
.users-card {
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
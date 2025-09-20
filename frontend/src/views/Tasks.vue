<template>
  <div class="tasks">
    <el-card class="tasks-card">
      <div slot="header" class="clearfix">
        <span>任务管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增任务</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="任务标题">
          <el-input v-model="searchForm.title" placeholder="任务标题" clearable />
        </el-form-item>
        <el-form-item label="分配给">
          <el-select v-model="searchForm.assignedTo" placeholder="请选择用户" clearable>
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 任务列表 -->
      <el-table :data="tasks" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="任务标题" />
        <el-table-column prop="assignedToName" label="分配给" />
        <el-table-column prop="dueDate" label="截止日期" width="120" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">
              {{ getPriorityText(scope.row.priority) }}
            </el-tag>
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
    
    <!-- 任务编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="currentTask" :rules="taskRules" ref="taskFormRef" label-width="120px">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="currentTask.title" />
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input type="textarea" v-model="currentTask.description" :rows="3" />
        </el-form-item>
        <el-form-item label="分配给" prop="assignedTo">
          <el-select v-model="currentTask.assignedTo" placeholder="请选择用户" style="width: 100%;">
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="截止日期" prop="dueDate">
          <el-date-picker
            v-model="currentTask.dueDate"
            type="date"
            placeholder="选择截止日期"
            style="width: 100%;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="currentTask.priority" placeholder="请选择优先级">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentTask.status" placeholder="请选择状态">
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveTask">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'

export default {
  name: 'Tasks',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const taskFormRef = ref(null)
    
    const searchForm = reactive({
      title: '',
      assignedTo: '',
      status: ''
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    const currentTask = reactive({
      id: null,
      title: '',
      description: '',
      assignedTo: null,
      dueDate: '',
      priority: 'medium',
      status: 'pending'
    })
    
    const taskRules = {
      title: [
        { required: true, message: '请输入任务标题', trigger: 'blur' }
      ],
      assignedTo: [
        { required: true, message: '请选择分配用户', trigger: 'change' }
      ],
      dueDate: [
        { required: true, message: '请选择截止日期', trigger: 'change' }
      ]
    }
    
    const tasks = ref([
      {
        id: 1,
        title: '联系ABC公司',
        description: '电话联系ABC公司确认项目需求',
        assignedTo: 1,
        assignedToName: '张三',
        dueDate: '2023-05-25',
        priority: 'high',
        status: 'in_progress'
      },
      {
        id: 2,
        title: '准备产品演示',
        description: '为XYZ集团准备产品演示材料',
        assignedTo: 2,
        assignedToName: '李四',
        dueDate: '2023-05-30',
        priority: 'medium',
        status: 'pending'
      }
    ])
    
    const users = ref([
      { id: 1, username: '张三' },
      { id: 2, username: '李四' }
    ])
    
    const handleCreate = () => {
      dialogTitle.value = '新增任务'
      Object.assign(currentTask, {
        id: null,
        title: '',
        description: '',
        assignedTo: null,
        dueDate: '',
        priority: 'medium',
        status: 'pending'
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑任务'
      Object.assign(currentTask, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除该任务, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        // 这里应该调用后端API删除任务
        ElMessage({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        ElMessage({
          type: 'info',
          message: '已取消删除'
        })
      })
    }
    
    const handleSearch = () => {
      // 执行搜索
      ElMessage({
        message: '执行搜索操作',
        type: 'info'
      })
    }
    
    const handleRefresh = () => {
      // 刷新数据
      ElMessage({
        message: '刷新任务数据',
        type: 'info'
      })
    }
    
    const saveTask = () => {
      taskFormRef.value.validate((valid) => {
        if (valid) {
          // 这里应该调用后端API保存任务信息
          ElMessage({
            message: '任务信息保存成功',
            type: 'success'
          })
          dialogVisible.value = false
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
    
    const getPriorityType = (priority) => {
      const priorityMap = {
        'low': 'info',
        'medium': 'warning',
        'high': 'danger'
      }
      return priorityMap[priority] || 'info'
    }
    
    const getPriorityText = (priority) => {
      const priorityMap = {
        'low': '低',
        'medium': '中',
        'high': '高'
      }
      return priorityMap[priority] || '未知'
    }
    
    const getStatusType = (status) => {
      const statusMap = {
        'pending': 'info',
        'in_progress': 'warning',
        'completed': 'success'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待处理',
        'in_progress': '进行中',
        'completed': '已完成'
      }
      return statusMap[status] || '未知状态'
    }
    
    return {
      dialogVisible,
      dialogTitle,
      taskFormRef,
      searchForm,
      pagination,
      currentTask,
      taskRules,
      tasks,
      users,
      handleCreate,
      handleEdit,
      handleDelete,
      handleSearch,
      handleRefresh,
      saveTask,
      handleSizeChange,
      handleCurrentChange,
      getPriorityType,
      getPriorityText,
      getStatusType,
      getStatusText
    }
  }
}
</script>

<style scoped>
.tasks-card {
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
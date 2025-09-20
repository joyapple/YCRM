<template>
  <div class="tasks">
    <el-card>
      <div slot="header">
        <span>任务管理</span>
        <el-button style="float: right; margin-left: 10px;" type="primary" @click="handleCreate">新增任务</el-button>
        <el-button style="float: right;" @click="handleRefresh">刷新</el-button>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="任务标题">
          <el-input v-model="searchForm.title" placeholder="任务标题"></el-input>
        </el-form-item>
        <el-form-item label="分配给">
          <el-select v-model="searchForm.assignedTo" placeholder="请选择用户">
            <el-option label="全部" value=""></el-option>
            <el-option
              v-for="user in users"
              :key="user.id"
              :label="user.username"
              :value="user.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="待处理" value="pending"></el-option>
            <el-option label="进行中" value="in_progress"></el-option>
            <el-option label="已完成" value="completed"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 任务列表 -->
      <el-table :data="tasks" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="title" label="任务标题"></el-table-column>
        <el-table-column prop="assignedToName" label="分配给"></el-table-column>
        <el-table-column prop="dueDate" label="截止日期" width="120"></el-table-column>
        <el-table-column prop="priority" label="优先级" width="100">
          <template slot-scope="scope">
            <el-tag :type="getPriorityType(scope.row.priority)">{{ getPriorityText(scope.row.priority) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </el-card>
    
    <!-- 任务编辑对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="currentTask" :rules="taskRules" ref="taskForm" label-width="120px">
        <el-form-item label="任务标题" prop="title">
          <el-input v-model="currentTask.title"></el-input>
        </el-form-item>
        <el-form-item label="任务描述" prop="description">
          <el-input type="textarea" v-model="currentTask.description" :rows="3"></el-input>
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
            <el-option label="低" value="low"></el-option>
            <el-option label="中" value="medium"></el-option>
            <el-option label="高" value="high"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentTask.status" placeholder="请选择状态">
            <el-option label="待处理" value="pending"></el-option>
            <el-option label="进行中" value="in_progress"></el-option>
            <el-option label="已完成" value="completed"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveTask">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Tasks',
  data() {
    return {
      tasks: [
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
      ],
      users: [
        { id: 1, username: '张三' },
        { id: 2, username: '李四' }
      ],
      searchForm: {
        title: '',
        assignedTo: '',
        status: ''
      },
      dialogVisible: false,
      dialogTitle: '',
      currentTask: {
        id: null,
        title: '',
        description: '',
        assignedTo: null,
        dueDate: '',
        priority: 'medium',
        status: 'pending'
      },
      taskRules: {
        title: [
          { required: true, message: '请输入任务标题', trigger: 'blur' }
        ],
        assignedTo: [
          { required: true, message: '请选择分配用户', trigger: 'change' }
        ],
        dueDate: [
          { required: true, message: '请选择截止日期', trigger: 'change' }
        ]
      },
      currentPage: 1,
      pageSize: 10,
      total: 2
    }
  },
  methods: {
    handleCreate() {
      this.dialogTitle = '新增任务'
      this.currentTask = {
        id: null,
        title: '',
        description: '',
        assignedTo: null,
        dueDate: '',
        priority: 'medium',
        status: 'pending'
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑任务'
      this.currentTask = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除该任务, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用后端API删除任务
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        })
      })
    },
    handleSearch() {
      // 执行搜索
      this.$message({
        message: '执行搜索操作',
        type: 'info'
      })
    },
    handleRefresh() {
      // 刷新数据
      this.$message({
        message: '刷新任务数据',
        type: 'info'
      })
    },
    saveTask() {
      this.$refs.taskForm.validate((valid) => {
        if (valid) {
          // 这里应该调用后端API保存任务信息
          this.$message({
            message: '任务信息保存成功',
            type: 'success'
          })
          this.dialogVisible = false
        } else {
          return false
        }
      })
    },
    handleSizeChange(val) {
      this.pageSize = val
      // 重新加载数据
    },
    handleCurrentChange(val) {
      this.currentPage = val
      // 重新加载数据
    },
    getPriorityType(priority) {
      const priorityMap = {
        'low': 'info',
        'medium': 'warning',
        'high': 'danger'
      }
      return priorityMap[priority] || 'info'
    },
    getPriorityText(priority) {
      const priorityMap = {
        'low': '低',
        'medium': '中',
        'high': '高'
      }
      return priorityMap[priority] || '未知'
    },
    getStatusType(status) {
      const statusMap = {
        'pending': 'info',
        'in_progress': 'warning',
        'completed': 'success'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'pending': '待处理',
        'in_progress': '进行中',
        'completed': '已完成'
      }
      return statusMap[status] || '未知状态'
    }
  }
}
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
}
</style>
<template>
  <div class="followups">
    <el-card>
      <div slot="header">
        <span>销售跟进</span>
        <el-button style="float: right; margin-left: 10px;" type="primary" @click="handleCreate">新增跟进</el-button>
        <el-button style="float: right;" @click="handleRefresh">刷新</el-button>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="客户名称">
          <el-input v-model="searchForm.customerName" placeholder="客户名称"></el-input>
        </el-form-item>
        <el-form-item label="跟进方式">
          <el-select v-model="searchForm.followupType" placeholder="请选择跟进方式">
            <el-option label="全部" value=""></el-option>
            <el-option label="电话" value="call"></el-option>
            <el-option label="邮件" value="email"></el-option>
            <el-option label="面谈" value="meeting"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="待跟进" value="pending"></el-option>
            <el-option label="已完成" value="completed"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 跟进列表 -->
      <el-table :data="followups" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="customerName" label="客户名称"></el-table-column>
        <el-table-column prop="content" label="跟进内容"></el-table-column>
        <el-table-column prop="followupType" label="跟进方式" width="100">
          <template slot-scope="scope">
            {{ getFollowupTypeText(scope.row.followupType) }}
          </template>
        </el-table-column>
        <el-table-column prop="followupTime" label="跟进时间" width="120"></el-table-column>
        <el-table-column prop="nextFollowupDate" label="下次跟进" width="120"></el-table-column>
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
    
    <!-- 跟进编辑对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="currentFollowup" :rules="followupRules" ref="followupForm" label-width="120px">
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
          <el-input type="textarea" v-model="currentFollowup.content" :rows="4"></el-input>
        </el-form-item>
        <el-form-item label="跟进方式" prop="followupType">
          <el-select v-model="currentFollowup.followupType" placeholder="请选择跟进方式">
            <el-option label="电话" value="call"></el-option>
            <el-option label="邮件" value="email"></el-option>
            <el-option label="面谈" value="meeting"></el-option>
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
            <el-option label="待跟进" value="pending"></el-option>
            <el-option label="已完成" value="completed"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveFollowup">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'FollowUps',
  data() {
    return {
      followups: [
        {
          id: 1,
          customerId: 1,
          customerName: '张三',
          content: '电话沟通产品需求',
          followupType: 'call',
          followupTime: '2023-05-20 10:00',
          nextFollowupDate: '2023-05-27 10:00',
          status: 'completed'
        },
        {
          id: 2,
          customerId: 2,
          customerName: '李四',
          content: '发送产品资料邮件',
          followupType: 'email',
          followupTime: '2023-05-19 14:00',
          nextFollowupDate: '2023-05-26 14:00',
          status: 'pending'
        }
      ],
      customers: [
        { id: 1, name: '张三' },
        { id: 2, name: '李四' }
      ],
      searchForm: {
        customerName: '',
        followupType: '',
        status: ''
      },
      dialogVisible: false,
      dialogTitle: '',
      currentFollowup: {
        id: null,
        customerId: null,
        content: '',
        followupType: '',
        followupTime: '',
        nextFollowupDate: '',
        status: 'pending'
      },
      followupRules: {
        customerId: [
          { required: true, message: '请选择客户', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入跟进内容', trigger: 'blur' }
        ],
        followupType: [
          { required: true, message: '请选择跟进方式', trigger: 'change' }
        ]
      },
      currentPage: 1,
      pageSize: 10,
      total: 2
    }
  },
  methods: {
    handleCreate() {
      this.dialogTitle = '新增跟进'
      this.currentFollowup = {
        id: null,
        customerId: null,
        content: '',
        followupType: '',
        followupTime: '',
        nextFollowupDate: '',
        status: 'pending'
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑跟进'
      this.currentFollowup = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除该跟进记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用后端API删除跟进记录
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
        message: '刷新跟进数据',
        type: 'info'
      })
    },
    saveFollowup() {
      this.$refs.followupForm.validate((valid) => {
        if (valid) {
          // 这里应该调用后端API保存跟进信息
          this.$message({
            message: '跟进信息保存成功',
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
    getFollowupTypeText(type) {
      const typeMap = {
        'call': '电话',
        'email': '邮件',
        'meeting': '面谈'
      }
      return typeMap[type] || '未知'
    },
    getStatusType(status) {
      const statusMap = {
        'pending': 'warning',
        'completed': 'success'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'pending': '待跟进',
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
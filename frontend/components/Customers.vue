<template>
  <div class="customers">
    <el-card>
      <div slot="header">
        <span>客户管理</span>
        <el-button style="float: right; margin-left: 10px;" type="primary" @click="handleCreate">新增客户</el-button>
        <el-button style="float: right;" @click="handleRefresh">刷新</el-button>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="客户名称">
          <el-input v-model="searchForm.name" placeholder="客户名称"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="潜在客户" value="potential"></el-option>
            <el-option label="意向客户" value="intention"></el-option>
            <el-option label="成交客户" value="converted"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 客户列表 -->
      <el-table :data="customers" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="客户名称"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="phone" label="电话"></el-table-column>
        <el-table-column prop="company" label="公司"></el-table-column>
        <el-table-column prop="source" label="来源"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            <el-button size="mini" @click="handleViewDetails(scope.row)">详情</el-button>
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
    
    <!-- 客户编辑对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="currentCustomer" :rules="customerRules" ref="customerForm" label-width="100px">
        <el-form-item label="客户名称" prop="name">
          <el-input v-model="currentCustomer.name"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="currentCustomer.email"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="currentCustomer.phone"></el-input>
        </el-form-item>
        <el-form-item label="公司" prop="company">
          <el-input v-model="currentCustomer.company"></el-input>
        </el-form-item>
        <el-form-item label="来源" prop="source">
          <el-select v-model="currentCustomer.source" placeholder="请选择来源">
            <el-option label="网站咨询" value="website"></el-option>
            <el-option label="线下推广" value="offline"></el-option>
            <el-option label="转介绍" value="referral"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentCustomer.status" placeholder="请选择状态">
            <el-option label="潜在客户" value="potential"></el-option>
            <el-option label="意向客户" value="intention"></el-option>
            <el-option label="成交客户" value="converted"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveCustomer">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Customers',
  data() {
    return {
      customers: [
        {
          id: 1,
          name: '张三',
          email: 'zhangsan@example.com',
          phone: '13800138000',
          company: 'ABC公司',
          source: 'website',
          status: 'potential'
        },
        {
          id: 2,
          name: '李四',
          email: 'lisi@example.com',
          phone: '13900139000',
          company: 'XYZ集团',
          source: 'referral',
          status: 'intention'
        }
      ],
      searchForm: {
        name: '',
        status: ''
      },
      dialogVisible: false,
      dialogTitle: '',
      currentCustomer: {
        id: null,
        name: '',
        email: '',
        phone: '',
        company: '',
        source: '',
        status: 'potential'
      },
      customerRules: {
        name: [
          { required: true, message: '请输入客户名称', trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ]
      },
      currentPage: 1,
      pageSize: 10,
      total: 2
    }
  },
  methods: {
    handleCreate() {
      this.dialogTitle = '新增客户'
      this.currentCustomer = {
        id: null,
        name: '',
        email: '',
        phone: '',
        company: '',
        source: '',
        status: 'potential'
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑客户'
      this.currentCustomer = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除该客户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用后端API删除客户
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
    handleViewDetails(row) {
      // 查看客户详情
      this.$message({
        message: `查看客户 ${row.name} 的详情`,
        type: 'info'
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
        message: '刷新客户数据',
        type: 'info'
      })
    },
    saveCustomer() {
      this.$refs.customerForm.validate((valid) => {
        if (valid) {
          // 这里应该调用后端API保存客户信息
          this.$message({
            message: '客户信息保存成功',
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
    getStatusType(status) {
      const statusMap = {
        'potential': 'info',
        'intention': 'warning',
        'converted': 'success'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'potential': '潜在客户',
        'intention': '意向客户',
        'converted': '成交客户'
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
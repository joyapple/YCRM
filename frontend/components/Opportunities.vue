<template>
  <div class="opportunities">
    <el-card>
      <div slot="header">
        <span>商机管理</span>
        <el-button style="float: right; margin-left: 10px;" type="primary" @click="handleCreate">新增商机</el-button>
        <el-button style="float: right;" @click="handleRefresh">刷新</el-button>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="商机名称">
          <el-input v-model="searchForm.name" placeholder="商机名称"></el-input>
        </el-form-item>
        <el-form-item label="客户">
          <el-select v-model="searchForm.customerId" placeholder="请选择客户">
            <el-option label="全部" value=""></el-option>
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="进行中" value="open"></el-option>
            <el-option label="已成交" value="won"></el-option>
            <el-option label="已丢失" value="lost"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 商机列表 -->
      <el-table :data="opportunities" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="商机名称"></el-table-column>
        <el-table-column prop="customerName" label="客户名称"></el-table-column>
        <el-table-column prop="description" label="描述"></el-table-column>
        <el-table-column prop="estimatedAmount" label="预估金额" width="120"></el-table-column>
        <el-table-column prop="probability" label="成交概率" width="100">
          <template slot-scope="scope">
            {{ scope.row.probability }}%
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
    
    <!-- 商机编辑对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="currentOpportunity" :rules="opportunityRules" ref="opportunityForm" label-width="120px">
        <el-form-item label="商机名称" prop="name">
          <el-input v-model="currentOpportunity.name"></el-input>
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
          <el-input type="textarea" v-model="currentOpportunity.description" :rows="3"></el-input>
        </el-form-item>
        <el-form-item label="预估金额" prop="estimatedAmount">
          <el-input-number v-model="currentOpportunity.estimatedAmount" :min="0" style="width: 100%;"></el-input-number>
        </el-form-item>
        <el-form-item label="成交概率(%)" prop="probability">
          <el-slider v-model="currentOpportunity.probability" :min="0" :max="100" show-input></el-slider>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentOpportunity.status" placeholder="请选择状态">
            <el-option label="进行中" value="open"></el-option>
            <el-option label="已成交" value="won"></el-option>
            <el-option label="已丢失" value="lost"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveOpportunity">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Opportunities',
  data() {
    return {
      opportunities: [
        {
          id: 1,
          name: '企业级软件采购',
          customerId: 1,
          customerName: '张三',
          description: 'ABC公司企业级软件采购项目',
          estimatedAmount: 50000,
          probability: 70,
          status: 'open'
        },
        {
          id: 2,
          name: '云服务续约',
          customerId: 2,
          customerName: '李四',
          description: 'XYZ集团云服务续约项目',
          estimatedAmount: 30000,
          probability: 90,
          status: 'open'
        }
      ],
      customers: [
        { id: 1, name: '张三' },
        { id: 2, name: '李四' }
      ],
      searchForm: {
        name: '',
        customerId: '',
        status: ''
      },
      dialogVisible: false,
      dialogTitle: '',
      currentOpportunity: {
        id: null,
        name: '',
        customerId: null,
        description: '',
        estimatedAmount: 0,
        probability: 50,
        status: 'open'
      },
      opportunityRules: {
        name: [
          { required: true, message: '请输入商机名称', trigger: 'blur' }
        ],
        customerId: [
          { required: true, message: '请选择客户', trigger: 'change' }
        ],
        estimatedAmount: [
          { required: true, message: '请输入预估金额', trigger: 'blur' }
        ]
      },
      currentPage: 1,
      pageSize: 10,
      total: 2
    }
  },
  methods: {
    handleCreate() {
      this.dialogTitle = '新增商机'
      this.currentOpportunity = {
        id: null,
        name: '',
        customerId: null,
        description: '',
        estimatedAmount: 0,
        probability: 50,
        status: 'open'
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑商机'
      this.currentOpportunity = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除该商机, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用后端API删除商机
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
        message: '刷新商机数据',
        type: 'info'
      })
    },
    saveOpportunity() {
      this.$refs.opportunityForm.validate((valid) => {
        if (valid) {
          // 这里应该调用后端API保存商机信息
          this.$message({
            message: '商机信息保存成功',
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
        'open': 'warning',
        'won': 'success',
        'lost': 'danger'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'open': '进行中',
        'won': '已成交',
        'lost': '已丢失'
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
<template>
  <div class="orders">
    <el-card>
      <div slot="header">
        <span>订单管理</span>
        <el-button style="float: right; margin-left: 10px;" type="primary" @click="handleCreate">新增订单</el-button>
        <el-button style="float: right;" @click="handleRefresh">刷新</el-button>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderNumber" placeholder="订单号"></el-input>
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
            <el-option label="待付款" value="pending"></el-option>
            <el-option label="已付款" value="paid"></el-option>
            <el-option label="已发货" value="shipped"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 订单列表 -->
      <el-table :data="orders" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="orderNumber" label="订单号"></el-table-column>
        <el-table-column prop="customerName" label="客户名称"></el-table-column>
        <el-table-column prop="amount" label="金额" width="120">
          <template slot-scope="scope">
            ¥{{ scope.row.amount }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentMethod" label="付款方式" width="100"></el-table-column>
        <el-table-column prop="orderDate" label="下单日期" width="120"></el-table-column>
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
    
    <!-- 订单编辑对话框 -->
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="currentOrder" :rules="orderRules" ref="orderForm" label-width="120px">
        <el-form-item label="订单号" prop="orderNumber">
          <el-input v-model="currentOrder.orderNumber" :disabled="!!currentOrder.id"></el-input>
        </el-form-item>
        <el-form-item label="客户" prop="customerId">
          <el-select v-model="currentOrder.customerId" placeholder="请选择客户" style="width: 100%;">
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="currentOrder.amount" :min="0" style="width: 100%;"></el-input-number>
        </el-form-item>
        <el-form-item label="付款方式" prop="paymentMethod">
          <el-select v-model="currentOrder.paymentMethod" placeholder="请选择付款方式">
            <el-option label="银行转账" value="bank_transfer"></el-option>
            <el-option label="支付宝" value="alipay"></el-option>
            <el-option label="微信支付" value="wechat_pay"></el-option>
            <el-option label="现金" value="cash"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentOrder.status" placeholder="请选择状态">
            <el-option label="待付款" value="pending"></el-option>
            <el-option label="已付款" value="paid"></el-option>
            <el-option label="已发货" value="shipped"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="下单日期" prop="orderDate">
          <el-date-picker
            v-model="currentOrder.orderDate"
            type="date"
            placeholder="选择下单日期"
            style="width: 100%;">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveOrder">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Orders',
  data() {
    return {
      orders: [
        {
          id: 1,
          orderNumber: 'ORD20230520001',
          customerId: 1,
          customerName: '张三',
          amount: 25000,
          status: 'paid',
          paymentMethod: '银行转账',
          orderDate: '2023-05-20'
        },
        {
          id: 2,
          orderNumber: 'ORD20230519001',
          customerId: 2,
          customerName: '李四',
          amount: 18000,
          status: 'shipped',
          paymentMethod: '支付宝',
          orderDate: '2023-05-19'
        }
      ],
      customers: [
        { id: 1, name: '张三' },
        { id: 2, name: '李四' }
      ],
      searchForm: {
        orderNumber: '',
        customerId: '',
        status: ''
      },
      dialogVisible: false,
      dialogTitle: '',
      currentOrder: {
        id: null,
        orderNumber: '',
        customerId: null,
        amount: 0,
        status: 'pending',
        paymentMethod: '',
        orderDate: ''
      },
      orderRules: {
        orderNumber: [
          { required: true, message: '请输入订单号', trigger: 'blur' }
        ],
        customerId: [
          { required: true, message: '请选择客户', trigger: 'change' }
        ],
        amount: [
          { required: true, message: '请输入金额', trigger: 'blur' }
        ],
        paymentMethod: [
          { required: true, message: '请选择付款方式', trigger: 'change' }
        ],
        orderDate: [
          { required: true, message: '请选择下单日期', trigger: 'change' }
        ]
      },
      currentPage: 1,
      pageSize: 10,
      total: 2
    }
  },
  methods: {
    handleCreate() {
      this.dialogTitle = '新增订单'
      this.currentOrder = {
        id: null,
        orderNumber: `ORD${new Date().getFullYear()}${(new Date().getMonth() + 1).toString().padStart(2, '0')}${new Date().getDate().toString().padStart(2, '0')}${Math.floor(Math.random() * 1000).toString().padStart(3, '0')}`,
        customerId: null,
        amount: 0,
        status: 'pending',
        paymentMethod: '',
        orderDate: new Date()
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑订单'
      this.currentOrder = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除该订单, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 这里应该调用后端API删除订单
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
        message: '刷新订单数据',
        type: 'info'
      })
    },
    saveOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          // 这里应该调用后端API保存订单信息
          this.$message({
            message: '订单信息保存成功',
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
        'pending': 'warning',
        'paid': 'primary',
        'shipped': 'info',
        'completed': 'success',
        'cancelled': 'danger'
      }
      return statusMap[status] || 'info'
    },
    getStatusText(status) {
      const statusMap = {
        'pending': '待付款',
        'paid': '已付款',
        'shipped': '已发货',
        'completed': '已完成',
        'cancelled': '已取消'
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
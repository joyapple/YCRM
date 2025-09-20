<template>
  <div class="orders">
    <el-card class="orders-card">
      <div slot="header" class="clearfix">
        <span>订单管理</span>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">新增订单</el-button>
          <el-button @click="handleRefresh">刷新</el-button>
        </div>
      </div>
      
      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderNumber" placeholder="订单号" clearable />
        </el-form-item>
        <el-form-item label="客户">
          <el-select v-model="searchForm.customerId" placeholder="请选择客户" clearable>
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待付款" value="pending" />
            <el-option label="已付款" value="paid" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 订单列表 -->
      <el-table :data="orders" style="width: 100%" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="orderNumber" label="订单号" />
        <el-table-column prop="customerName" label="客户名称" />
        <el-table-column prop="amount" label="金额" width="120">
          <template #default="scope">
            ¥{{ scope.row.amount }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="paymentMethod" label="付款方式" width="100">
          <template #default="scope">
            {{ getPaymentMethodText(scope.row.paymentMethod) }}
          </template>
        </el-table-column>
        <el-table-column prop="orderDate" label="下单日期" width="120" />
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
    
    <!-- 订单编辑对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="currentOrder" :rules="orderRules" ref="orderFormRef" label-width="120px">
        <el-form-item label="订单号" prop="orderNumber">
          <el-input v-model="currentOrder.orderNumber" :disabled="!!currentOrder.id" />
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
          <el-input-number v-model="currentOrder.amount" :min="0" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="付款方式" prop="paymentMethod">
          <el-select v-model="currentOrder.paymentMethod" placeholder="请选择付款方式">
            <el-option label="银行转账" value="bank_transfer" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="微信支付" value="wechat_pay" />
            <el-option label="现金" value="cash" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="currentOrder.status" placeholder="请选择状态">
            <el-option label="待付款" value="pending" />
            <el-option label="已付款" value="paid" />
            <el-option label="已发货" value="shipped" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
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
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveOrder">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { customerAPI, orderAPI } from '../services/api'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'Orders',
  setup() {
    const dialogVisible = ref(false)
    const dialogTitle = ref('')
    const orderFormRef = ref(null)
    
    const searchForm = reactive({
      orderNumber: '',
      customerId: '',
      status: ''
    })
    
    const pagination = reactive({
      currentPage: 1,
      pageSize: 10,
      total: 0
    })
    
    const currentOrder = reactive({
      id: null,
      orderNumber: '',
      customerId: null,
      amount: 0,
      status: 'pending',
      paymentMethod: '',
      orderDate: ''
    })
    
    const orderRules = {
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
    }
    
    const orders = ref([])
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
    
    // 获取订单列表
    const fetchOrders = async () => {
      try {
        const response = await orderAPI.getOrders()
        if (response.data.status === 'success') {
          // 将客户名称添加到订单中，并转换字段名
          const ordersData = response.data.orders.map(order => {
            const customer = customers.value.find(c => c.id === order.customer_id)
            return {
              id: order.id,
              orderNumber: order.order_number,
              customerId: order.customer_id,
              customerName: customer ? customer.name : '未知客户',
              amount: order.amount,
              status: order.status,
              paymentMethod: order.payment_method,
              orderDate: order.order_date ? order.order_date.split('T')[0] : '' // 格式化日期
            }
          })
          orders.value = ordersData
          pagination.total = ordersData.length
        } else {
          ElMessage.error(response.data.message || '获取订单失败')
        }
      } catch (error) {
        console.error('Fetch orders error:', error)
        ElMessage.error('获取订单失败')
      }
    }
    
    // 页面加载时获取数据
    onMounted(() => {
      fetchCustomers()
      fetchOrders()
    })
    
    const handleCreate = () => {
      dialogTitle.value = '新增订单'
      const now = new Date()
      const orderNumber = `ORD${now.getFullYear()}${(now.getMonth() + 1).toString().padStart(2, '0')}${now.getDate().toString().padStart(2, '0')}${Math.floor(Math.random() * 1000).toString().padStart(3, '0')}`
      
      Object.assign(currentOrder, {
        id: null,
        orderNumber: orderNumber,
        customerId: null,
        amount: 0,
        status: 'pending',
        paymentMethod: '',
        orderDate: new Date()
      })
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑订单'
      Object.assign(currentOrder, row)
      dialogVisible.value = true
    }
    
    const handleDelete = (row) => {
      ElMessageBox.confirm(
        `此操作将永久删除该订单, 是否继续?`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // 调用后端API删除订单
          const response = await orderAPI.deleteOrder(row.id)
          if (response.data.status === 'success') {
            ElMessage.success('删除成功!')
            // 重新获取数据以更新列表
            await fetchOrders()
          } else {
            ElMessage.error(response.data.message || '删除失败')
          }
        } catch (error) {
          console.error('Delete order error:', error)
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
      await fetchOrders()
      ElMessage.success('数据刷新成功')
    }
    
    const saveOrder = async () => {
      orderFormRef.value.validate(async (valid) => {
        if (valid) {
          try {
            let response
            if (currentOrder.id) {
              // 更新订单
              const orderData = {
                customer_id: currentOrder.customerId,
                order_number: currentOrder.orderNumber,
                amount: currentOrder.amount,
                status: currentOrder.status,
                payment_method: currentOrder.paymentMethod,
                order_date: currentOrder.orderDate
              }
              
              response = await orderAPI.updateOrder(currentOrder.id, orderData)
            } else {
              // 创建新的订单
              const orderData = {
                customer_id: currentOrder.customerId,
                order_number: currentOrder.orderNumber,
                amount: currentOrder.amount,
                status: currentOrder.status,
                payment_method: currentOrder.paymentMethod,
                order_date: currentOrder.orderDate
              }
              
              response = await orderAPI.createOrder(orderData)
            }
            
            if (response && response.data.status === 'success') {
              ElMessage.success(currentOrder.id ? '订单更新成功' : '订单创建成功')
              dialogVisible.value = false
              // 重新获取数据以更新列表
              await fetchOrders()
            } else {
              ElMessage.error(response.data.message || (currentOrder.id ? '订单更新失败' : '订单创建失败'))
            }
          } catch (error) {
            console.error('Save order error:', error)
            ElMessage.error(currentOrder.id ? '订单更新失败' : '订单创建失败')
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
    
    const getStatusType = (status) => {
      const statusMap = {
        'pending': 'warning',
        'paid': 'primary',
        'shipped': 'info',
        'completed': 'success',
        'cancelled': 'danger'
      }
      return statusMap[status] || 'info'
    }
    
    const getStatusText = (status) => {
      const statusMap = {
        'pending': '待付款',
        'paid': '已付款',
        'shipped': '已发货',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || '未知状态'
    }
    
    // 添加付款方式文本映射函数
    const getPaymentMethodText = (method) => {
      const methodMap = {
        'bank_transfer': '银行转账',
        'alipay': '支付宝',
        'wechat_pay': '微信支付',
        'cash': '现金'
      }
      return methodMap[method] || method || '未知方式'
    }
    
    return {
      dialogVisible,
      dialogTitle,
      orderFormRef,
      searchForm,
      pagination,
      currentOrder,
      orderRules,
      orders,
      customers,
      handleCreate,
      handleEdit,
      handleDelete,
      handleSearch,
      handleRefresh,
      saveOrder,
      handleSizeChange,
      handleCurrentChange,
      getStatusType,
      getStatusText,
      getPaymentMethodText
    }
  }
}
</script>

<style scoped>
.orders-card {
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
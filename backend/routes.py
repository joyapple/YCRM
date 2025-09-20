from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Customer, FollowUp, Opportunity, Order, Task, Department, Role
from decorators import admin_required, permission_required
from datetime import datetime
import json
import random

# 创建蓝图
api = Blueprint('api', __name__)

# 用户认证相关路由
@api.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists', 'status': 'error'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists', 'status': 'error'}), 400
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'employee')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating user: {str(e)}', 'status': 'error'}), 500

@api.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        
        # 查找用户
        user = User.query.filter_by(username=data['username']).first()
        
        # 验证用户和密码
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid username or password', 'status': 'error'}), 401
        
        # 创建访问令牌，将用户ID转换为字符串
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            },
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error during login: {str(e)}', 'status': 'error'}), 500

# 用户相关路由
@api.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """获取所有用户"""
    try:
        users = User.query.all()
        departments = Department.query.all()
        roles = Role.query.all()
        
        # 创建部门和角色字典以便快速查找
        dept_dict = {dept.id: dept.name for dept in departments}
        role_dict = {role.id: role.name for role in roles}
        
        return jsonify({
            'users': [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'department_id': user.department_id,
                'role_id': user.role_id,
                'data_scope': user.data_scope,
                'department_name': dept_dict.get(user.department_id, '未分配'),
                'role_name': role_dict.get(user.role_id, '未分配')
            } for user in users],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching users: {str(e)}', 'status': 'error'}), 500

@api.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    """创建新用户"""
    try:
        data = request.get_json()
        
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists', 'status': 'error'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists', 'status': 'error'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'employee'),
            department_id=data.get('department_id'),
            role_id=data.get('role_id'),
            data_scope=data.get('data_scope', 'own')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating user: {str(e)}', 'status': 'error'}), 500

@api.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """更新用户信息"""
    try:
        current_user_id = get_jwt_identity()
        # 检查当前用户是否有权限（只有管理员可以更新用户信息）
        current_user = User.query.get(current_user_id)
        if current_user.role != 'admin':
            return jsonify({'message': 'Permission denied', 'status': 'error'}), 403
        
        user = User.query.get_or_404(id)
        data = request.get_json()
        
        # 防止普通用户将自己提升为管理员
        if 'role' in data and user.id == int(current_user_id) and user.role == 'admin' and data['role'] != 'admin':
            return jsonify({'message': 'Cannot demote yourself from admin', 'status': 'error'}), 403
        
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        user.role = data.get('role', user.role)
        user.department_id = data.get('department_id', user.department_id)
        user.role_id = data.get('role_id', user.role_id)
        user.data_scope = data.get('data_scope', user.data_scope)
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating user: {str(e)}', 'status': 'error'}), 500

@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """删除用户"""
    try:
        current_user_id = get_jwt_identity()
        # 检查当前用户是否有权限（只有管理员可以删除用户）
        current_user = User.query.get(current_user_id)
        if current_user.role != 'admin':
            return jsonify({'message': 'Permission denied', 'status': 'error'}), 403
        
        # 防止用户删除自己
        if int(current_user_id) == id:
            return jsonify({'message': 'Cannot delete yourself', 'status': 'error'}), 400
        
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting user: {str(e)}', 'status': 'error'}), 500

# 客户相关路由
@api.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    """获取所有客户"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # 根据数据权限范围过滤客户数据
        if current_user.role == 'admin':
            # 管理员可以看到所有客户
            customers = Customer.query.all()
        else:
            if current_user.data_scope == 'own':
                # 仅自己：只能看到自己创建的客户
                customers = Customer.query.filter_by(assigned_to=current_user_id).all()
            elif current_user.data_scope == 'department':
                # 本部门：只能看到本部门用户创建的客户
                if current_user.department_id:
                    # 获取本部门所有用户ID
                    dept_users = User.query.filter_by(department_id=current_user.department_id).all()
                    dept_user_ids = [user.id for user in dept_users]
                    customers = Customer.query.filter(Customer.assigned_to.in_(dept_user_ids)).all()
                else:
                    # 如果用户没有分配部门，则只能看到自己的客户
                    customers = Customer.query.filter_by(assigned_to=current_user_id).all()
            else:
                # 全部：可以看到所有客户
                customers = Customer.query.all()
        
        return jsonify({
            'customers': [{
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'company': customer.company,
                'source': customer.source,
                'status': customer.status,
                'created_at': customer.created_at.isoformat() if customer.created_at else None,
                'updated_at': customer.updated_at.isoformat() if customer.updated_at else None
            } for customer in customers],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching customers: {str(e)}', 'status': 'error'}), 500

@api.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    """创建新客户"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        customer = Customer(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            company=data.get('company'),
            source=data.get('source'),
            status=data.get('status', 'potential'),
            assigned_to=current_user_id
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating customer: {str(e)}', 'status': 'error'}), 500

@api.route('/customers/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    """更新客户信息"""
    try:
        customer = Customer.query.get_or_404(id)
        data = request.get_json()
        
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.company = data.get('company', customer.company)
        customer.source = data.get('source', customer.source)
        customer.status = data.get('status', customer.status)
        
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating customer: {str(e)}', 'status': 'error'}), 500

@api.route('/customers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    """删除客户"""
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting customer: {str(e)}', 'status': 'error'}), 500

# 销售跟进管理
@api.route('/followups', methods=['GET'])
@jwt_required()
def get_followups():
    """获取所有跟进记录"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # 根据数据权限范围过滤跟进记录数据
        if current_user.role == 'admin':
            # 管理员可以看到所有跟进记录
            followups = FollowUp.query.all()
        else:
            if current_user.data_scope == 'own':
                # 仅自己：只能看到自己的跟进记录
                followups = FollowUp.query.filter_by(user_id=current_user_id).all()
            elif current_user.data_scope == 'department':
                # 本部门：只能看到本部门用户的跟进记录
                if current_user.department_id:
                    # 获取本部门所有用户ID
                    dept_users = User.query.filter_by(department_id=current_user.department_id).all()
                    dept_user_ids = [user.id for user in dept_users]
                    followups = FollowUp.query.filter(FollowUp.user_id.in_(dept_user_ids)).all()
                else:
                    # 如果用户没有分配部门，则只能看到自己的跟进记录
                    followups = FollowUp.query.filter_by(user_id=current_user_id).all()
            else:
                # 全部：可以看到所有跟进记录
                followups = FollowUp.query.all()
        
        return jsonify({
            'followups': [{
                'id': followup.id,
                'customer_id': followup.customer_id,
                'user_id': followup.user_id,
                'content': followup.content,
                'followup_type': followup.followup_type,
                'followup_time': followup.followup_time.isoformat() if followup.followup_time else None,
                'next_followup_date': followup.next_followup_date.isoformat() if followup.next_followup_date else None,
                'status': followup.status
            } for followup in followups],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching followups: {str(e)}', 'status': 'error'}), 500

@api.route('/followups', methods=['POST'])
@jwt_required()
def create_followup():
    """创建新跟进记录"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 解析日期时间
        followup_time = None
        if data.get('followup_time'):
            followup_time = datetime.fromisoformat(data['followup_time'].replace('Z', '+00:00'))
        
        next_followup_date = None
        if data.get('next_followup_date'):
            next_followup_date = datetime.fromisoformat(data['next_followup_date'].replace('Z', '+00:00'))
        
        followup = FollowUp(
            customer_id=data['customer_id'],
            user_id=current_user_id,  # 设置创建跟进记录的用户ID
            content=data['content'],
            followup_type=data.get('followup_type'),
            followup_time=followup_time,
            next_followup_date=next_followup_date,
            status=data.get('status', 'pending')
        )
        db.session.add(followup)
        db.session.commit()
        return jsonify({'message': 'FollowUp created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating followup: {str(e)}', 'status': 'error'}), 500

@api.route('/followups/<int:id>', methods=['PUT'])
@jwt_required()
def update_followup(id):
    """更新跟进记录"""
    try:
        followup = FollowUp.query.get_or_404(id)
        data = request.get_json()
        
        # 解析日期时间
        followup_time = None
        if data.get('followup_time'):
            followup_time = datetime.fromisoformat(data['followup_time'].replace('Z', '+00:00'))
        
        next_followup_date = None
        if data.get('next_followup_date'):
            next_followup_date = datetime.fromisoformat(data['next_followup_date'].replace('Z', '+00:00'))
        
        followup.customer_id = data.get('customer_id', followup.customer_id)
        followup.user_id = data.get('user_id', followup.user_id)
        followup.content = data.get('content', followup.content)
        followup.followup_type = data.get('followup_type', followup.followup_type)
        followup.followup_time = followup_time or followup.followup_time
        followup.next_followup_date = next_followup_date or followup.next_followup_date
        followup.status = data.get('status', followup.status)
        
        db.session.commit()
        return jsonify({'message': 'FollowUp updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating followup: {str(e)}', 'status': 'error'}), 500

@api.route('/followups/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_followup(id):
    """删除跟进记录"""
    try:
        followup = FollowUp.query.get_or_404(id)
        db.session.delete(followup)
        db.session.commit()
        return jsonify({'message': 'FollowUp deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting followup: {str(e)}', 'status': 'error'}), 500

# 商机管理
@api.route('/opportunities', methods=['GET'])
@jwt_required()
def get_opportunities():
    """获取所有商机"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # 根据数据权限范围过滤商机数据
        if current_user.role == 'admin':
            # 管理员可以看到所有商机
            opportunities = Opportunity.query.all()
        else:
            if current_user.data_scope == 'own':
                # 仅自己：只能看到自己创建的商机
                opportunities = Opportunity.query.filter(
                    Opportunity.user_id == current_user_id
                ).all()
            elif current_user.data_scope == 'department':
                # 本部门：只能看到本部门用户创建的商机
                if current_user.department_id:
                    # 获取本部门所有用户ID
                    dept_users = User.query.filter_by(department_id=current_user.department_id).all()
                    dept_user_ids = [user.id for user in dept_users]
                    opportunities = Opportunity.query.filter(
                        Opportunity.user_id.in_(dept_user_ids)
                    ).all()
                else:
                    # 如果用户没有分配部门，则只能看到自己的商机
                    opportunities = Opportunity.query.filter(
                        Opportunity.user_id == current_user_id
                    ).all()
            else:
                # 全部：可以看到所有商机
                opportunities = Opportunity.query.all()
        
        return jsonify({
            'opportunities': [{
                'id': opportunity.id,
                'name': opportunity.name,
                'customer_id': opportunity.customer_id,
                'user_id': opportunity.user_id,
                'description': opportunity.description,
                'estimated_amount': opportunity.estimated_amount,
                'status': opportunity.status,
                'created_at': opportunity.created_at.isoformat() if opportunity.created_at else None,
                'updated_at': opportunity.updated_at.isoformat() if opportunity.updated_at else None
            } for opportunity in opportunities],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching opportunities: {str(e)}', 'status': 'error'}), 500

@api.route('/opportunities', methods=['POST'])
@jwt_required()
def create_opportunity():
    """创建新商机"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        opportunity = Opportunity(
            customer_id=data['customer_id'],
            user_id=current_user_id,  # 设置创建商机的用户ID
            name=data['name'],
            description=data.get('description'),
            estimated_amount=data['estimated_amount'],
            probability=data['probability'],
            status=data.get('status', 'open')
        )
        db.session.add(opportunity)
        db.session.commit()
        return jsonify({'message': 'Opportunity created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating opportunity: {str(e)}', 'status': 'error'}), 500

@api.route('/opportunities/<int:id>', methods=['PUT'])
@jwt_required()
def update_opportunity(id):
    """更新商机"""
    try:
        opportunity = Opportunity.query.get_or_404(id)
        data = request.get_json()
        
        opportunity.customer_id = data.get('customer_id', opportunity.customer_id)
        opportunity.name = data.get('name', opportunity.name)
        opportunity.description = data.get('description', opportunity.description)
        opportunity.estimated_amount = data.get('estimated_amount', opportunity.estimated_amount)
        opportunity.probability = data.get('probability', opportunity.probability)
        opportunity.status = data.get('status', opportunity.status)
        
        db.session.commit()
        return jsonify({'message': 'Opportunity updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating opportunity: {str(e)}', 'status': 'error'}), 500

@api.route('/opportunities/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_opportunity(id):
    """删除商机"""
    try:
        opportunity = Opportunity.query.get_or_404(id)
        db.session.delete(opportunity)
        db.session.commit()
        return jsonify({'message': 'Opportunity deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting opportunity: {str(e)}', 'status': 'error'}), 500

# 订单管理
@api.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """获取所有订单"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # 根据数据权限范围过滤订单数据
        if current_user.role == 'admin':
            # 管理员可以看到所有订单
            orders = Order.query.all()
        else:
            if current_user.data_scope == 'own':
                # 仅自己：只能看到自己创建的订单
                orders = Order.query.filter(
                    Order.user_id == current_user_id
                ).all()
            elif current_user.data_scope == 'department':
                # 本部门：只能看到本部门用户创建的订单
                if current_user.department_id:
                    # 获取本部门所有用户ID
                    dept_users = User.query.filter_by(department_id=current_user.department_id).all()
                    dept_user_ids = [user.id for user in dept_users]
                    orders = Order.query.filter(
                        Order.user_id.in_(dept_user_ids)
                    ).all()
                else:
                    # 如果用户没有分配部门，则只能看到自己的订单
                    orders = Order.query.filter(
                        Order.user_id == current_user_id
                    ).all()
            else:
                # 全部：可以看到所有订单
                orders = Order.query.all()
        
        return jsonify({
            'orders': [{
                'id': order.id,
                'customer_id': order.customer_id,
                'user_id': order.user_id,
                'opportunity_id': order.opportunity_id,
                'order_number': order.order_number,
                'amount': order.amount,
                'payment_method': order.payment_method,
                'status': order.status,
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'updated_at': order.updated_at.isoformat() if order.updated_at else None
            } for order in orders],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching orders: {str(e)}', 'status': 'error'}), 500

@api.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """创建新订单"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 生成唯一的订单号
        order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(1000, 9999)}"
        
        order = Order(
            customer_id=data['customer_id'],
            user_id=current_user_id,  # 设置创建订单的用户ID
            opportunity_id=data.get('opportunity_id'),
            order_number=order_number,
            amount=data['amount'],
            payment_method=data.get('payment_method'),
            status=data.get('status', 'pending')
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating order: {str(e)}', 'status': 'error'}), 500

@api.route('/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    """更新订单"""
    try:
        order = Order.query.get_or_404(id)
        data = request.get_json()
        
        # 解析订单日期
        order_date = None
        if data.get('order_date'):
            order_date = datetime.fromisoformat(data['order_date'].replace('Z', '+00:00'))
        
        order.customer_id = data.get('customer_id', order.customer_id)
        order.opportunity_id = data.get('opportunity_id', order.opportunity_id)
        order.order_number = data.get('order_number', order.order_number)
        order.amount = data.get('amount', order.amount)
        order.status = data.get('status', order.status)
        order.payment_method = data.get('payment_method', order.payment_method)
        order.order_date = order_date or order.order_date
        
        db.session.commit()
        return jsonify({'message': 'Order updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating order: {str(e)}', 'status': 'error'}), 500

@api.route('/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    """删除订单"""
    try:
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting order: {str(e)}', 'status': 'error'}), 500

# 任务与日程管理
@api.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """获取所有任务"""
    try:
        current_user_id = get_jwt_identity()
        tasks = Task.query.all()
        return jsonify({
            'tasks': [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'assigned_to': task.assigned_to,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority': task.priority,
                'status': task.status
            } for task in tasks],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching tasks: {str(e)}', 'status': 'error'}), 500

@api.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """创建新任务"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 解析截止日期
        due_date = None
        if data.get('due_date'):
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        
        task = Task(
            title=data['title'],
            description=data.get('description'),
            assigned_to=data.get('assigned_to'),
            due_date=due_date,
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending')
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating task: {str(e)}', 'status': 'error'}), 500

# 部门相关路由
@api.route('/departments', methods=['GET'])
@jwt_required()
@admin_required
def get_departments():
    """获取所有部门"""
    try:
        departments = Department.query.all()
        return jsonify({
            'departments': [{
                'id': dept.id,
                'name': dept.name,
                'description': dept.description,
                'created_at': dept.created_at.isoformat() if dept.created_at else None,
                'updated_at': dept.updated_at.isoformat() if dept.updated_at else None
            } for dept in departments],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching departments: {str(e)}', 'status': 'error'}), 500

@api.route('/departments', methods=['POST'])
@jwt_required()
@admin_required
def create_department():
    """创建新部门"""
    try:
        data = request.get_json()
        
        # 检查部门名称是否已存在
        if Department.query.filter_by(name=data['name']).first():
            return jsonify({'message': 'Department name already exists', 'status': 'error'}), 400
        
        department = Department(
            name=data['name'],
            description=data.get('description', '')
        )
        
        db.session.add(department)
        db.session.commit()
        return jsonify({'message': 'Department created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating department: {str(e)}', 'status': 'error'}), 500

@api.route('/departments/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_department(id):
    """更新部门信息"""
    try:
        department = Department.query.get_or_404(id)
        data = request.get_json()
        
        # 检查部门名称是否已存在（排除当前部门）
        if 'name' in data and data['name'] != department.name:
            if Department.query.filter_by(name=data['name']).first():
                return jsonify({'message': 'Department name already exists', 'status': 'error'}), 400
        
        department.name = data.get('name', department.name)
        department.description = data.get('description', department.description)
        
        db.session.commit()
        return jsonify({'message': 'Department updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating department: {str(e)}', 'status': 'error'}), 500

@api.route('/departments/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_department(id):
    """删除部门"""
    try:
        department = Department.query.get_or_404(id)
        
        # 检查是否有用户关联到该部门
        if department.users:
            return jsonify({'message': 'Cannot delete department with associated users', 'status': 'error'}), 400
        
        db.session.delete(department)
        db.session.commit()
        return jsonify({'message': 'Department deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting department: {str(e)}', 'status': 'error'}), 500

# 角色相关路由
@api.route('/roles', methods=['GET'])
@jwt_required()
@admin_required
def get_roles():
    """获取所有角色"""
    try:
        roles = Role.query.all()
        return jsonify({
            'roles': [{
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'permissions': role.permissions,
                'created_at': role.created_at.isoformat() if role.created_at else None,
                'updated_at': role.updated_at.isoformat() if role.updated_at else None
            } for role in roles],
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching roles: {str(e)}', 'status': 'error'}), 500

@api.route('/roles', methods=['POST'])
@jwt_required()
@admin_required
def create_role():
    """创建新角色"""
    try:
        data = request.get_json()
        
        # 检查角色名称是否已存在
        if Role.query.filter_by(name=data['name']).first():
            return jsonify({'message': 'Role name already exists', 'status': 'error'}), 400
        
        role = Role(
            name=data['name'],
            description=data.get('description', ''),
            permissions=data.get('permissions', '')
        )
        
        db.session.add(role)
        db.session.commit()
        return jsonify({'message': 'Role created successfully', 'status': 'success'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating role: {str(e)}', 'status': 'error'}), 500

@api.route('/roles/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_role(id):
    """更新角色信息"""
    try:
        role = Role.query.get_or_404(id)
        data = request.get_json()
        
        # 检查角色名称是否已存在（排除当前角色）
        if 'name' in data and data['name'] != role.name:
            if Role.query.filter_by(name=data['name']).first():
                return jsonify({'message': 'Role name already exists', 'status': 'error'}), 400
        
        role.name = data.get('name', role.name)
        role.description = data.get('description', role.description)
        role.permissions = data.get('permissions', role.permissions)
        
        db.session.commit()
        return jsonify({'message': 'Role updated successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating role: {str(e)}', 'status': 'error'}), 500

@api.route('/roles/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_role(id):
    """删除角色"""
    try:
        role = Role.query.get_or_404(id)
        
        # 检查是否有用户关联到该角色
        if role.users:
            return jsonify({'message': 'Cannot delete role with associated users', 'status': 'error'}), 400
        
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'Role deleted successfully', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting role: {str(e)}', 'status': 'error'}), 500

# 健康检查路由
@api.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'OK', 'message': 'YCRM API is running'}), 200
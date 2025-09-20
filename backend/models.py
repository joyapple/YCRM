from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Department(db.Model):
    """部门模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到用户表
    users = db.relationship('User', backref='department', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Role(db.Model):
    """角色模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    permissions = db.Column(db.Text)  # 存储权限列表，可以是JSON格式
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到用户表
    users = db.relationship('User', backref='role_obj', lazy=True)
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # admin, employee
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))  # 部门关联
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 角色关联
    data_scope = db.Column(db.String(20), nullable=False, default='own')  # 数据权限范围: own, department, all
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """设置密码并加密"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'
    
    def is_employee(self):
        """检查用户是否为普通员工"""
        return self.role == 'employee'

    def __repr__(self):
        return f'<User {self.username}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    address = db.Column(db.Text)
    source = db.Column(db.String(50))  # 客户来源
    status = db.Column(db.String(50), default='potential')  # 客户状态: potential,意向,成交,流失
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))  # 指派给哪个销售
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到用户表
    user = db.relationship('User', backref=db.backref('customers', lazy=True))

    def __repr__(self):
        return f'<Customer {self.name}>'

class FollowUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 跟进内容
    followup_type = db.Column(db.String(20))  # 跟进方式: 电话,邮件,面谈等
    followup_time = db.Column(db.DateTime, default=datetime.utcnow)  # 跟进时间
    next_followup_date = db.Column(db.DateTime)  # 下次跟进时间
    status = db.Column(db.String(20), default='pending')  # 跟进状态: pending, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联到客户表和用户表
    customer = db.relationship('Customer', backref=db.backref('followups', lazy=True))
    user = db.relationship('User', backref=db.backref('followups', lazy=True))

    def __repr__(self):
        return f'<FollowUp {self.id}>'

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 关联的用户（销售）
    name = db.Column(db.String(100), nullable=False)  # 商机名称
    description = db.Column(db.Text)  # 商机描述
    estimated_amount = db.Column(db.Float)  # 预估金额
    probability = db.Column(db.Integer)  # 成交概率(0-100)
    status = db.Column(db.String(20), default='open')  # 商机状态: open, won, lost
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到客户表和用户表
    customer = db.relationship('Customer', backref=db.backref('opportunities', lazy=True))
    user = db.relationship('User', backref=db.backref('opportunities', lazy=True))

    def __repr__(self):
        return f'<Opportunity {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 关联的用户（销售）
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'))  # 关联的商机
    order_number = db.Column(db.String(50), unique=True, nullable=False)  # 订单编号
    amount = db.Column(db.Float, nullable=False)  # 订单金额
    status = db.Column(db.String(20), default='pending')  # 订单状态: pending, paid, shipped, completed, cancelled
    payment_method = db.Column(db.String(20))  # 付款方式
    order_date = db.Column(db.DateTime, default=datetime.utcnow)  # 下单日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到客户表、用户表和商机表
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    opportunity = db.relationship('Opportunity', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'<Order {self.order_number}>'

class Task(db.Model):
    """任务与日程管理模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # 任务标题
    description = db.Column(db.Text)  # 任务描述
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))  # 分配给谁
    due_date = db.Column(db.DateTime)  # 截止日期
    priority = db.Column(db.String(10), default='medium')  # 优先级: low, medium, high
    status = db.Column(db.String(20), default='pending')  # 状态: pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联到用户表
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.title}>'
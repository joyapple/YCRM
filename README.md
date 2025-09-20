# YCRM 客户关系管理系统

YCRM (Yet another CRM) 是一个基于Vue 3 + Flask开发的轻量级客户关系管理系统，旨在帮助中小企业和个人更好地管理客户信息、销售跟进、商机和订单等业务流程。

## 功能特性

- **用户认证**: 用户注册、登录和权限管理
- **客户管理**: 客户信息的增删改查，客户状态跟踪
- **销售跟进**: 记录客户跟进情况，安排下次跟进计划
- **商机管理**: 商机跟踪，预估金额和成交概率管理
- **订单管理**: 订单创建、状态跟踪和付款管理
- **任务管理**: 个人任务和日程安排
- **数据统计**: 仪表板展示关键业务指标和图表

## 技术栈

### 前端
- Vue 3 (Composition API)
- Element Plus UI 组件库
- Vue Router 路由管理
- Axios HTTP 客户端
- ECharts 数据可视化

### 后端
- Flask Python Web 框架
- Flask-JWT-Extended JWT 认证
- Flask-SQLAlchemy ORM
- SQLite 数据库

## 项目结构

```
YCRM/
├── backend/           # 后端代码
│   ├── app.py         # Flask 应用入口
│   ├── models.py      # 数据模型定义
│   ├── routes.py      # API 路由
│   ├── config.py      # 配置文件
│   └── init_db.py     # 数据库初始化脚本
├── frontend/          # 前端代码
│   ├── src/
│   │   ├── views/     # 页面组件
│   │   ├── components/ # 可复用组件
│   │   ├── services/  # API 服务
│   │   ├── router/    # 路由配置
│   │   ├── App.vue    # 根组件
│   │   └── main.js    # 应用入口
│   └── index.html     # HTML 模板
└── README.md          # 项目说明文档
```

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 14+
- npm 6+

### 后端启动

1. 进入后端目录:
   ```bash
   cd backend
   ```

2. 安装Python依赖:
   ```bash
   pip install -r requirements.txt
   ```

3. 初始化数据库:
   ```bash
   python init_db.py
   ```

4. 启动后端服务:
   ```bash
   python app.py
   ```
   默认运行在 `http://localhost:5000`

### 前端启动

1. 进入前端目录:
   ```bash
   cd frontend
   ```

2. 安装npm依赖:
   ```bash
   npm install
   ```

3. 启动前端开发服务器:
   ```bash
   npm run dev
   ```
   默认运行在 `http://localhost:3000`

## API 接口

系统提供RESTful API接口，主要包含以下模块:

- **认证接口**: `/api/register`, `/api/login`
- **用户接口**: `/api/users`
- **客户接口**: `/api/customers`
- **跟进接口**: `/api/followups`
- **商机接口**: `/api/opportunities`
- **订单接口**: `/api/orders`
- **任务接口**: `/api/tasks`

## 数据库设计

系统使用SQLite数据库，包含以下主要表:

- `user`: 用户表
- `customer`: 客户表
- `followup`: 跟进记录表
- `opportunity`: 商机表
- `order`: 订单表
- `task`: 任务表

## 开发指南

### 前端开发
- 使用Vue 3 Composition API
- 组件化开发，遵循单文件组件(SFC)规范
- 使用Element Plus组件库
- 通过Axios与后端API交互

### 后端开发
- 遵循RESTful API设计原则
- 使用Flask-JWT-Extended实现JWT认证
- 使用Flask-SQLAlchemy进行数据库操作
- 通过装饰器实现路由保护

## 部署说明

### 生产环境部署
1. 构建前端:
   ```bash
   cd frontend
   npm run build
   ```

2. 配置生产环境变量
3. 使用生产级WSGI服务器(如Gunicorn)部署Flask应用
4. 配置反向代理(如Nginx)

## 常见问题

### 登录后页面空白
确保路由配置正确，登录后应跳转到 `/layout/dashboard` 路径。

### 数据无法保存
检查后端API是否正常运行，确认请求是否携带有效的JWT Token。

### 图表不显示
确认ECharts库是否正确引入，检查图表容器是否正确初始化。

## 贡献

欢迎提交Issue和Pull Request来改进系统。

## 许可证

本项目采用GNU General Public License v3.0开源许可证。根据该许可证的要求，任何使用本项目代码或对其进行修改的用户，都必须将修改后的代码同样以开源方式发布。

详细许可证内容请参见 [LICENSE](LICENSE) 文件。
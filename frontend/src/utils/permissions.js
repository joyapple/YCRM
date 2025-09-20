/**
 * 权限检查工具函数
 */

/**
 * 检查用户是否具有指定角色
 * @param {Object} user - 当前用户对象
 * @param {string} requiredRole - 所需的角色
 * @returns {boolean} 是否具有权限
 */
export const hasPermission = (user, requiredRole) => {
  if (!user || !user.role) return false
  
  // 管理员拥有所有权限
  if (user.role === 'admin') return true
  
  // 检查是否具有指定角色
  return user.role === requiredRole
}

/**
 * 检查用户是否是管理员
 * @param {Object} user - 当前用户对象
 * @returns {boolean} 是否是管理员
 */
export const isAdmin = (user) => {
  return user && user.role === 'admin'
}

/**
 * 检查用户是否是普通员工
 * @param {Object} user - 当前用户对象
 * @returns {boolean} 是否是普通员工
 */
export const isEmployee = (user) => {
  return user && user.role === 'employee'
}

export default {
  hasPermission,
  isAdmin,
  isEmployee
}
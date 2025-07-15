# Production Management System - React Frontend

数字类器官模型（Digital Organoid ModelS, DOMS）生产管理系统前端应用

## 项目简介

这是一个基于 React + TypeScript + Tailwind CSS 构建的现代化生产管理系统前端，用于管理产品、库存、任务、需求、物料和余料等生产相关业务。

## 技术栈

- **React 19** - 用户界面库
- **TypeScript** - 类型安全的 JavaScript
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Vite** - 现代化的前端构建工具
- **React Router** - 客户端路由
- **FullCalendar** - 日历和任务调度组件
- **Lucide React** - 现代化图标库

## 功能模块

### 🏭 生产管理
- **产品管理** - 产品信息的增删改查，支持产品、母液、原料、耗材四种类型
- **库存管理** - 实时库存查看和管理，库存预警
- **任务管理** - 生产任务的创建、分配、跟踪，支持任务视图和排班视图
- **需求管理** - 生产需求的管理和规划
- **物料管理** - 生产物料的管理和追踪
- **余料管理** - 生产余料的处理和管理

### 🎨 界面特性
- 响应式设计，支持多设备访问
- Element UI 风格的设计语言
- 支持中文界面
- 现代化的用户体验

## 快速开始

### 环境要求
- Node.js >= 18.0.0
- npm >= 8.0.0

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

应用将在 http://localhost:3000 启动

### 构建生产版本
```bash
npm run build
```

### 预览生产构建
```bash
npm run preview
```

## 项目结构

```
src/
├── components/          # 组件目录
│   ├── ui/             # 通用 UI 组件
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Table.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   └── index.ts
│   ├── Layout.tsx      # 主布局组件
│   ├── Topbar.tsx      # 顶部导航栏
│   ├── Sidebar.tsx     # 侧边栏导航
│   └── FullCalendar.tsx # 日历组件
├── pages/              # 页面组件
│   ├── ProductManagement.tsx
│   ├── InventoryManagement.tsx
│   ├── TaskManagement.tsx
│   ├── DemandManagement.tsx
│   ├── MaterialManagement.tsx
│   ├── ScrapManagement.tsx
│   └── index.ts
├── types/              # TypeScript 类型定义
│   └── index.ts
├── App.tsx             # 主应用组件
├── main.tsx           # 应用入口
└── index.css          # 全局样式
```

## 开发指南

### 代码规范
- 使用 TypeScript 进行开发
- 遵循 ESLint 规则
- 使用 Prettier 格式化代码
- 组件使用 PascalCase 命名
- 文件使用 camelCase 命名

### 样式规范
- 优先使用 Tailwind CSS 类名
- 自定义样式写在 `@layer components` 中
- 保持样式的一致性和可维护性

### 组件开发
- 使用函数式组件和 Hooks
- 合理拆分组件，保持单一职责
- 使用 TypeScript 定义 Props 类型
- 添加适当的错误处理

## 可用脚本

- `npm run dev` - 启动开发服务器
- `npm run build` - 构建生产版本
- `npm run preview` - 预览生产构建
- `npm run lint` - 运行 ESLint 检查
- `npm run lint:fix` - 自动修复 ESLint 错误
- `npm run type-check` - 运行 TypeScript 类型检查

## 浏览器支持

- Chrome >= 88
- Firefox >= 85
- Safari >= 14
- Edge >= 88

## 故障排除

### 开发服务器无法启动
如果 `npm run dev` 命令失败，请尝试以下解决方案：

1. **确保在正确目录**：
   ```bash
   cd /path/to/frontend-react
   pwd  # 应该显示 .../frontend-react
   ```

2. **直接使用 Vite**：
   ```bash
   npx vite
   # 或指定端口
   npx vite --port 3000
   ```

3. **清理缓存**：
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **检查端口占用**：
   ```bash
   lsof -ti:3000  # 检查 3000 端口
   kill -9 $(lsof -ti:3000)  # 终止占用进程
   ```

### 浏览器显示 404 错误
- 确保开发服务器正在运行
- 检查控制台是否有错误信息
- 尝试强制刷新页面 (Cmd+Shift+R)

## License

This project is licensed under the MIT License.

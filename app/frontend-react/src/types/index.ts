export interface Product {
  id: number;
  type: '产品' | '母液' | '原料' | '耗材';
  name: string;
  code: string;
  spec: string;
  unit?: string;
  quantity?: number;
  created?: string;
  updated?: string;
}

export interface InventoryItem extends Product {
  quantity: number;
  latestInTime?: string;
  latestOutTime?: string;
}

export interface Task {
  id: number;
  productType: '产品' | '母液' | '原料' | '耗材';
  productName: string;
  productCode: string;
  status: '待生产' | '生产中' | '已完成' | '已暂停';
  assignee?: string;
  createdAt: string;
  updatedAt?: string;
  dueDate?: string;
}

export interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end: string;
  backgroundColor?: string;
  borderColor?: string;
}

export interface User {
  id: string;
  name: string;
  avatar?: string;
  role: string;
}

export interface MenuItem {
  key: string;
  label: string;
  icon?: string;
  path?: string;
  children?: MenuItem[];
}

// Constants matching backend models
export const Category = {
  ORGANOID: "Organoid(类器官)",
  CONSUMABLE: "Consumable(耗材)",
  EQUIPMENT: "Equipment(设备)",
  REAGENT: "Reagent(试剂)"
} as const;

export const SubCategory = {
  HUMAN_ORGANOID: "Human Organoid(人源类器官)",
  MOUSE_ORGANOID: "Mouse Organoid(小鼠类器官)",
  OTHER_AUXILIARY_REAGENTS: "Other Auxiliary Reagents(其他辅助试剂)",
  CRYOTUBES: "Cryotubes(冷冻管)",
  MATRIGEL: "Matrigel(基质胶)",
  LARGE_EQUIPMENT: "Large Equipment(大型设备)",
  PRIMERS: "Primers(引物)",
  CENTRIFUGE_TUBE: "Centrifuge Tube(离心管)",
  PIPETTE_TIPS: "Pipette Tips(移液枪吸头)",
  PIPETTE: "Pipette(移液枪)",
  ORGANOID_DIFFERENTIATION_MEDIUM: "Organoid Differentiation Medium(类器官分化培养基)",
  ORGANOID_CULTURE_KIT: "Organoid Culture Kit(类器官培养套件)",
  ORGANOID_BASAL_MEDIUM: "Organoid Basal Medium(类器官基础培养基)",
  COMPLETE_ORGANOID_CULTURE_MEDIUM: "Complete Organoid Culture Medium(类器官完全培养基)",
  ORGANOID_CONDITIONED_MEDIUM: "Organoid Conditioned Medium(类器官条件培养基)",
  CELL_CULTURE_PLATE: "Cell Culture Plate(细胞培养板)",
  CELL_CULTURE_FLASK: "Cell Culture Flask(细胞培养瓶)",
  CELL_CULTURE_DISH: "Cell Culture Dish(细胞培养皿)",
  CELL_CULTURE_REAGENTS: "Cell Culture Reagents(细胞培养试剂)",
  CELL_SHAKE_FLASK: "Cell Shake Flask(细胞摇瓶)",
  CELL_COUNTING_PLATE: "Cell Counting Plate(细胞计数板)",
  CHIP: "Chip(芯片)",
  SERUM: "Serum(血清)"
} as const;

export const Source = {
  HUMAN: "Human(人源)",
  MOUSE: "Mouse(鼠源)",
  HESC: "hESC(人胚胎干细胞)",
  HPSC: "hPSC(人诱导多能干细胞)"
} as const;

export const Unit = {
  BOX: "Box(盒)",
  PACKET: "Packet(包)",
  BOTTLE: "Bottle(瓶)",
  UNIT: "Unit(台)",
  TUBE: "Tube(支)",
  BIGBOX: "Big Box(箱)"
} as const;

export const InventoryStatus = {
  AVAILABLE: "AVAILABLE(可用)",
  RESERVED: "RESERVED(预留)", 
  IN_USE: "IN_USE(使用中)",
  EXPIRED: "EXPIRED(过期)",
  DAMAGED: "DAMAGED(损坏)",
  QUARANTINE: "QUARANTINE(隔离)",
  OUT_OF_STOCK: "OUT_OF_STOCK(缺货)"
} as const;

export type CategoryType = typeof Category[keyof typeof Category];
export type SubCategoryType = typeof SubCategory[keyof typeof SubCategory];
export type SourceType = typeof Source[keyof typeof Source];
export type UnitType = typeof Unit[keyof typeof Unit];
export type InventoryStatusType = typeof InventoryStatus[keyof typeof InventoryStatus];

export interface ProductDetails {
  productid: string;
  category: CategoryType;
  setsubcategory: SubCategoryType;
  source: SourceType;
  productnameen: string;
  productnamezh: string;
  specification: string;
  unit: UnitType;
  components: string[];
  is_sold_independently: boolean;
  remarks_temperature?: string;
  storage_temperature_duration?: string;
  reorderlevel: number;
  targetstocklevel: number;
  leadtime: number;
}

export interface ProductInventory extends ProductDetails {
  batchid_internal: string;
  batchid_external: string;
  basicmediumid: string;
  addictiveid: string;
  quantityinstock: number;
  productiondate: string;
  imageurl: string;
  status: InventoryStatusType;
  productiondatetime: string;
  producedby: string;
  to_show: boolean;
  lastupdated: string;
  lastupdatedby: string;
  // COA fields
  coa_appearance?: string;
  coa_clarity?: boolean;
  coa_osmoticpressure?: number;
  coa_ph?: number;
  coa__mycoplasma?: boolean;
  coa_sterility?: boolean;
  coa_fillingvolumedifference?: boolean;
}

// ProductInventory create request type that matches backend schema
export interface ProductInventoryCreateRequest {
  productid: string;
  basicmediumid: string;
  addictiveid: string;
  quantityinstock: number;
  productiondate: string; // YYYY-MM-DD format
  status: InventoryStatusType;
  productiondatetime: string; // ISO datetime string
  producedby: string;
  to_show: boolean;
  lastupdatedby: string;
  // Optional fields
  imageurl?: string;
  // COA fields (optional)
  coa_appearance?: string;
  coa_clarity?: boolean;
  coa_osmoticpressure?: number;
  coa_ph?: number;
  coa__mycoplasma?: boolean;
  coa_sterility?: boolean;
  coa_fillingvolumedifference?: boolean;
}

// Legacy interface for backward compatibility
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

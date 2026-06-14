# 基米吃饭 - 数据目录

## 目录结构

```
data/
├── raw/                        # 原始数据
│   ├── usda_sr_legacy/         # USDA SR Legacy（英文）
│   ├── usda_foundation/        # USDA Foundation Foods（英文）
│   ├── china_food/             # 中国食物成分表（中文）
│   └── openfoodfacts/          # Open Food Facts（多语言）
│
├── processed/                  # 处理后的数据
│   ├── foods.json              # 统一格式的食材数据
│   ├── train.json              # 训练数据
│   └── val.json                # 验证数据
│
└── knowledge_base/             # RAG 知识库
    ├── chroma/                 # ChromaDB 数据
    └── embeddings/             # 向量数据
```

---

## 数据集语言分类

| 数据集 | 语言 | 数据量 | 格式 | 优先级 |
|--------|------|--------|------|--------|
| **USDA SR Legacy** | 英文 | ~8,000 种 | CSV | 第一优先级 |
| **USDA Foundation Foods** | 英文 | ~2,000 种 | CSV | 第一优先级 |
| **中国食物成分表** | 中文 | ~2,000 种 | CSV/JSON | 第二优先级 |
| **Open Food Facts** | 多语言 | ~3,000,000 种 | CSV/JSON | 第三优先级 |

---

## 数据集详细说明

### 1. USDA SR Legacy（英文）

**来源**：USDA FoodData Central
**语言**：英文
**数据量**：~8,000 种食物
**格式**：CSV
**下载链接**：
```
https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_csv_2018-04.zip
```
**说明**：核心营养数据来源，包含常用食材的标准化营养信息。

---

### 2. USDA Foundation Foods（英文）

**来源**：USDA FoodData Central
**语言**：英文
**数据量**：~2,000 种食物
**格式**：CSV
**下载链接**：
```
https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip
```
**说明**：补充数据源，提供更详细的营养信息。

---

### 3. 中国食物成分表（中文）

**来源**：中国疾病预防控制中心
**语言**：中文
**数据量**：~2,000 种食物
**格式**：CSV/JSON
**搜索链接**：
- https://github.com/search?q=中国食物成分表&type=repositories
- https://www.sciencedb.cn/
**说明**：中式食材数据，需要手动下载或从 GitHub 获取。

---

### 4. Open Food Facts（多语言）

**来源**：Open Food Facts
**语言**：多语言（含中文）
**数据量**：~3,000,000 种产品
**格式**：CSV/JSON/Parquet
**下载链接**：
- CSV: https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz
- JSONL: https://static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz
**说明**：全球食品数据，可按国家筛选。

---

## 数据使用策略

### MVP 阶段

1. **主要数据源**：USDA SR Legacy（英文）
2. **补充数据源**：USDA Foundation Foods（英文）
3. **中文翻译**：建立食材名称对照表

### 后续阶段

1. **补充中式食材**：中国食物成分表（中文）
2. **品牌食品**：Open Food Facts（多语言）
3. **数据增强**：添加价格、包装等信息

---

## 数据格式规范

### 统一食材数据格式

```json
{
  "food_id": 1,
  "name_cn": "鸡胸肉",
  "name_en": "Chicken Breast",
  "category": "肉类",
  "serving_size": 100,
  "serving_unit": "g",
  "nutrition": {
    "protein": 20.0,
    "fat": 2.0,
    "carbs": 0.0,
    "calories": 110
  },
  "common_portions": [
    {"amount": 100, "unit": "g"},
    {"amount": 200, "unit": "g"}
  ],
  "tags": ["高蛋白", "低脂", "肉类"],
  "source": "USDA"
}
```

---

## 备注

- **USDA 数据**：公开免费使用，无版权限制
- **中国食物成分表**：版权属于中国 CDC，仅限个人学习使用
- **Open Food Facts**：Open Database License，可免费使用
- 所有数据仅用于个人学习和研究目的

---

**来源**：
- [USDA FoodData Central](https://fdc.nal.usda.gov/)
- [Open Food Facts](https://world.openfoodfacts.org/)
- [中国科学数据](https://www.sciencedb.cn/)

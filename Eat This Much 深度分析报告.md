# Eat This Much 深度分析报告

> **分析目的**: 以 Eat This Much 为模板，为学校食堂配餐系统提供参考
> **分析日期**: 2026-06-10
> **信息来源**: [eatthismuch.com](https://www.eatthismuch.com/)

---

## 一、产品概述

### 1.1 基本信息

| 项目 | 详情 |
|------|------|
| **产品名称** | Eat This Much |
| **官网** | [eatthismuch.com](https://www.eatthismuch.com/) |
| **定位** | 自动化宏量营养素配餐平台 |
| **用户规模** | 400万+ 用户 |
| **餐食生成量** | 2.1亿+ 份 |
| **数据库规模** | 6,000+ 食谱，1,000,000+ 种食物 |
| **平台** | 网页 + iOS + Android |
| **媒体评价** | CNN Underscored 2025年最佳配餐App |
| **评分** | iOS 4.7星（22,000+评价），Android 4.6星（10,100+评价） |

### 1.2 核心价值主张

> "Turn meal planning into an effortless and magical experience"
> （将配餐变成轻松而神奇的体验）

**核心解决的问题**：
- 用户不知道吃什么才能达到营养目标
- 手动计算宏量营养素太复杂
- 每天决定吃什么很费脑
- 购物清单整理麻烦

### 1.3 创始团队

| 成员 | 职责 | 背景 |
|------|------|------|
| Louis DeMenthon | 创始人兼CEO | 产品愿景 |
| Patrick McKeown | 联合创始人兼CTO | 技术架构 |
| Matt Sisinni | 移动端开发 | iOS/Android |
| Brian Keyes | Web开发 | 前端/后端 |
| Elias Teeny | 移动端开发 | iOS/Android |
| Erin Mario | 用户体验负责人 | UX设计 |
| Tabitha W. | 用户幸福专员 | 客户支持 |
| Nat DeMenthon | UX设计师/艺术家 | 食物插画 |
| Taylor Berggren | 注册营养师 | 营养顾问 |

**团队特点**：小而精（7人核心+2外部），技术+产品+营养专业结合

---

## 二、核心功能详解

### 2.1 功能架构图

```
Eat This Much 功能架构
│
├── 🎯 配餐引擎（核心）
│   ├── 宏量营养素目标设定
│   ├── TDEE/BMR 计算
│   ├── 按日差异化营养目标
│   └── 无限再生算法
│
├── 📊 数据库系统
│   ├── 6,000+ 食谱
│   ├── 1,000,000+ 食物
│   └── 营养成分数据
│
├── 👤 用户偏好系统
│   ├── 餐食评分机制
│   ├── 食材屏蔽/过滤
│   ├── 饮食类型选择
│   └── 循环餐食设置
│
├── 🏠 食材管理（Pantry）
│   ├── 库存追踪
│   ├── 保鲜期监控
│   └── 库存优先推荐
│
├── 🛒 购物清单
│   ├── 自动生成
│   ├── Instacart集成
│   └── Amazon Fresh集成
│
├── 📈 营养追踪
│   ├── 热量追踪
│   ├── 体重进展
│   └── 目标达成
│
└── 📱 多平台
    ├── 网页版
    ├── iOS App
    └── Android App
```

---

### 2.2 功能模块详细分析

#### 模块一：配餐引擎（核心算法）

**输入参数**：
```
用户输入
├── 基本信息：年龄、性别、身高、体重、体脂率
├── 活动水平：久坐/轻度/中度/高度/极高
├── 目标：减脂/维持/增肌
├── 营养目标：蛋白质、脂肪、碳水（克数或百分比）
└── 餐食偏好：每天几餐、饮食类型
```

**算法流程**：
```
Step 1: 计算 BMR（基础代谢率）
        使用 Mifflin-St Jeor 方程
        男性: BMR = 10×体重(kg) + 6.25×身高(cm) - 5×年龄 - 161 + 5
        女性: BMR = 10×体重(kg) + 6.25×身高(cm) - 5×年龄 - 161 - 161

Step 2: 计算 TDEE（总每日能量消耗）
        TDEE = BMR × 活动系数
        活动系数: 1.2(久坐) ~ 1.9(极高运动量)

Step 3: 根据目标调整热量
        减脂: TDEE × 0.8（20%赤字）
        维持: TDEE × 1.0
        增肌: TDEE × 1.15（15%盈余）

Step 4: 分配宏量营养素
        蛋白质: 基于体重和活动量（0.82-1.1 g/lb）
        脂肪: 最低0.3 g/lb（减脂）或0.5 g/lb（维持/增肌）
        碳水: 剩余热量分配

Step 5: 生成餐食计划
        从数据库中选择符合营养目标的食物组合
        考虑用户偏好和屏蔽规则
        按餐次分配
```

**关键创新点**：
- **绝对克数而非百分比**：用户直接设定蛋白质/脂肪/碳水的克数，更直观
- **按日差异化**：支持每天不同营养目标（适合碳水循环）
- **无限再生**：不满意可一键重新生成

**来源**: [eatthismuch.com/tdee-calculator](https://www.eatthismuch.com/tdee-calculator/)

---

#### 模块二：数据库系统

**数据规模**：
| 类型 | 数量 | 说明 |
|------|------|------|
| 食谱 | 6,000+ | 完整的菜品配方 |
| 食物 | 1,000,000+ | 单个食材/食品 |
| 营养素 | 每种食物20+项 | 蛋白质、脂肪、碳水、维生素、矿物质等 |

**数据来源推测**：
- USDA（美国农业部）营养数据库
- 用户贡献的食谱
- 合作营养师审核

**数据结构推测**：
```json
{
  "food_id": 12345,
  "name": "Chicken Breast",
  "serving_size": 100,
  "serving_unit": "g",
  "nutrition": {
    "calories": 165,
    "protein": 31,
    "fat": 3.6,
    "carbs": 0,
    "fiber": 0,
    "vitamins": {...},
    "minerals": {...}
  },
  "tags": ["high-protein", "low-fat", "meat"],
  "allergens": ["none"]
}
```

---

#### 模块三：用户偏好系统

**评分机制**：
```
用户对餐食评分（1-5星）
    ↓
系统学习偏好
    ↓
正面反馈: 推荐类似餐食
负面反馈: 避免推荐相似餐食
```

**食材过滤系统**：
| 过滤类型 | 示例 | 实现方式 |
|----------|------|----------|
| 饮食类型 | 素食、生酮、Paleo | 食物标签筛选 |
| 过敏源 | 坚麸、乳糖、海鲜 | 食物过敏源标记 |
| 食材屏蔽 | 不喜欢番茄、香菜 | 用户黑名单 |
| 关键词过滤 | "无糖"、"低脂" | 文本匹配 |

**循环餐食**：
- 用户可将喜爱的餐食设为"每周重复"
- 适合饮食要求固定或时间有限的用户
- 被标注为"Great For Bodybuilding Diets"

---

#### 模块四：食材管理（Pantry）

**功能详解**：
```
虚拟储藏室
├── 库存录入：用户手动添加家中食材
├── 数量追踪：实时更新食材用量
├── 保鲜期监控：提醒即将过期的食材
└── 智能推荐：优先使用库存中的食材
```

**价值**：
- 减少食物浪费
- 降低购物成本
- 提高食材利用率

---

#### 模块五：购物清单系统

**工作流程**：
```
生成餐食计划
    ↓
提取所需食材
    ↓
合并相同食材
    ↓
减去库存已有
    ↓
生成购物清单
    ↓
一键下单（Instacart/Amazon Fresh）
```

**集成平台**：
- Instacart：美国生鲜配送
- Amazon Fresh：亚马逊生鲜

---

#### 模块六：营养追踪

**追踪维度**：
| 维度 | 数据 | 可视化 |
|------|------|--------|
| 热量摄入 | 每日/每周/每月 | 图表 |
| 宏量营养素 | 蛋白质/脂肪/碳水 | 进度条 |
| 体重变化 | 历史趋势 | 折线图 |
| 目标达成 | 完成百分比 | 仪表盘 |

**平台累计数据**：
- 追踪 420亿+ 卡路里
- 生成 2.1亿+ 份餐食

---

### 2.3 功能优先级矩阵

| 功能 | 重要性 | 实现难度 | 用户价值 | 学校食堂适用性 |
|------|--------|----------|----------|----------------|
| 宏量营养素配餐 | ⭐⭐⭐⭐⭐ | 中 | 高 | ⭐⭐⭐⭐⭐ |
| 食材数据库 | ⭐⭐⭐⭐⭐ | 高 | 高 | ⭐⭐⭐⭐⭐ |
| 用户偏好过滤 | ⭐⭐⭐⭐ | 中 | 高 | ⭐⭐⭐⭐ |
| 食材替代 | ⭐⭐⭐⭐ | 中 | 高 | ⭐⭐⭐⭐⭐ |
| 一日三餐分配 | ⭐⭐⭐⭐ | 低 | 中 | ⭐⭐⭐⭐⭐ |
| 购物清单 | ⭐⭐⭐ | 低 | 中 | ⭐⭐（食堂不需要） |
| Pantry管理 | ⭐⭐ | 中 | 中 | ⭐（食堂不需要） |
| 营养追踪 | ⭐⭐⭐ | 中 | 中 | ⭐⭐⭐ |

---

## 三、技术栈分析

### 3.1 已确认的技术

| 层级 | 技术 | 证据来源 |
|------|------|----------|
| **前端框架** | SvelteKit | URL路径 `/_app/immutable/assets/` 是SvelteKit特征 |
| **CDN/安全** | Cloudflare | `/cdn-cgi/l/email-protection` 是Cloudflare特征 |
| **分析工具** | Google Analytics | Similarweb数据 |
| **广告平台** | Google AdSense | Similarweb数据 |
| **移动端** | iOS + Android | App Store/Google Play |

### 3.2 推测的技术栈

基于行业标准和产品特征，推测如下：

```
Eat This Much 技术栈推测
│
├── 前端
│   ├── 框架: SvelteKit（已确认）
│   ├── 状态管理: Svelte stores
│   ├── UI组件: 自定义组件 + 可能使用 Skeleton/Flowbite
│   └── 构建工具: Vite（SvelteKit默认）
│
├── 后端（推测）
│   ├── 语言: Python 或 Node.js
│   ├── 框架: Django/FastAPI (Python) 或 Express/NestJS (Node.js)
│   ├── API: RESTful API
│   └── 认证: JWT
│
├── 数据库（推测）
│   ├── 主数据库: PostgreSQL（存储用户、食谱、营养数据）
│   ├── 缓存: Redis（会话、热点数据）
│   └── 搜索: Elasticsearch（食物搜索）
│
├── 移动端（推测）
│   ├── 方案A: React Native（跨平台）
│   ├── 方案B: Flutter（跨平台）
│   └── 方案C: 原生开发（Swift + Kotlin）
│
├── 基础设施
│   ├── CDN: Cloudflare（已确认）
│   ├── 云平台: AWS/GCP（推测）
│   └── CI/CD: GitHub Actions（推测）
│
└── 第三方服务
    ├── 支付: Stripe
    ├── 配送: Instacart API, Amazon Fresh API
    ├── 分析: Google Analytics
    └── 广告: Google AdSense
```

### 3.3 核心算法实现推测

> ⚠️ **重要说明**：Eat This Much 是闭源产品，以下伪代码是我根据官网公开信息推断编写的，**不是真实源代码**。

#### 信息来源与确定性标注

| 标记 | 含义 | 来源 |
|------|------|------|
| ✅ **确定** | 官网明确说明或引用的科学公式 | [eatthismuch.com/tdee-calculator](https://www.eatthismuch.com/tdee-calculator/) |
| ⚠️ **推测** | 基于行业惯例和技术逻辑推断 | 通用算法知识 |
| ❓ **假设** | 无法验证，仅为合理猜测 | 我的推断 |

#### 宏量营养素配餐算法

```python
# ====================================================================
# 伪代码：Eat This Much 配餐算法推测
# 作者：Claude Code（基于官网公开信息推断）
# 日期：2026-06-10
# ====================================================================

# ---- 第一部分：基础代谢率（BMR）计算 ----
# ✅ 确定：官网明确说明使用 Mifflin-St Jeor 方程
# 来源：https://www.eatthismuch.com/tdee-calculator/
# 原文："We use the Mifflin-St Jeor equation to estimate your BMR,
#        which research has found to be the most accurate predictive
#        formula for BMR in non-obese individuals."

def calculate_bmr(weight, height, age, gender):
    """
    ✅ 确定：使用 Mifflin-St Jeor 方程计算基础代谢率
    
    参数：
        weight: 体重（kg）
        height: 身高（cm）
        age: 年龄
        gender: 性别（"male" 或 "female"）
    
    返回：基础代谢率（千卡/天）
    """
    if gender == "male":
        # ✅ 确定：男性公式
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        # ✅ 确定：女性公式
        return 10 * weight + 6.25 * height - 5 * age - 161


# ---- 第二部分：总每日能量消耗（TDEE）计算 ----
# ✅ 确定：官网说明 TDEE = BMR × 活动系数
# ✅ 确定：活动系数范围从 1.2（久坐）到 1.9（极高运动量）
# ⚠️ 推测：具体的活动系数数值（1.2, 1.375, 1.55, 1.725, 1.9）
#          这些是健身行业通用数值，官网未列出具体数字

def calculate_tdee(bmr, activity_level):
    """
    ✅ 确定：计算总每日能量消耗
    ⚠️ 推测：具体活动系数数值
    
    原文："Your TDEE is calculated by multiplying your BMR by an
            activity factor based on how much you exercise."
    """
    # ⚠️ 推测：这些系数是健身行业标准，但官网未明确列出
    activity_multipliers = {
        "sedentary": 1.2,      # 久坐不动
        "light": 1.375,        # 轻度活动（每周1-3天）
        "moderate": 1.55,      # 中度活动（每周3-5天）
        "active": 1.725,       # 高度活动（每周6-7天）
        "very_active": 1.9     # 极高运动量（每天2次）
    }
    return bmr * activity_multipliers[activity_level]


# ---- 第三部分：目标热量调整 ----
# ✅ 确定：官网明确说明调整系数
# 来源：https://www.eatthismuch.com/tdee-calculator/
# 原文："Lose weight: TDEE × 0.8 (default 20% deficit)"
#        "Gain weight: TDEE × 1.15 (default 15% surplus)"

def adjust_for_goal(tdee, goal):
    """
    ✅ 确定：根据目标调整热量
    
    原文明确说明：
    - 减脂：TDEE × 0.8（20%赤字）
    - 增肌：TDEE × 1.15（15%盈余）
    - 维持：TDEE × 1.0
    """
    if goal == "lose":
        return tdee * 0.8  # ✅ 确定：20%赤字
    elif goal == "gain":
        return tdee * 1.15  # ✅ 确定：15%盈余
    else:
        return tdee  # ✅ 确定：维持


# ---- 第四部分：宏量营养素分配 ----
# ✅ 确定：使用绝对克数而非百分比
# ✅ 确定：蛋白质基于体重计算（0.82-1.1 g/lb）
# ✅ 确定：脂肪最低 0.3 g/lb（减脂）或 0.5 g/lb（维持/增肌）
# ✅ 确定：碳水 = 剩余热量
# ⚠️ 推测：具体的蛋白质系数（2.4 g/kg 和 1.8 g/kg）
#          原文说的是 g/lb，我转换为 g/kg

def calculate_macros(target_calories, weight, goal):
    """
    ✅ 确定：计算宏量营养素目标
    
    官网原文：
    - 蛋白质："up to ~0.82 g/lb (1.8 g/kg)" 对肌肉蛋白合成最大益处
    - 蛋白质（减脂）："up to ~1.1 g/lb or 2.4 g/kg" 保护瘦体重
    - 脂肪（减脂）：最低 "0.3 g/lb"
    - 脂肪（维持/增肌）："0.5 g/lb"
    - 碳水：根据活动量和目标弹性调整
    """
    # ✅ 确定：蛋白质基于体重计算
    if goal == "lose":
        protein = weight * 2.4  # ✅ 确定：减脂期 2.4 g/kg（原文 1.1 g/lb）
    else:
        protein = weight * 1.8  # ✅ 确定：维持/增肌 1.8 g/kg（原文 0.82 g/lb）

    # ✅ 确定：脂肪最低需求
    if goal == "lose":
        fat = weight * 0.3 * 2.2  # ✅ 确定：0.3 g/lb = 0.66 g/kg
    else:
        fat = weight * 0.5 * 2.2  # ✅ 确定：0.5 g/lb = 1.1 g/kg

    # ✅ 确定：碳水 = 剩余热量
    # ✅ 确定：4-4-9 法则（蛋白质4kcal/g，脂肪9kcal/g，碳水4kcal/g）
    protein_calories = protein * 4
    fat_calories = fat * 9
    carb_calories = target_calories - protein_calories - fat_calories
    carbs = carb_calories / 4

    return {
        "protein": round(protein),
        "fat": round(fat),
        "carbs": round(carbs)
    }


# ---- 第五部分：餐食计划生成 ----
# ⚠️ 推测：整体流程（官网未公开具体算法）
# ❓ 假设：使用贪心算法或线性规划（行业通用做法）

def generate_meal_plan(macros, num_meals, food_database, user_preferences):
    """
    ⚠️ 推测：生成餐食计划的整体流程
    
    官网说明了功能（支持1-6餐/天、按日差异化目标），
    但未公开具体算法实现。
    """
    # ⚠️ 推测：将总营养目标平均分配到各餐
    per_meal = {
        "protein": macros["protein"] / num_meals,
        "fat": macros["fat"] / num_meals,
        "carbs": macros["carbs"] / num_meals
    }

    # ⚠️ 推测：从数据库中筛选符合条件的食物
    # 官网说明支持饮食类型、过敏源、食材屏蔽等过滤
    filtered_foods = filter_foods(
        food_database,
        diet_type=user_preferences["diet"],
        allergies=user_preferences["allergies"],
        blocked_ingredients=user_preferences["blocked"]
    )

    # ⚠️ 推测：为每餐生成食物组合
    meals = []
    for meal_idx in range(num_meals):
        meal = optimize_meal(
            filtered_foods,
            per_meal,
            meal_type=["breakfast", "lunch", "dinner", "snack"][meal_idx]
        )
        meals.append(meal)

    return meals


# ---- 第六部分：单餐优化 ----
# ❓ 假设：使用贪心算法（我猜测的实现方式）
# 实际可能使用线性规划、遗传算法或其他优化方法

def optimize_meal(foods, target_macros, meal_type):
    """
    ❓ 假设：优化单餐食物组合
    
    这是我猜测的简化版实现，实际算法可能更复杂。
    可能的优化方法：
    1. 贪心算法（这里展示的）
    2. 线性规划（更精确）
    3. 遗传算法（处理复杂约束）
    4. 动态规划
    """
    # ❓ 假设：使用贪心算法
    selected = []
    remaining = target_macros.copy()

    # ❓ 假设：按蛋白质/热量比排序（优先高蛋白食物）
    foods_sorted = sorted(foods, key=lambda f: f["protein"]/f["calories"], reverse=True)

    for food in foods_sorted:
        if can_add_food(food, remaining, meal_type):
            serving = calculate_serving(food, remaining)
            selected.append({"food": food, "serving": serving})
            remaining = subtract_nutrition(remaining, food, serving)

            # ❓ 假设：当剩余需求小于阈值时停止
            if is_satisfied(remaining):
                break

    return selected
```

#### 确定性总结

| 函数 | 确定性 | 依据 |
|------|--------|------|
| `calculate_bmr()` | ✅ 确定 | 官网明确说明使用 Mifflin-St Jeor 方程 |
| `calculate_tdee()` | ✅ 确定 / ⚠️ 部分推测 | 官网说明了公式，但具体系数是行业通用值 |
| `adjust_for_goal()` | ✅ 确定 | 官网明确说明调整系数（0.8/1.15） |
| `calculate_macros()` | ✅ 确定 | 官网明确说明了蛋白质、脂肪的计算方式 |
| `generate_meal_plan()` | ⚠️ 推测 | 官网未公开具体算法，我基于功能推断 |
| `optimize_meal()` | ❓ 假设 | 完全是我猜测的实现方式 |

---

## 四、优点分析

### 4.1 产品设计优点

#### 优点一：极简的用户体验
```
用户操作流程：
输入目标 → 一键生成 → 查看计划 → 满意就用，不满意就重新生成

关键设计：
- 默认设置即可用（不需要复杂配置）
- 无限再生降低决策压力
- 清晰的营养目标展示
```

**为什么好**：
- 降低使用门槛
- 减少用户认知负担
- 提高用户留存

#### 优点二：灵活的营养目标系统
```
传统方式：设定百分比（蛋白质30%，脂肪20%，碳水50%）
Eat This Much：设定克数（蛋白质150g，脂肪60g，碳水200g）

优势：
- 更直观（用户知道自己需要多少克蛋白质）
- 更灵活（每天可以不同）
- 更科学（基于体重计算）
```

**为什么好**：
- 符合专业健身人群需求
- 更容易理解和执行
- 支持复杂的营养方案

#### 优点三：智能化的偏好学习
```
用户行为 → 系统学习 → 优化推荐

评分机制：对餐食打分 → 系统学习偏好
食材屏蔽：直接排除不喜欢的食材
循环重复：喜欢的餐食可以定期出现
```

**为什么好**：
- 越用越精准
- 尊重用户偏好
- 减少重复推荐

#### 优点四：完整的闭环体验
```
计划 → 执行 → 追踪 → 调整

配餐计划 → 购物清单 → 配送下单 → 营养追踪 → 目标调整
```

**为什么好**：
- 覆盖用户完整需求
- 提高用户粘性
- 创造商业价值

#### 优点五：数据驱动的产品迭代
```
累计数据：
- 400万+用户
- 2.1亿+份餐食
- 420亿+卡路里追踪

用途：
- 优化推荐算法
- 改进用户体验
- 验证产品价值
```

---

### 4.2 技术实现优点

#### 优点一：选择 SvelteKit 框架
```
SvelteKit 优势：
- 编译时框架，性能优异
- 文件系统路由，开发效率高
- 内置 SSR/SSG，SEO友好
- 学习曲线平缓
- 构建产物小
```

**为什么好**：
- 适合小团队快速开发
- 性能优于 React/Vue
- 部署简单

#### 优点二：数据库设计合理
```
推测的数据结构：
- 食物表：存储所有食物和营养数据
- 食谱表：存储完整食谱配方
- 用户表：存储用户信息和偏好
- 评分表：存储用户对餐食的评分
- 计划表：存储生成的餐食计划
```

**为什么好**：
- 数据结构清晰
- 支持复杂查询
- 便于扩展

#### 优点三：算法设计科学
```
营养计算：
- 使用 Mifflin-St Jeor 方程（最准确的BMR公式）
- 基于科学文献设定营养素目标
- 支持按日差异化目标
```

**为什么好**：
- 科学依据充分
- 计算结果可信
- 支持个性化

---

### 4.3 商业模式优点

#### 优点一：免费+增值模式
```
免费版：每日配餐、基础功能
付费版：周计划、购物清单、配送集成

定价：
- $5/月（年付）
- $14.99/月（月付）
```

**为什么好**：
- 降低获客成本
- 免费用户可转化为付费用户
- 收入可预测

#### 优点二：广告+订阅双收入
```
收入来源：
1. 订阅收入（Premium会员）
2. 广告收入（Google AdSense）
3. 配送分成（Instacart/Amazon Fresh）
```

**为什么好**：
- 收入多元化
- 降低单一收入风险
- 最大化用户价值

---

## 五、可借鉴之处

### 5.1 学校食堂配餐系统可借鉴的功能

| 功能 | 借鉴程度 | 学校食堂适配方案 |
|------|----------|------------------|
| 宏量营养素配餐 | ⭐⭐⭐⭐⭐ | 完全借鉴，针对学生体质调整参数 |
| 食材数据库 | ⭐⭐⭐⭐⭐ | 建立食堂专用食材数据库 |
| 用户偏好过滤 | ⭐⭐⭐⭐ | 支持忌口、过敏源、个人喜好 |
| 食材替代 | ⭐⭐⭐⭐⭐ | 核心功能，食堂菜品有限需要替代方案 |
| 一日三餐分配 | ⭐⭐⭐⭐⭐ | 完全符合食堂场景 |
| 购物清单 | ⭐ | 不需要，食堂统一采购 |
| Pantry管理 | ⭐ | 不需要，食堂统一管理 |
| 营养追踪 | ⭐⭐⭐ | 可选功能，帮助学生了解营养摄入 |

### 5.2 技术栈借鉴

| 层级 | Eat This Much | 学校食堂系统建议 |
|------|---------------|------------------|
| 前端 | SvelteKit | SvelteKit 或 Vue.js（国内更流行） |
| 后端 | Python/Node.js | Python（FastAPI/Django） |
| 数据库 | PostgreSQL | PostgreSQL + Redis |
| 移动端 | React Native/Flutter | 微信小程序（更易推广） |
| AI/算法 | 规则算法 | RAG + LLM（更智能） |

### 5.3 算法借鉴

**直接借鉴**：
- Mifflin-St Jeor 方程计算BMR/TDEE
- 宏量营养素分配逻辑（绝对克数而非百分比）
- 按日差异化营养目标

**改进方向**：
- 使用 LLM 理解自然语言输入
- 使用 RAG 检索匹配食材
- 使用向量数据库存储营养知识

---

## 六、学校食堂配餐系统设计建议

### 6.1 核心功能设计

```
学校食堂配餐系统
│
├── 输入模块
│   ├── 手动输入：蛋白质/脂肪/碳水克数
│   ├── 自然语言输入："我想增肌，每天需要多少蛋白质"
│   └── 目标选择：减脂/维持/增肌
│
├── 配餐引擎
│   ├── 营养目标计算（BMR/TDEE）
│   ├── 食材匹配（从食堂菜单中筛选）
│   ├── 份量计算（达到营养目标的食材用量）
│   └── 一日三餐分配
│
├── 偏好系统
│   ├── 忌口设置（如：不吃香菜）
│   ├── 过敏源标记（如：花生过敏）
│   └── 喜好学习（基于历史选择）
│
├── 替代系统
│   ├── 营养等效替代（番茄→黄瓜，蛋白质相近）
│   ├── 食材可用性检查（食堂今天有没有这个菜）
│   └── 替代方案推荐
│
└── 输出模块
    ├── 推荐食材及用量
    ├── 一日三餐菜谱
    └── 营养成分报告
```

### 6.2 数据库设计

```sql
-- 食材表
CREATE TABLE foods (
    food_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),  -- 蔬菜、肉类、主食等
    serving_size DECIMAL(10,2),  -- 份量（克）
    protein DECIMAL(10,2),  -- 蛋白质（克）
    fat DECIMAL(10,2),  -- 脂肪（克）
    carbs DECIMAL(10,2),  -- 碳水化合物（克）
    calories DECIMAL(10,2),  -- 热量（千卡）
    available BOOLEAN DEFAULT true  -- 食堂是否供应
);

-- 食堂菜单表
CREATE TABLE cafeteria_menu (
    menu_id SERIAL PRIMARY KEY,
    food_id INTEGER REFERENCES foods(food_id),
    date DATE NOT NULL,
    meal_type VARCHAR(20),  -- 早餐、午餐、晚餐
    price DECIMAL(10,2),
    available BOOLEAN DEFAULT true
);

-- 用户偏好表
CREATE TABLE user_preferences (
    user_id INTEGER PRIMARY KEY,
    blocked_foods INTEGER[],  -- 屏蔽的食材ID
    allergies INTEGER[],  -- 过敏源食材ID
    goal VARCHAR(20),  -- 减脂、维持、增肌
    weight DECIMAL(10,2),
    height DECIMAL(10,2),
    age INTEGER,
    gender VARCHAR(10),
    activity_level VARCHAR(20)
);

-- 用户评分表
CREATE TABLE user_ratings (
    user_id INTEGER,
    food_id INTEGER,
    rating INTEGER,  -- 1-5星
    created_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, food_id)
);
```

### 6.3 技术架构建议

```
学校食堂配餐系统技术架构
│
├── 前端
│   ├── 方案A: 微信小程序（推荐，学生易用）
│   ├── 方案B: Web应用（SvelteKit/Vue.js）
│   └── 方案C: 两者都要
│
├── 后端
│   ├── 框架: FastAPI (Python)
│   ├── API: RESTful API
│   └── 认证: JWT
│
├── 数据库
│   ├── 主库: PostgreSQL（存储食材、菜单、用户数据）
│   ├── 缓存: Redis（会话、热点数据）
│   └── 向量库: ChromaDB（存储食材嵌入，用于RAG检索）
│
├── AI/算法层
│   ├── LLM: Qwen2.5/ChatGLM（理解自然语言）
│   ├── Embedding: text2vec（食材文本向量化）
│   ├── RAG: LangChain（检索增强生成）
│   └── 算法: 营养计算、配餐优化
│
└── 部署
    ├── 云平台: AutoDL/阿里云
    ├── 容器: Docker
    └── CI/CD: GitHub Actions
```

---

## 七、总结

### 7.1 Eat This Much 的核心成功因素

1. **简单易用**：一键生成，降低使用门槛
2. **科学准确**：基于营养学研究的算法
3. **灵活定制**：支持多种饮食需求和偏好
4. **完整闭环**：从计划到执行到追踪
5. **数据驱动**：基于用户行为持续优化

### 7.2 学校食堂系统的关键差异化

1. **场景聚焦**：只服务学校食堂，不追求通用
2. **中文支持**：完全中文化的界面和食材
3. **食堂集成**：与食堂菜单和供应系统对接
4. **AI增强**：使用LLM和RAG提供更智能的服务
5. **成本可控**：开源技术栈，云平台部署

### 7.3 下一步行动

1. **收集数据**：整理学校食堂的食材和菜单数据
2. **搭建环境**：配置开发环境（AutoDL + VSCode）
3. **开发MVP**：先实现核心配餐功能
4. **测试迭代**：邀请同学测试，收集反馈
5. **完善功能**：逐步添加偏好、替代等功能

---

## 参考来源

1. [Eat This Much 官网](https://www.eatthismuch.com/) - 产品介绍
2. [Eat This Much How It Works](https://www.eatthismuch.com/how-it-works/) - 功能详解
3. [Eat This Much FAQ](https://www.eatthismuch.com/faq/) - 免费/付费功能
4. [Eat This Much TDEE Calculator](https://www.eatthismuch.com/tdee-calculator/) - 算法原理
5. [Eat This Much About](https://www.eatthismuch.com/about/) - 团队信息
6. [Similarweb - eatthismuch.com](https://www.similarweb.com/website/eatthismuch.com/) - 技术栈分析

---

**文档生成日期**: 2026-06-10
**分析人**: Claude Code

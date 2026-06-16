# -*- coding: utf-8 -*-
"""
数据清洗脚本

功能：
1. 去除无效数据（营养数据缺失）
2. 去除重复数据
3. 验证数据合理性
4. 统一分类名称
5. 添加常用标签

输入：
- foods.json: 原始食材数据

输出：
- foods_cleaned.json: 清洗后的食材数据
"""

import json
import os
from pathlib import Path


def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, file_path):
    """保存 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_valid_nutrition(nutrition):
    """
    验证营养数据是否有效

    规则：
    - 所有营养素 >= 0
    - 蛋白质 <= 100g/100g
    - 脂肪 <= 100g/100g
    - 碳水 <= 100g/100g
    - 热量 <= 900kcal/100g
    """
    protein = nutrition.get('protein', 0)
    fat = nutrition.get('fat', 0)
    carbs = nutrition.get('carbs', 0)
    calories = nutrition.get('calories', 0)

    # 检查是否为负数
    if protein < 0 or fat < 0 or carbs < 0 or calories < 0:
        return False

    # 检查是否超过合理范围
    if protein > 100 or fat > 100 or carbs > 100:
        return False

    if calories > 900:
        return False

    return True


def has_nutrition_data(nutrition):
    """
    检查是否有营养数据

    规则：至少有一项营养素大于 0
    """
    protein = nutrition.get('protein', 0)
    fat = nutrition.get('fat', 0)
    carbs = nutrition.get('carbs', 0)
    calories = nutrition.get('calories', 0)

    return protein > 0 or fat > 0 or carbs > 0 or calories > 0


def generate_tags(food):
    """
    生成食物标签

    基于营养数据自动添加标签
    """
    tags = []
    nutrition = food.get('nutrition', {})
    protein = nutrition.get('protein', 0)
    fat = nutrition.get('fat', 0)
    carbs = nutrition.get('carbs', 0)
    calories = nutrition.get('calories', 0)

    # 蛋白质标签
    if protein >= 20:
        tags.append('高蛋白')
    elif protein >= 10:
        tags.append('中蛋白')
    else:
        tags.append('低蛋白')

    # 脂肪标签
    if fat >= 20:
        tags.append('高脂')
    elif fat >= 10:
        tags.append('中脂')
    else:
        tags.append('低脂')

    # 碳水标签
    if carbs >= 50:
        tags.append('高碳水')
    elif carbs >= 20:
        tags.append('中碳水')
    else:
        tags.append('低碳水')

    # 热量标签
    if calories >= 400:
        tags.append('高热量')
    elif calories >= 200:
        tags.append('中热量')
    else:
        tags.append('低热量')

    # 分类标签
    category = food.get('category', '')
    if 'Meat' in category or 'Poultry' in category or 'Seafood' in category:
        tags.append('肉类')
    elif 'Vegetable' in category:
        tags.append('蔬菜')
    elif 'Fruit' in category:
        tags.append('水果')
    elif 'Dairy' in category or 'Cheese' in category:
        tags.append('乳制品')
    elif 'Grain' in category or 'Cereal' in category or 'Baked' in category:
        tags.append('主食')
    elif 'Nut' in category or 'Seed' in category:
        tags.append('坚果')

    return tags


def clean_data(foods):
    """
    清洗数据

    参数：
        foods: 原始食物数据列表

    返回：
        清洗后的食物数据列表
    """
    print("=" * 50)
    print("开始数据清洗")
    print("=" * 50)

    total_count = len(foods)
    print(f"\n原始数据量: {total_count}")

    # 1. 去除无效数据
    print("\n[1/5] 去除无效数据...")
    valid_foods = []
    invalid_count = 0
    for food in foods:
        nutrition = food.get('nutrition', {})
        if has_nutrition_data(nutrition) and is_valid_nutrition(nutrition):
            valid_foods.append(food)
        else:
            invalid_count += 1
    print(f"  去除了 {invalid_count} 条无效数据")
    print(f"  剩余 {len(valid_foods)} 条数据")

    # 2. 去除重复数据
    print("\n[2/5] 去除重复数据...")
    seen = set()
    unique_foods = []
    duplicate_count = 0
    for food in valid_foods:
        food_id = food.get('food_id')
        if food_id not in seen:
            seen.add(food_id)
            unique_foods.append(food)
        else:
            duplicate_count += 1
    print(f"  去除了 {duplicate_count} 条重复数据")
    print(f"  剩余 {len(unique_foods)} 条数据")

    # 3. 验证数据合理性
    print("\n[3/5] 验证数据合理性...")
    valid_foods = []
    invalid_range_count = 0
    for food in unique_foods:
        nutrition = food.get('nutrition', {})
        if is_valid_nutrition(nutrition):
            valid_foods.append(food)
        else:
            invalid_range_count += 1
    print(f"  去除了 {invalid_range_count} 条范围不合理数据")
    print(f"  剩余 {len(valid_foods)} 条数据")

    # 4. 添加标签
    print("\n[4/5] 添加标签...")
    for food in valid_foods:
        food['tags'] = generate_tags(food)
    print(f"  已为 {len(valid_foods)} 条数据添加标签")

    # 5. 数据统计
    print("\n[5/5] 数据统计...")
    categories = {}
    for food in valid_foods:
        cat = food.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n清洗后数据量: {len(valid_foods)}")
    print(f"去除数据量: {total_count - len(valid_foods)}")
    print(f"保留比例: {len(valid_foods) / total_count * 100:.1f}%")

    print(f"\n分类统计 (Top 10):")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count}")

    return valid_foods


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent

    # 输入文件
    input_file = os.path.join(project_root, 'data', 'processed', 'foods.json')

    # 输出文件
    output_file = os.path.join(project_root, 'data', 'processed', 'foods_cleaned.json')

    # 加载数据
    print(f"加载数据: {input_file}")
    foods = load_json(input_file)
    print(f"加载了 {len(foods)} 条数据")

    # 清洗数据
    cleaned_foods = clean_data(foods)

    # 保存数据
    print(f"\n保存数据: {output_file}")
    save_json(cleaned_foods, output_file)
    print(f"[OK] 保存成功")

    # 显示示例数据
    print("\n" + "=" * 50)
    print("示例数据")
    print("=" * 50)
    for food in cleaned_foods[:3]:
        print(f"\n  {food['name_en']}")
        print(f"    分类: {food['category']}")
        print(f"    蛋白质: {food['nutrition']['protein']}g")
        print(f"    脂肪: {food['nutrition']['fat']}g")
        print(f"    碳水: {food['nutrition']['carbs']}g")
        print(f"    热量: {food['nutrition']['calories']}kcal")
        print(f"    标签: {', '.join(food['tags'])}")


if __name__ == '__main__':
    main()

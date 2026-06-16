# -*- coding: utf-8 -*-
"""
USDA 数据解析脚本

功能：
1. 解析 USDA SR Legacy 数据
2. 提取食物基本信息和营养数据
3. 转换为统一的 JSON 格式

输入：
- food.csv: 食物基本信息
- nutrient.csv: 营养素定义
- food_nutrient.csv: 食物营养数据
- food_category.csv: 食物分类

输出：
- foods.json: 统一格式的食材数据
"""

import csv
import json
import os
from pathlib import Path


def load_csv(file_path):
    """加载 CSV 文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def parse_usda_data(data_dir):
    """
    解析 USDA 数据

    参数：
        data_dir: USDA 数据目录

    返回：
        解析后的食物数据列表
    """
    print("=" * 50)
    print("开始解析 USDA 数据")
    print("=" * 50)

    # 加载数据文件
    print("\n[1/4] 加载食物基本信息...")
    food_file = os.path.join(data_dir, 'food.csv')
    foods = load_csv(food_file)
    print(f"  加载了 {len(foods)} 条食物记录")

    print("\n[2/4] 加载营养素定义...")
    nutrient_file = os.path.join(data_dir, 'nutrient.csv')
    nutrients = load_csv(nutrient_file)
    print(f"  加载了 {len(nutrients)} 种营养素")

    # 创建营养素 ID 到名称的映射
    nutrient_map = {}
    for n in nutrients:
        nutrient_map[n['id']] = {
            'name': n['name'],
            'unit': n['unit_name']
        }

    print("\n[3/4] 加载食物营养数据...")
    food_nutrient_file = os.path.join(data_dir, 'food_nutrient.csv')
    food_nutrients = load_csv(food_nutrient_file)
    print(f"  加载了 {len(food_nutrients)} 条营养数据")

    # 创建食物 ID 到营养数据的映射
    food_nutrient_map = {}
    for fn in food_nutrients:
        food_id = fn['fdc_id']
        nutrient_id = fn['nutrient_id']
        amount = fn['amount']

        if food_id not in food_nutrient_map:
            food_nutrient_map[food_id] = {}

        if nutrient_id in nutrient_map:
            nutrient_name = nutrient_map[nutrient_id]['name']
            food_nutrient_map[food_id][nutrient_name] = float(amount) if amount else 0.0

    print("\n[4/4] 加载食物分类...")
    category_file = os.path.join(data_dir, 'food_category.csv')
    categories = load_csv(category_file)
    print(f"  加载了 {len(categories)} 个分类")

    # 创建分类 ID 到名称的映射
    category_map = {}
    for c in categories:
        category_map[c['id']] = c['description']

    # 整合数据
    print("\n[5/5] 整合数据...")
    result = []
    for food in foods:
        food_id = food['fdc_id']
        description = food['description']
        category_id = food['food_category_id']

        # 获取分类名称
        category = category_map.get(category_id, 'Unknown')

        # 获取营养数据
        nutrition_data = food_nutrient_map.get(food_id, {})

        # 提取核心营养素
        protein = nutrition_data.get('Protein', 0.0)
        fat = nutrition_data.get('Total lipid (fat)', 0.0)
        carbs = nutrition_data.get('Carbohydrate, by difference', 0.0)
        calories = nutrition_data.get('Energy', 0.0)

        # 构建统一格式
        food_item = {
            'food_id': int(food_id),
            'name_en': description,
            'name_cn': '',  # 待翻译
            'category': category,
            'serving_size': 100,
            'serving_unit': 'g',
            'nutrition': {
                'protein': round(protein, 2),
                'fat': round(fat, 2),
                'carbs': round(carbs, 2),
                'calories': round(calories, 2)
            },
            'common_portions': [
                {'amount': 100, 'unit': 'g'}
            ],
            'tags': [],
            'source': 'USDA'
        }

        result.append(food_item)

    print(f"\n[OK] 解析完成，共 {len(result)} 条食物数据")
    return result


def save_to_json(data, output_file):
    """保存数据到 JSON 文件"""
    print(f"\n保存数据到: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] 保存成功")


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent

    # USDA 数据目录
    usda_dir = os.path.join(
        project_root,
        'data',
        'raw',
        'usda_sr_legacy',
        'FoodData_Central_sr_legacy_food_csv_2018-04'
    )

    # 输出文件
    output_dir = os.path.join(project_root, 'data', 'processed')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'foods.json')

    # 解析数据
    foods = parse_usda_data(usda_dir)

    # 保存数据
    save_to_json(foods, output_file)

    # 打印统计信息
    print("\n" + "=" * 50)
    print("数据统计")
    print("=" * 50)

    # 统计分类
    categories = {}
    for food in foods:
        cat = food['category']
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\n总食物数量: {len(foods)}")
    print(f"\n分类统计:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cat}: {count}")

    # 显示示例数据
    print("\n示例数据:")
    for food in foods[:3]:
        print(f"\n  {food['name_en']}")
        print(f"    分类: {food['category']}")
        print(f"    蛋白质: {food['nutrition']['protein']}g")
        print(f"    脂肪: {food['nutrition']['fat']}g")
        print(f"    碳水: {food['nutrition']['carbs']}g")
        print(f"    热量: {food['nutrition']['calories']}kcal")


if __name__ == '__main__':
    main()

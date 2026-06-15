# -*- coding: utf-8 -*-
"""
生成训练数据脚本

功能：
1. 读取清洗后的食材数据
2. 随机生成营养目标
3. 根据目标选择合适的食材组合
4. 生成自然语言描述

输入：
- foods_cleaned.json: 清洗后的食材数据

输出：
- train.json: 训练数据
- val.json: 验证数据
"""

import json
import os
import random
from pathlib import Path


def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, file_path):
    """保存 JSON 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def categorize_foods(foods):
    """
    将食物按分类分组

    返回：
        分类到食物列表的映射
    """
    categories = {}
    for food in foods:
        cat = food.get('category', 'Unknown')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(food)
    return categories


def select_foods_for_target(categories, target_protein, target_fat, target_carbs, max_foods=6):
    """
    根据营养目标选择食物组合

    参数：
        categories: 分类到食物列表的映射
        target_protein: 目标蛋白质（g）
        target_fat: 目标脂肪（g）
        target_carbs: 目标碳水（g）
        max_foods: 最大食物数量

    返回：
        选择的食物列表
    """
    selected_foods = []
    current_protein = 0
    current_fat = 0
    current_carbs = 0

    # 定义食物选择策略
    # 1. 先选择蛋白质来源（肉类、蛋类、豆类）
    protein_sources = []
    for cat in ['Beef Products', 'Poultry Products', 'Pork Products',
                'Lamb, Veal, and Game Products', 'Finfish and Shellfish Products',
                'Legumes and Legume Products', 'Egg Products']:
        if cat in categories:
            protein_sources.extend(categories[cat])

    # 2. 选择碳水来源（主食、谷物）
    carb_sources = []
    for cat in ['Cereal Grains and Pasta', 'Baked Products', 'Breakfast Cereals']:
        if cat in categories:
            carb_sources.extend(categories[cat])

    # 3. 选择蔬菜
    veg_sources = categories.get('Vegetables and Vegetable Products', [])

    # 4. 选择脂肪来源（坚果、油脂）
    fat_sources = []
    for cat in ['Nut and Seed Products', 'Fats and Oils']:
        if cat in categories:
            fat_sources.extend(categories[cat])

    # 选择蛋白质来源
    if protein_sources and target_protein > 0:
        food = random.choice(protein_sources)
        serving = min(300, max(100, int(target_protein / food['nutrition']['protein'] * 100))) if food['nutrition']['protein'] > 0 else 100
        selected_foods.append({
            'food': food,
            'serving': serving
        })
        current_protein += food['nutrition']['protein'] * serving / 100
        current_fat += food['nutrition']['fat'] * serving / 100
        current_carbs += food['nutrition']['carbs'] * serving / 100

    # 选择碳水来源
    if carb_sources and target_carbs > 0:
        food = random.choice(carb_sources)
        serving = min(400, max(100, int(target_carbs / food['nutrition']['carbs'] * 100))) if food['nutrition']['carbs'] > 0 else 100
        selected_foods.append({
            'food': food,
            'serving': serving
        })
        current_protein += food['nutrition']['protein'] * serving / 100
        current_fat += food['nutrition']['fat'] * serving / 100
        current_carbs += food['nutrition']['carbs'] * serving / 100

    # 选择蔬菜
    if veg_sources:
        food = random.choice(veg_sources)
        serving = random.choice([100, 150, 200])
        selected_foods.append({
            'food': food,
            'serving': serving
        })
        current_protein += food['nutrition']['protein'] * serving / 100
        current_fat += food['nutrition']['fat'] * serving / 100
        current_carbs += food['nutrition']['carbs'] * serving / 100

    # 如果还差蛋白质，再选一个蛋白质来源
    if current_protein < target_protein * 0.7 and protein_sources:
        food = random.choice(protein_sources)
        serving = min(200, max(100, int((target_protein - current_protein) / food['nutrition']['protein'] * 100))) if food['nutrition']['protein'] > 0 else 100
        selected_foods.append({
            'food': food,
            'serving': serving
        })
        current_protein += food['nutrition']['protein'] * serving / 100
        current_fat += food['nutrition']['fat'] * serving / 100
        current_carbs += food['nutrition']['carbs'] * serving / 100

    # 如果还差碳水，再选一个碳水来源
    if current_carbs < target_carbs * 0.7 and carb_sources:
        food = random.choice(carb_sources)
        serving = min(300, max(100, int((target_carbs - current_carbs) / food['nutrition']['carbs'] * 100))) if food['nutrition']['carbs'] > 0 else 100
        selected_foods.append({
            'food': food,
            'serving': serving
        })
        current_protein += food['nutrition']['protein'] * serving / 100
        current_fat += food['nutrition']['fat'] * serving / 100
        current_carbs += food['nutrition']['carbs'] * serving / 100

    # 如果还差脂肪，再选一个脂肪来源
    if current_fat < target_fat * 0.7 and fat_sources:
        food = random.choice(fat_sources)
        serving = min(100, max(50, int((target_fat - current_fat) / food['nutrition']['fat'] * 100))) if food['nutrition']['fat'] > 0 else 50
        selected_foods.append({
            'food': food,
            'serving': serving
        })
        current_protein += food['nutrition']['protein'] * serving / 100
        current_fat += food['nutrition']['fat'] * serving / 100
        current_carbs += food['nutrition']['carbs'] * serving / 100

    # 限制食物数量
    if len(selected_foods) > max_foods:
        selected_foods = selected_foods[:max_foods]

    return selected_foods


def format_output(selected_foods):
    """
    格式化输出

    参数：
        selected_foods: 选择的食物列表

    返回：
        格式化的字符串
    """
    lines = ["推荐食材："]
    for i, item in enumerate(selected_foods, 1):
        food = item['food']
        serving = item['serving']
        protein = food['nutrition']['protein'] * serving / 100
        fat = food['nutrition']['fat'] * serving / 100
        carbs = food['nutrition']['carbs'] * serving / 100

        lines.append(f"{i}. {food['name_en']} {serving}g（蛋白质{protein:.1f}g，脂肪{fat:.1f}g，碳水{carbs:.1f}g）")

    return "\n".join(lines)


def generate_training_data(foods, num_samples=500):
    """
    生成训练数据

    参数：
        foods: 食物数据列表
        num_samples: 生成样本数量

    返回：
        训练数据列表
    """
    print("=" * 50)
    print("开始生成训练数据")
    print("=" * 50)

    # 按分类分组
    categories = categorize_foods(foods)
    print(f"\n食物分类数: {len(categories)}")

    training_data = []

    print(f"\n生成 {num_samples} 条训练数据...")
    for i in range(num_samples):
        # 随机生成营养目标
        # 常见的营养目标范围
        target_protein = random.randint(30, 200)  # 30-200g
        target_fat = random.randint(20, 100)  # 20-100g
        target_carbs = random.randint(100, 400)  # 100-400g

        # 选择食物
        selected_foods = select_foods_for_target(
            categories,
            target_protein,
            target_fat,
            target_carbs
        )

        # 生成输入
        input_text = f"蛋白质{target_protein}g，脂肪{target_fat}g，碳水{target_carbs}g"

        # 生成输出
        output_text = format_output(selected_foods)

        training_data.append({
            'input': input_text,
            'output': output_text
        })

        if (i + 1) % 100 == 0:
            print(f"  已生成 {i + 1} 条")

    print(f"[OK] 生成完成，共 {len(training_data)} 条")
    return training_data


def split_data(data, train_ratio=0.8):
    """
    划分训练集和验证集

    参数：
        data: 数据列表
        train_ratio: 训练集比例

    返回：
        train_data, val_data
    """
    random.shuffle(data)
    split_idx = int(len(data) * train_ratio)
    return data[:split_idx], data[split_idx:]


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent

    # 输入文件
    input_file = os.path.join(project_root, 'data', 'processed', 'foods_cleaned.json')

    # 输出文件
    train_file = os.path.join(project_root, 'data', 'processed', 'train.json')
    val_file = os.path.join(project_root, 'data', 'processed', 'val.json')

    # 加载数据
    print(f"加载数据: {input_file}")
    foods = load_json(input_file)
    print(f"加载了 {len(foods)} 条食物数据")

    # 生成训练数据
    training_data = generate_training_data(foods, num_samples=600)

    # 划分训练集和验证集
    print("\n划分训练集和验证集...")
    train_data, val_data = split_data(training_data, train_ratio=0.8)
    print(f"  训练集: {len(train_data)} 条")
    print(f"  验证集: {len(val_data)} 条")

    # 保存数据
    print(f"\n保存训练集: {train_file}")
    save_json(train_data, train_file)
    print(f"[OK] 保存成功")

    print(f"\n保存验证集: {val_file}")
    save_json(val_data, val_file)
    print(f"[OK] 保存成功")

    # 显示示例数据
    print("\n" + "=" * 50)
    print("示例数据")
    print("=" * 50)
    for i, sample in enumerate(train_data[:3], 1):
        print(f"\n样本 {i}:")
        print(f"  输入: {sample['input']}")
        print(f"  输出:")
        for line in sample['output'].split('\n'):
            print(f"    {line}")


if __name__ == '__main__':
    main()

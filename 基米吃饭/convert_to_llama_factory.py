# -*- coding: utf-8 -*-
"""
数据格式转换脚本

功能：
将 train.json 转换为 LLaMA-Factory 支持的格式

输入：
- data/processed/train.json

输出：
- data/processed/train_llama.json
- data/processed/val_llama.json
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


def convert_to_llama_format(data):
    """
    转换为 LLaMA-Factory 格式

    输入格式：
    {
        "input": "蛋白质150g，脂肪60g，碳水200g",
        "output": "推荐食材：..."
    }

    输出格式：
    {
        "instruction": "你是一个营养师，根据用户的营养目标推荐食材搭配。",
        "input": "蛋白质150g，脂肪60g，碳水200g",
        "output": "推荐食材：..."
    }
    """
    instruction = "你是一个专业的营养师，根据用户提供的营养目标（蛋白质、脂肪、碳水），推荐合适的食材搭配。请给出具体的食材名称和用量。"

    llama_data = []
    for item in data:
        llama_data.append({
            'instruction': instruction,
            'input': item['input'],
            'output': item['output']
        })

    return llama_data


def create_dataset_info(project_root):
    """
    创建 dataset_info.json 文件

    LLaMA-Factory 需要这个文件来定义数据集格式
    """
    dataset_info = {
        "train_llama": {
            "file_name": "train_llama.json",
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output"
            }
        },
        "val_llama": {
            "file_name": "val_llama.json",
            "columns": {
                "prompt": "instruction",
                "query": "input",
                "response": "output"
            }
        }
    }

    output_file = os.path.join(project_root, 'data', 'processed', 'dataset_info.json')
    save_json(dataset_info, output_file)
    print(f"\n创建 dataset_info.json: {output_file}")
    print(f"[OK] 保存成功")


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent

    # 输入文件
    train_file = os.path.join(project_root, 'data', 'processed', 'train.json')
    val_file = os.path.join(project_root, 'data', 'processed', 'val.json')

    # 输出文件
    train_llama_file = os.path.join(project_root, 'data', 'processed', 'train_llama.json')
    val_llama_file = os.path.join(project_root, 'data', 'processed', 'val_llama.json')

    # 转换训练数据
    print("=" * 50)
    print("转换训练数据格式")
    print("=" * 50)

    print(f"\n加载训练数据: {train_file}")
    train_data = load_json(train_file)
    print(f"加载了 {len(train_data)} 条数据")

    print(f"\n转换格式...")
    train_llama = convert_to_llama_format(train_data)
    print(f"转换完成")

    print(f"\n保存到: {train_llama_file}")
    save_json(train_llama, train_llama_file)
    print(f"[OK] 保存成功")

    # 转换验证数据
    print(f"\n加载验证数据: {val_file}")
    val_data = load_json(val_file)
    print(f"加载了 {len(val_data)} 条数据")

    print(f"\n转换格式...")
    val_llama = convert_to_llama_format(val_data)
    print(f"转换完成")

    print(f"\n保存到: {val_llama_file}")
    save_json(val_llama, val_llama_file)
    print(f"[OK] 保存成功")

    # 创建 dataset_info.json
    print("\n" + "=" * 50)
    print("创建 dataset_info.json")
    print("=" * 50)
    create_dataset_info(project_root)

    # 显示示例
    print("\n" + "=" * 50)
    print("示例数据")
    print("=" * 50)
    print(f"\n指令: {train_llama[0]['instruction'][:50]}...")
    print(f"输入: {train_llama[0]['input']}")
    print(f"输出: {train_llama[0]['output'][:100]}...")

    print("\n" + "=" * 50)
    print("转换完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()

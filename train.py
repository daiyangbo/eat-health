# -*- coding: utf-8 -*-
"""
训练脚本

功能：
封装完整的训练流程，一键运行

使用方法：
python train.py

步骤：
1. 转换数据格式
2. 下载模型（如果不存在）
3. 执行训练
4. 测试模型
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """运行命令"""
    print(f"\n执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=False)
    if result.returncode != 0:
        print(f"命令执行失败，退出码: {result.returncode}")
        sys.exit(1)
    return result


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent

    print("=" * 60)
    print("基米吃饭 - 模型训练脚本")
    print("=" * 60)

    # 步骤 1: 转换数据格式
    print("\n" + "=" * 60)
    print("步骤 1: 转换数据格式")
    print("=" * 60)
    run_command("python convert_to_llama_factory.py", cwd=project_root)

    # 步骤 2: 检查模型是否存在
    model_path = project_root / "models" / "base" / "qwen2.5-1.5b"
    if not model_path.exists():
        print("\n" + "=" * 60)
        print("步骤 2: 下载模型")
        print("=" * 60)
        run_command("python download_model.py", cwd=project_root)
    else:
        print(f"\n模型已存在: {model_path}")
        print("跳过下载步骤")

    # 步骤 3: 检查 LLaMA-Factory 是否安装
    llama_factory_path = project_root / "LLaMA-Factory"
    if not llama_factory_path.exists():
        print("\n" + "=" * 60)
        print("步骤 3: 安装 LLaMA-Factory")
        print("=" * 60)
        run_command("git clone https://github.com/hiyouga/LLaMA-Factory.git", cwd=project_root)
        run_command("pip install -e .", cwd=llama_factory_path)
    else:
        print(f"\nLLaMA-Factory 已存在: {llama_factory_path}")
        print("跳过安装步骤")

    # 步骤 4: 执行训练
    print("\n" + "=" * 60)
    print("步骤 4: 执行训练")
    print("=" * 60)
    config_path = project_root / "train_config.yaml"
    run_command(f"llamafactory-cli train {config_path}", cwd=llama_factory_path)

    # 步骤 5: 测试模型
    print("\n" + "=" * 60)
    print("步骤 5: 测试模型")
    print("=" * 60)
    run_command("python test_model.py", cwd=project_root)

    print("\n" + "=" * 60)
    print("训练完成！")
    print("=" * 60)
    print(f"\n训练后的模型保存在: {project_root / 'models' / 'finetuned'}")
    print("可以下载到本地使用了！")


if __name__ == '__main__':
    main()

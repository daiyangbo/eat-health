# -*- coding: utf-8 -*-
"""
模型下载脚本

功能：
下载 Qwen2.5-1.5B 模型到本地

使用方法：
python download_model.py

说明：
- 首次运行需要下载模型，请确保网络连接正常
- 国内用户建议设置 HuggingFace 镜像
  export HF_ENDPOINT=https://hf-mirror.com
"""

import os
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM


def download_with_retry(func, *args, max_retries=3, **kwargs):
    """
    带重试的下载函数

    参数：
        func: 下载函数
        max_retries: 最大重试次数
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  下载失败，重试 {attempt + 1}/{max_retries}...")
                print(f"  错误: {str(e)}")
                import time
                time.sleep(5)  # 等待 5 秒后重试
            else:
                print(f"  下载失败，已达到最大重试次数")
                print(f"  错误: {str(e)}")
                print("\n建议：")
                print("1. 检查网络连接")
                print("2. 设置 HuggingFace 镜像：export HF_ENDPOINT=https://hf-mirror.com")
                print("3. 使用代理")
                sys.exit(1)


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent

    # 模型保存路径
    save_path = os.path.join(project_root, 'models', 'base', 'qwen2.5-1.5b')

    # 模型名称
    model_name = "Qwen/Qwen2.5-1.5B"

    print("=" * 50)
    print("下载 Qwen2.5-1.5B 模型")
    print("=" * 50)

    # 检查是否已下载
    if os.path.exists(save_path) and os.path.exists(os.path.join(save_path, "config.json")):
        print(f"\n模型已存在: {save_path}")
        print("跳过下载步骤")
        return

    # 创建目录
    os.makedirs(save_path, exist_ok=True)

    # 下载 tokenizer
    print(f"\n[1/2] 下载 Tokenizer...")
    print(f"  模型: {model_name}")
    print(f"  保存到: {save_path}")
    tokenizer = download_with_retry(AutoTokenizer.from_pretrained, model_name)
    tokenizer.save_pretrained(save_path)
    print(f"[OK] Tokenizer 下载完成")

    # 下载模型
    print(f"\n[2/2] 下载模型...")
    print(f"  模型: {model_name}")
    print(f"  保存到: {save_path}")
    model = download_with_retry(AutoModelForCausalLM.from_pretrained, model_name)
    model.save_pretrained(save_path)
    print(f"[OK] 模型下载完成")

    # 显示模型信息
    print("\n" + "=" * 50)
    print("模型信息")
    print("=" * 50)
    print(f"\n模型名称: {model_name}")
    print(f"保存路径: {save_path}")
    print(f"模型类型: {model.config.model_type}")
    print(f"词汇表大小: {model.config.vocab_size}")
    print(f"隐藏层大小: {model.config.hidden_size}")
    print(f"注意力头数: {model.config.num_attention_heads}")
    print(f"隐藏层数: {model.config.num_hidden_layers}")

    # 计算模型参数量
    total_params = sum(p.numel() for p in model.parameters())
    print(f"总参数量: {total_params / 1e6:.2f}M")

    print("\n" + "=" * 50)
    print("下载完成！")
    print("=" * 50)
    print(f"\n模型已保存到: {save_path}")
    print("可以开始训练了！")


if __name__ == '__main__':
    main()

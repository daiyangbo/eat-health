# -*- coding: utf-8 -*-
"""
模型测试脚本

功能：
测试训练后的模型效果

使用方法：
python test_model.py

说明：
- 加载训练后的模型
- 使用测试用例进行推理
- 显示生成结果
"""

import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def load_model(model_path):
    """加载模型"""
    print(f"加载模型: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    print("[OK] 模型加载成功")
    return tokenizer, model


def generate_response(tokenizer, model, instruction, input_text, max_length=512):
    """
    生成回答

    参数：
        tokenizer: 分词器
        model: 模型
        instruction: 指令
        input_text: 输入文本
        max_length: 最大生成长度

    返回：
        生成的文本
    """
    # 构建 prompt (LLaMA-Factory Qwen 模板格式)
    messages = [
        {"role": "system", "content": instruction},
        {"role": "user", "content": input_text}
    ]

    # 使用 tokenizer 的 apply_chat_template 方法
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # 编码
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # 生成（优化参数，防止重复生成）
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,          # 最大生成长度
            temperature=0.3,             # 降低温度，减少随机性（原0.7）
            do_sample=True,              # 启用采样
            top_p=0.85,                  # 核采样（原0.9）
            top_k=40,                    # Top-K采样（原50）
            repetition_penalty=1.3,      # 增加重复惩罚（原1.1）
            no_repeat_ngram_size=3,      # 禁止3-gram重复
            early_stopping=True          # 早停
        )

    # 解码（只取新生成的部分）
    result = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

    return result


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent

    # 模型路径
    model_path = project_root / "models" / "finetuned"

    # 检查模型是否存在
    if not model_path.exists():
        print(f"错误：模型不存在: {model_path}")
        print("请先运行训练脚本: python train.py")
        return

    print("=" * 60)
    print("基米吃饭 - 模型测试")
    print("=" * 60)

    # 加载模型
    tokenizer, model = load_model(model_path)

    # 测试用例（优化提示词格式）
    test_cases = [
        {
            "instruction": "你是一个专业的营养师，专门为学校食堂设计营养餐。请根据用户提供的营养目标，推荐具体的食材搭配和用量。要求：1）推荐3-5种主要食材；2）每种食材给出具体克数；3）确保营养目标大致达标。",
            "input": "请帮我搭配一餐，营养目标：蛋白质150g，脂肪60g，碳水化合物200g"
        },
        {
            "instruction": "你是一个专业的营养师，专门为学校食堂设计营养餐。请根据用户提供的营养目标，推荐具体的食材搭配和用量。要求：1）推荐3-5种主要食材；2）每种食材给出具体克数；3）确保营养目标大致达标。",
            "input": "请帮我搭配一餐，营养目标：蛋白质100g，脂肪40g，碳水化合物150g"
        },
        {
            "instruction": "你是一个专业的营养师，专门为学校食堂设计营养餐。请根据用户提供的营养目标，推荐具体的食材搭配和用量。要求：1）推荐3-5种主要食材；2）每种食材给出具体克数；3）确保营养目标大致达标。",
            "input": "请帮我搭配一餐，营养目标：蛋白质200g，脂肪80g，碳水化合物300g"
        }
    ]

    # 测试每个用例
    print("\n" + "=" * 60)
    print("测试结果")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"  输入: {test_case['input']}")

        # 生成回答
        response = generate_response(
            tokenizer,
            model,
            test_case['instruction'],
            test_case['input']
        )

        print(f"  输出:")
        # 格式化输出
        for line in response.split('\n'):
            if line.strip():
                print(f"    {line}")

        print("-" * 60)

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()

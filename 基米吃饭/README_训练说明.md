# 基米吃饭 - 训练说明文档

> **创建日期**：2026-06-14
> **用途**：AutoDL 训练完整指南

---

## 📁 文件清单

### 必须上传的文件

| 文件 | 用途 | 大小 |
|------|------|------|
| `data/processed/train.json` | 训练数据 | ~500KB |
| `data/processed/val.json` | 验证数据 | ~100KB |
| `data/processed/foods_cleaned.json` | 食材数据 | ~2MB |
| `convert_to_llama_factory.py` | 数据格式转换脚本 | ~3KB |
| `train_config.yaml` | 训练配置文件 | ~1KB |
| `train.py` | 一键训练脚本 | ~3KB |
| `download_model.py` | 模型下载脚本 | ~2KB |
| `test_model.py` | 模型测试脚本 | ~3KB |
| `requirements.txt` | 依赖包列表 | ~1KB |

### 可选文件

| 文件 | 用途 | 说明 |
|------|------|------|
| `src/` | 源代码 | 包含数据处理和 RAG 代码 |
| `docs/` | 文档 | 包含流程图等 |

---

## 🚀 快速开始

### 第一步：上传文件

将上述文件上传到 AutoDL 实例的 `/root/基米吃饭/` 目录。

### 第二步：安装依赖

```bash
cd /root/基米吃饭
pip install -r requirements.txt
```

### 第三步：设置 HuggingFace 镜像

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

### 第四步：一键训练

```bash
python train.py
```

**train.py 会自动执行以下步骤**：
1. 转换数据格式
2. 下载模型（如果不存在）
3. 安装 LLaMA-Factory（如果不存在）
4. 执行训练
5. 测试模型

---

## 📋 手动执行步骤

如果你想手动执行每个步骤，可以按以下顺序：

### 1. 转换数据格式

```bash
python convert_to_llama_factory.py
```

**输入**：
- `data/processed/train.json`
- `data/processed/val.json`

**输出**：
- `data/processed/train_llama.json`
- `data/processed/val_llama.json`

---

### 2. 下载模型

```bash
python download_model.py
```

**下载内容**：
- Qwen3-8B 模型
- 保存到 `models/base/qwen3-8b/`

**注意事项**：
- 首次运行需要下载约 16GB 模型
- 建议设置 HuggingFace 镜像加速

---

### 3. 安装 LLaMA-Factory

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e .
```

---

### 4. 执行训练

```bash
cd LLaMA-Factory
llamafactory-cli train ../train_config.yaml
```

**训练参数**：
- 模型：Qwen3-8B
- 训练轮数：3 epochs
- 批次大小：4 × 4 = 16
- 学习率：2e-6
- 预计时间：2-3 小时

---

### 5. 测试模型

```bash
python test_model.py
```

**测试内容**：
- 加载训练后的模型
- 使用测试用例进行推理
- 显示生成结果

---

## ⚙️ 训练配置说明

### train_config.yaml 参数说明

```yaml
# 模型配置
model_name_or_path: ./models/base/qwen3-8b  # 模型路径（Qwen3-8B）

# 数据配置
dataset_dir: ./data/processed  # 数据目录
dataset: train_llama  # 数据集名称
template: qwen  # 模板类型
finetuning_type: lora  # 微调类型（LoRA微调）

# LoRA配置
lora_rank: 16  # LoRA秩
lora_alpha: 32  # LoRA缩放因子
lora_target: all  # LoRA目标模块

# 输出配置
output_dir: ./models/finetuned  # 输出目录
logging_dir: ./logs  # 日志目录

# 训练参数
per_device_train_batch_size: 4  # 每个设备的批次大小
gradient_accumulation_steps: 4  # 梯度累积步数
num_train_epochs: 3  # 训练轮数
learning_rate: 2.0e-6  # 学习率（8B模型使用较小的学习率）
lr_scheduler_type: cosine  # 学习率调度器
warmup_steps: 300  # 预热步数（8B模型需要更多预热）
weight_decay: 0.01  # 权重衰减

# 保存配置
save_steps: 500  # 保存步数
save_total_limit: 2  # 最多保存 2 个 checkpoint
save_strategy: steps  # 保存策略

# 日志配置
logging_steps: 10  # 日志步数
report_to: none  # 不上报到 wandb

# 精度配置
bf16: true  # 使用 bfloat16 精度

# 其他配置
seed: 42  # 随机种子
dataloader_num_workers: 4  # 数据加载线程数
remove_unused_columns: false  # 不删除未使用的列
```

---

## 📊 训练监控

### 查看训练日志

```bash
# 查看实时日志
tail -f logs/training.log

# 查看 GPU 使用情况
nvidia-smi
```

### 训练指标

| 指标 | 说明 | 理想状态 |
|------|------|----------|
| **Loss** | 损失值 | 逐渐下降，趋于稳定 |
| **Learning Rate** | 学习率 | 按计划衰减 |
| **Gradient Norm** | 梯度范数 | 保持稳定，不爆炸 |

---

## 🧪 测试用例

### 测试用例 1

**输入**：
```
蛋白质150g，脂肪60g，碳水200g
```

**预期输出**：
```
推荐食材：
1. 鸡胸肉 200g（蛋白质40g，脂肪4g）
2. 鸡蛋 3个（蛋白质18g，脂肪15g）
3. 米饭 300g（碳水78g）
4. 西兰花 150g（蛋白质4g，碳水10g）
...
```

### 测试用例 2

**输入**：
```
蛋白质100g，脂肪40g，碳水150g
```

**预期输出**：
```
推荐食材：
1. 牛肉 150g（蛋白质30g，脂肪15g）
2. 糙米 200g（碳水150g）
3. 菠菜 100g（蛋白质3g，脂肪0.5g）
...
```

---

## 💾 模型下载

### 打包模型

```bash
cd /root/基米吃饭/models/finetuned
tar -czvf ../../finetuned_model.tar.gz .
```

### 下载到本地

```bash
# 使用 SCP 下载
scp -P <端口号> root@<地址>:/root/基米吃饭/finetuned_model.tar.gz .
```

---

## ⚠️ 常见问题

### 1. CUDA 内存不足

**错误**：`RuntimeError: CUDA out of memory`

**解决方案**：
- 减小 `per_device_train_batch_size`（改为 2 或 1）
- 增加 `gradient_accumulation_steps`（改为 8 或 16）
- 使用梯度检查点：`gradient_checkpointing: true`

### 2. 模型下载失败

**错误**：`ConnectionError` 或 `TimeoutError`

**解决方案**：
- 设置 HuggingFace 镜像：`export HF_ENDPOINT=https://hf-mirror.com`
- 使用代理
- 手动下载模型并上传

### 3. 训练速度慢

**原因**：
- GPU 性能不足
- 数据加载瓶颈

**解决方案**：
- 使用更强大的 GPU（如 A100）
- 增加 `dataloader_num_workers`
- 使用混合精度训练（已启用 bf16）

---

## 📞 获取帮助

如果遇到问题，可以：

1. 查看 AutoDL 官方文档：https://www.autodl.com/docs/
2. 查看 LLaMA-Factory 文档：https://github.com/hiyouga/LLaMA-Factory
3. 查看 Qwen3 模型文档：https://huggingface.co/Qwen/Qwen3-8B

---

## 📝 训练记录

| 项目 | 值 |
|------|-----|
| **训练日期** | |
| **GPU 型号** | RTX 4090 |
| **训练时长** | 约 2-3 小时 |
| **最终 Loss** | |
| **模型大小** | 约 16GB |

---

**文档结束**

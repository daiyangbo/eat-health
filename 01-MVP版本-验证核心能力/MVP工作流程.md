# 基米吃饭 - MVP 开发工作流程

> **目标**：验证 LLM + RAG 核心能力
> **输入**：蛋白质、脂肪、碳水克数
> **输出**：食材推荐（通用食材，非食堂菜品）
> **预计时间**：2周

---

## 总体流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    第一阶段：环境搭建（第1天）                  │
│  安装Python → 安装依赖包 → 配置VSCode → 测试环境              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    第二阶段：数据准备（第2-4天）                │
│  收集数据 → 清洗数据 → 生成训练数据 → 搭建RAG知识库            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    第三阶段：模型训练（第5-7天）                │
│  配置AutoDL → 下载模型 → 编写训练脚本 → 执行训练 → 评估       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    第四阶段：RAG集成（第8-10天）                │
│  搭建ChromaDB → 实现Embedding → 集成LLM → 命令行交互          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    第五阶段：测试优化（第11-14天）              │
│  功能测试 → 效果评估 → 优化调整 → 编写文档                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 第一阶段：环境搭建

### 时间：第1天

### 任务清单

| 序号 | 任务 | 具体操作 | 验收标准 | 预计时间 |
|------|------|----------|----------|----------|
| 1.1 | 安装Python | 下载安装Python 3.10+ | `python --version` 显示版本 | 30分钟 |
| 1.2 | 安装VSCode插件 | Python、Jupyter、Git | 插件正常加载 | 15分钟 |
| 1.3 | 创建项目目录 | 创建项目文件夹结构 | 目录结构正确 | 15分钟 |
| 1.4 | 创建虚拟环境 | `python -m venv venv` | 激活成功 | 10分钟 |
| 1.5 | 安装基础依赖 | `pip install -r requirements.txt` | 无报错 | 30分钟 |
| 1.6 | 测试环境 | 运行测试脚本 | 输出正常 | 15分钟 |

### 项目目录结构

```
基米吃饭/
├── data/                    # 数据目录
│   ├── raw/                 # 原始数据
│   ├── processed/           # 处理后的数据
│   └── knowledge_base/      # RAG知识库
├── models/                  # 模型目录
│   ├── base/                # 基座模型
│   └── finetuned/           # 微调后的模型
├── src/                     # 源代码
│   ├── data_processing/     # 数据处理
│   ├── training/            # 模型训练
│   ├── rag/                 # RAG系统
│   └── utils/               # 工具函数
├── tests/                   # 测试代码
├── docs/                    # 文档
├── requirements.txt         # 依赖包列表
├── config.yaml              # 配置文件
└── main.py                  # 主程序入口
```

### requirements.txt 内容

```
# 基础依赖
python>=3.10
torch>=2.0.0
transformers>=4.35.0
datasets>=2.14.0
accelerate>=0.24.0

# RAG相关
langchain>=0.1.0
chromadb>=0.4.0
sentence-transformers>=2.2.0

# 数据处理
pandas>=2.0.0
numpy>=1.24.0
json5>=0.9.0

# 工具
tqdm>=4.65.0
pyyaml>=6.0
python-dotenv>=1.0.0

# 开发工具
ipython>=8.0.0
jupyter>=1.0.0
```

---

## 第二阶段：数据准备

### 时间：第2-4天

### 任务清单

| 序号 | 任务 | 具体操作 | 验收标准 | 预计时间 |
|------|------|----------|----------|----------|
| 2.1 | 收集中国食物成分表 | 下载公开数据集 | 获得CSV/JSON格式数据 | 2小时 |
| 2.2 | 收集USDA营养数据 | 下载USDA数据库 | 获得CSV/JSON格式数据 | 2小时 |
| 2.3 | 数据清洗 | 去重、补全、格式统一 | 数据无重复、无空值 | 3小时 |
| 2.4 | 数据格式化 | 转换为统一JSON格式 | 格式符合要求 | 2小时 |
| 2.5 | 生成训练数据 | 生成输入-输出对 | 至少500条训练数据 | 4小时 |
| 2.6 | 搭建RAG知识库 | 向量化食材数据 | ChromaDB可查询 | 3小时 |

### 数据收集来源

#### 中国食物成分表
- **来源**：中国营养学会官方数据
- **内容**：中式食材营养数据
- **格式**：CSV或Excel
- **获取方式**：公开下载或购买

#### USDA食品数据库
- **来源**：美国农业部
- **内容**：国际食材营养数据
- **格式**：CSV
- **获取方式**：https://fdc.nal.usda.gov/download-datasets

### 数据清洗流程

```
原始数据
    │
    ▼
┌─────────────┐
│ 去重        │ 删除重复的食材记录
└─────────────┘
    │
    ▼
┌─────────────┐
│ 补全        │ 填充缺失的营养字段
└─────────────┘
    │
    ▼
┌─────────────┐
│ 格式统一    │ 统一单位、字段名
└─────────────┘
    │
    ▼
┌─────────────┐
│ 验证        │ 检查数据合理性
└─────────────┘
    │
    ▼
清洗后的数据
```

### 数据格式规范

#### 食材数据格式

```json
{
  "food_id": 1,
  "name": "鸡胸肉",
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
  "tags": ["高蛋白", "低脂", "肉类"]
}
```

#### 训练数据格式

```json
{
  "input": "蛋白质150g，脂肪60g，碳水200g",
  "output": "推荐食材：\n1. 鸡胸肉 200g（蛋白质40g，脂肪4g）\n2. 鸡蛋 3个（蛋白质18g，脂肪15g）\n3. 米饭 300g（碳水78g）\n4. 西兰花 150g（蛋白质4g，碳水10g）\n5. 牛肉 150g（蛋白质30g，脂肪15g）\n6. 糙米 200g（碳水150g）"
}
```

### RAG知识库搭建流程

```
食材数据
    │
    ▼
┌─────────────┐
│ 文本向量化  │ 使用 text2vec-chinese 将食材信息转为向量
└─────────────┘
    │
    ▼
┌─────────────┐
│ 存入ChromaDB│ 将向量和元数据存入向量数据库
└─────────────┘
    │
    ▼
┌─────────────┐
│ 测试查询    │ 测试检索效果
└─────────────┘
    │
    ▼
RAG知识库就绪
```

---

## 第三阶段：模型训练

### 时间：第5-7天

### 任务清单

| 序号 | 任务 | 具体操作 | 验收标准 | 预计时间 |
|------|------|----------|----------|----------|
| 3.1 | 注册AutoDL | 注册账号、充值 | 账号可用 | 30分钟 |
| 3.2 | 创建实例 | 选择RTX 3090、PyTorch镜像 | 实例创建成功 | 15分钟 |
| 3.3 | 上传数据 | 上传训练数据和代码 | 文件完整 | 30分钟 |
| 3.4 | 下载模型 | 下载Qwen2.5-1.5B | 模型文件完整 | 1小时 |
| 3.5 | 安装依赖 | 安装LLaMA-Factory等 | 无报错 | 30分钟 |
| 3.6 | 编写训练脚本 | 配置训练参数 | 脚本可运行 | 2小时 |
| 3.7 | 执行训练 | 运行SFT微调 | 训练完成无报错 | 3小时 |
| 3.8 | 评估模型 | 测试模型效果 | 输出符合预期 | 2小时 |

### AutoDL配置

```
实例配置：
- GPU：RTX 3090（24GB显存）
- 镜像：PyTorch 2.1 + CUDA 11.8 + Python 3.10
- 存储：50GB

费用估算：
- GPU：¥1.5/小时
- 存储：¥0.01/GB/小时
- 预计使用：20小时
- 预计费用：¥40左右
```

### 训练参数配置

```yaml
# config.yaml

model:
  name: "Qwen/Qwen2.5-1.5B"
  torch_dtype: "bfloat16"
  device_map: "auto"

training:
  output_dir: "./checkpoints"
  num_train_epochs: 3
  per_device_train_batch_size: 4
  gradient_accumulation_steps: 4
  learning_rate: 1.0e-5
  lr_scheduler_type: "cosine"
  warmup_steps: 100
  save_steps: 500
  save_total_limit: 2
  bf16: true
  logging_steps: 10

data:
  train_file: "./data/processed/train.json"
  max_length: 512
```

### 训练流程

```
Step 1: 准备环境
├── 登录AutoDL
├── 创建实例
├── 上传代码和数据
└── 安装依赖

Step 2: 下载模型
├── 设置HuggingFace镜像
├── 下载Qwen2.5-1.5B
└── 验证模型文件

Step 3: 配置训练
├── 编写config.yaml
├── 编写训练脚本
└── 测试数据加载

Step 4: 执行训练
├── 运行训练脚本
├── 监控训练过程
└── 保存checkpoint

Step 5: 评估模型
├── 加载训练后的模型
├── 测试输入输出
└── 评估效果
```

### 训练脚本示例

```python
# train.py

from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# 加载模型和tokenizer
model_name = "Qwen/Qwen2.5-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)

# 加载数据集
dataset = load_dataset("json", data_files="./data/processed/train.json")

# 数据预处理
def preprocess(examples):
    inputs = tokenizer(examples["input"], truncation=True, max_length=256)
    outputs = tokenizer(examples["output"], truncation=True, max_length=256)
    inputs["labels"] = outputs["input_ids"]
    return inputs

tokenized_dataset = dataset.map(preprocess, batched=True)

# 训练参数
training_args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=1e-5,
    lr_scheduler_type="cosine",
    warmup_steps=100,
    save_steps=500,
    save_total_limit=2,
    bf16=True,
    logging_steps=10,
)

# 创建Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# 开始训练
trainer.train()

# 保存模型
trainer.save_model("./checkpoints/final")
```

---

## 第四阶段：RAG集成

### 时间：第8-10天

### 任务清单

| 序号 | 任务 | 具体操作 | 验收标准 | 预计时间 |
|------|------|----------|----------|----------|
| 4.1 | 搭建ChromaDB | 安装、初始化向量数据库 | 数据库可连接 | 1小时 |
| 4.2 | 实现Embedding | 加载text2vec模型 | 向量化正常 | 2小时 |
| 4.3 | 实现RAG检索 | 编写检索函数 | 检索结果正确 | 3小时 |
| 4.4 | 集成LLM推理 | 加载训练后的模型 | 推理正常 | 2小时 |
| 4.5 | 实现命令行交互 | 编写main.py | 交互流程顺畅 | 3小时 |
| 4.6 | 实现结果格式化 | 表格输出 | 格式美观 | 2小时 |

### RAG架构

```
用户输入（营养目标）
    │
    ▼
┌─────────────┐
│ RAG检索     │ 从ChromaDB中检索匹配的食材
└─────────────┘
    │
    ▼
┌─────────────┐
│ 构建Prompt  │ 将检索结果和用户输入组合成prompt
└─────────────┘
    │
    ▼
┌─────────────┐
│ LLM推理     │ 使用训练后的模型生成推荐
└─────────────┘
    │
    ▼
┌─────────────┐
│ 结果格式化  │ 将输出格式化为表格
└─────────────┘
    │
    ▼
展示给用户
```

### RAG检索实现

```python
# src/rag/retriever.py

import chromadb
from sentence_transformers import SentenceTransformer

class NutritionRetriever:
    def __init__(self, db_path="./data/knowledge_base"):
        # 初始化ChromaDB
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_collection("foods")
        
        # 初始化Embedding模型
        self.embedding_model = SentenceTransformer("shibing624/text2vec-chinese")
    
    def retrieve(self, query, n_results=10):
        """
        检索匹配的食材
        
        参数：
            query: 用户查询（如"高蛋白低脂食材"）
            n_results: 返回结果数量
        
        返回：
            匹配的食材列表
        """
        # 向量化查询
        query_embedding = self.embedding_model.encode(query)
        
        # 检索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
```

### LLM推理实现

```python
# src/rag/generator.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class NutritionGenerator:
    def __init__(self, model_path="./checkpoints/final"):
        # 加载训练后的模型
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
    
    def generate(self, prompt, max_length=512):
        """
        生成推荐结果
        
        参数：
            prompt: 输入prompt
            max_length: 最大生成长度
        
        返回：
            生成的文本
        """
        # 编码
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # 生成
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=0.7,
                do_sample=True
            )
        
        # 解码
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return result
```

### 命令行交互实现

```python
# main.py

from src.rag.retriever import NutritionRetriever
from src.rag.generator import NutritionGenerator

def main():
    print("=" * 50)
    print("        基米吃饭 - 智能营养配餐助手")
    print("=" * 50)
    print()
    
    # 初始化组件
    retriever = NutritionRetriever()
    generator = NutritionGenerator()
    
    # 获取用户输入
    protein = int(input("请输入蛋白质（g）: "))
    fat = int(input("请输入脂肪（g）: "))
    carbs = int(input("请输入碳水（g）: "))
    
    # RAG检索
    query = f"蛋白质{protein}g，脂肪{fat}g，碳水{carbs}g"
    retrieved_foods = retriever.retrieve(query)
    
    # 构建prompt
    prompt = f"""
    用户需要摄入：蛋白质{protein}g，脂肪{fat}g，碳水{carbs}g
    
    以下是可用的食材：
    {format_foods(retrieved_foods)}
    
    请推荐食材搭配，达到用户的营养目标。
    """
    
    # LLM生成
    result = generator.generate(prompt)
    
    # 格式化输出
    print("\n正在为你推荐食材...\n")
    print(format_output(result))

def format_foods(foods):
    """格式化食材列表"""
    # 实现细节...
    pass

def format_output(result):
    """格式化输出结果"""
    # 实现细节...
    pass

if __name__ == "__main__":
    main()
```

---

## 第五阶段：测试优化

### 时间：第11-14天

### 任务清单

| 序号 | 任务 | 具体操作 | 验收标准 | 预计时间 |
|------|------|----------|----------|----------|
| 5.1 | 功能测试 | 测试所有功能 | 无报错 | 3小时 |
| 5.2 | 效果评估 | 评估推荐质量 | 推荐合理 | 3小时 |
| 5.3 | 提示词优化 | 调整prompt | 输出质量提升 | 3小时 |
| 5.4 | 检索优化 | 调整RAG策略 | 检索更准确 | 3小时 |
| 5.5 | 编写用户文档 | 编写使用说明 | 文档完整 | 2小时 |
| 5.6 | 代码整理 | 添加注释、清理代码 | 代码规范 | 2小时 |

### 测试用例

```
测试用例1：标准输入
输入：蛋白质150g，脂肪60g，碳水200g
预期：输出包含至少5种食材，营养数据合理

测试用例2：高蛋白输入
输入：蛋白质200g，脂肪50g，碳水150g
预期：输出以肉类、蛋类为主

测试用例3：低脂输入
输入：蛋白质100g，脂肪30g，碳水250g
预期：输出以蔬菜、主食为主

测试用例4：极端输入
输入：蛋白质300g，脂肪100g，碳水400g
预期：系统提示输入过高，建议调整
```

### 效果评估指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| 推荐合理性 | 推荐的食材是否符合营养目标 | >80% |
| 营养准确性 | 推荐的营养数据是否准确 | 误差<10% |
| 多样性 | 推荐的食材种类是否多样 | >5种 |
| 响应时间 | 生成推荐的时间 | <10秒 |

### 优化方向

```
如果推荐不合理：
├── 调整prompt模板
├── 增加训练数据
├── 调整训练参数
└── 优化RAG检索

如果营养不准确：
├── 检查数据质量
├── 优化营养计算逻辑
└── 增加约束条件

如果响应慢：
├── 优化模型推理
├── 减少检索数量
└── 使用更快的Embedding模型
```

---

## 附录

### 常用命令

```bash
# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行主程序
python main.py

# 运行训练
python train.py

# 运行测试
python -m pytest tests/
```

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| CUDA不可用 | 没有安装GPU版PyTorch | 使用云平台 |
| 显存不足 | 模型太大 | 减小batch_size或使用LoRA |
| 模型加载慢 | 模型文件大 | 使用本地缓存 |
| 检索不准 | Embedding质量差 | 更换Embedding模型 |

### 参考资料

1. [Qwen2.5模型](https://huggingface.co/Qwen/Qwen2.5-1.5B)
2. [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
3. [LangChain RAG教程](https://python.langchain.com/docs/tutorials/rag/)
4. [ChromaDB文档](https://docs.trychroma.com/)
5. [AutoDL使用教程](https://www.autodl.com/docs/)

---

**文档结束**

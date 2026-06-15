# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 用户偏好与工作规则

### 基本信息
- **GitHub仓库**: https://github.com/daiyangbo/eat-health
- **用途**: 项目需要保存时保存到此仓库

### 用户背景
- **身份**: 大学生
- **编程经验**: 几乎为0，只会Python和C++
- **开发工具**: VSCode
- **开发环境**: 准备用云平台（如AutoDL）
- **当前目标**: 训练一个属于自己的大模型（具体功能待定）
- **技术栈偏好**: 不了解，需要详细解释
- **学习风格**: 希望技术概念详细明了，能最快理解

### 工作规则

#### 1. 代码保存规则
- 只有用户明确要求保存时才进行保存操作
- 保存目标为 GitHub 仓库: https://github.com/daiyangbo/eat-health

#### 2. 回复格式规则
- 每次回复必须以"报告老大"开头，无论回复内容是什么

#### 3. 需求澄清规则
当用户提出的需求过于宽泛或不明确时，应主动反问以确认具体要求，例如：
- 用户说"写个网站" → 反问基于什么技术栈、什么框架、什么风格
- 用户说"做个功能" → 反问具体实现方式、使用场景、技术要求
- 用户说"优化代码" → 反问优化方向（性能/可读性/结构）

#### 4. 确认清单
在开始工作前，确保明确以下要素：
- 具体使用的技术和工具
- 具体的实现目标
- 具体的输出格式
- 具体的保存要求

#### 5. 工作流程规则
**一步一步完成任务，先分析再做**
- 收到任务后，先拆解为多个步骤
- 每个步骤先分析（调研、理解、规划），再执行（编码、实现）
- 使用 TodoWrite 工具记录任务进度
- 完成一个步骤后，汇报进度，再进入下一步
- 遇到问题及时反馈，不要盲目推进

#### 6. 对话打包规则
当用户说"打包对话"时，执行以下操作：
- 将当前对话的所有有用信息写入 `对话总览.md` 文件
- 创建对应的对话记录文件，保存到 `对话记录/` 文件夹（如 `对话记录/第X次对话记录.md`）
- 更新 `对话总览.md` 中的对话记录表格

#### 7. 新对话启动规则
每次开新对话时，必须先读取以下内容：
- **学习记录**：`05-学习记录/` 文件夹中的学习记录文件
- **当前阶段项目文件夹**：根据 `对话总览.md` 中的当前阶段，读取对应的项目文件夹内容
  - 如当前阶段是 MVP，则读取 `01-MVP版本-验证核心能力/` 中的工作流程和待办事项
- **对话总览**：读取 `对话总览.md` 了解项目整体进度和历史对话内容

#### 8. 参考资料规则
- **Eat This Much 分析报告**：在设计功能、算法、用户体验时，可以适当参考 `Eat This Much 深度分析报告.md` 中的功能设计、技术实现和优点分析
- 参考时注明引用来源，但不要完全照搬，需根据学校食堂场景进行调整

#### 9. 数据来源规则
- 给出任何数据、事实、统计信息时，必须标注数据来源
- 来源格式：`来源：[网站/文档名称](URL)`
- 示例：`来源：[eatthismuch.com](https://www.eatthismuch.com/)`
- 如果是推测或假设，必须明确标注为"推测"或"假设"

#### 10. 文件组织规则
- **批量创建文件时**：一次性创建多个文件前，应先创建对应的文件夹来存放
- **支线文件时**：在偏离项目主线的基础上创建文件时，应先创建对应的文件夹来存放
- **示例**：
  - 创建多个报名表 → 先创建 `报名材料/` 文件夹
  - 创建学习笔记 → 先创建 `学习笔记/` 文件夹
  - 创建临时文件 → 先创建 `临时文件/` 文件夹

#### 11. Git 推送规则
- **不要每次修改文件就自动推送**：修改文件后只在本地保存，不执行 `git push`
- **只在用户明确要求时推送**：当用户说"推送"、"更新到 git"、"同步到 GitHub" 时才执行 `git push`
- **一次性推送所有修改**：推送时将所有未提交的修改一起提交并推送
- **推送前先检查**：执行 `git status` 确认修改内容，执行 `git add` 和 `git commit` 后再推送
- **示例**：
  - 用户说"把代码更新到 git" → 执行 `git add . && git commit -m "xxx" && git push`
  - 用户说"推送" → 同上
  - 用户没有说推送 → 只在本地修改，不执行 `git push`

## Repository Overview

This directory (`claude project/`) contains the **consolidated learning records** from an 11-chapter LLM (Large Language Model) study series. It is a documentation-only directory — no build system, no tests, no executable code.

The parent directory (`documents/`) contains the full learning materials organized by chapter:

```
documents/
├── chapter1/    # BERT微调与部署 (notebook, PDF, TextClassification code)
├── chapter2/    # 提示工程 (notebook, 3 Python scripts)
├── chapter3/    # 知识编辑 (notebook, EasyEdit)
├── chapter4/    # 数学推理SFT (notebook, vllm)
├── chapter5/    # 文本水印 (notebook, X-SIR)
├── chapter6/    # 越狱攻击 (notebook, EasyJailbreak, work.py)
├── chapter7/    # 文本隐写术 (2 notebooks: original + fixed)
├── chapter8/    # 多模态MLLM (notebook, NExT-GPT)
├── chapter9/    # GUI智能体 (notebook, Qwen2-VL)
├── chapter10/   # 智能体安全 (notebook, R-Judge)
├── chapter11/   # RLHF (notebook, TRL/PPO, requirements.txt)
└── claude project/  # ← This directory: consolidated learning records
```

## Document Structure

Each `完整学习记录-打包N.md` file is a self-contained chapter summary following a consistent structure:

1. **PDF内容概览** — Summary of source lecture slides
2. **核心知识点详解** — Deep-dive Q&A on key concepts
3. **实验完整流程** — Step-by-step experiment walkthrough
4. **遇到的问题及解决** — Problems encountered and solutions
5. **与前序章节的关联** — Cross-references to earlier chapters
6. **术语表** — Glossary of technical terms
7. **学习资源** — References and learning resources
8. **学习进度** — Completion checklist

## Topic Progression

| Chapter | Topic | Key Tools/Models |
|---------|-------|------------------|
| 1 | BERT微调与部署 | Transformers, Gradio, AutoDL |
| 2 | 提示工程与思维链 | OpenAI API, mimo-v2.5-pro |
| 3 | 大模型知识编辑 | EasyEdit, ROME, GPT-2-XL |
| 4 | 数据蒸馏与数学推理 | DeepSeek-R1, Qwen2.5-Math, vllm |
| 5 | LLM文本水印 | X-SIR, KGW, Baichuan-7B |
| 6 | LLM越狱攻击 | EasyJailbreak, PAIR, AdvBench |
| 7 | LLM文本隐写术 | GPT-2, Huffman/FLC coding |
| 8 | 多模态大语言模型 | NExT-GPT, ImageBind, Vicuna |
| 9 | GUI智能体构建 | Qwen2-VL, LLaMA-Factory, OS-Kairos |
| 10 | 智能体安全 | R-Judge, risk modeling |
| 11 | RLHF与PPO | TRL, GPT-2, distilbert-imdb |

## Working with This Repository

- All content is in Chinese (Simplified). Technical terms are provided in English.
- The learning records reference code and notebooks in the parent `chapterN/` directories.
- Cross-references between chapters are documented in each file's "与前序章节的关联" section.
- To run the actual experiments, navigate to the corresponding `chapterN/` directory in the parent folder.

# -*- coding: utf-8 -*-
"""
RAG 知识库构建脚本

功能：
1. 加载食材数据
2. 使用 Embedding 模型向量化
3. 存入 ChromaDB
4. 测试检索效果

输入：
- foods_cleaned.json: 清洗后的食材数据

输出：
- ChromaDB 向量数据库
"""

import json
import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


def load_json(file_path):
    """加载 JSON 文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_food_text(food):
    """
    创建食物的文本描述

    用于向量化
    """
    name = food.get('name_en', '')
    category = food.get('category', '')
    nutrition = food.get('nutrition', {})
    tags = food.get('tags', [])

    # 构建文本描述
    text_parts = [
        f"Food: {name}",
        f"Category: {category}",
        f"Protein: {nutrition.get('protein', 0)}g",
        f"Fat: {nutrition.get('fat', 0)}g",
        f"Carbs: {nutrition.get('carbs', 0)}g",
        f"Calories: {nutrition.get('calories', 0)}kcal",
        f"Tags: {', '.join(tags)}"
    ]

    return " | ".join(text_parts)


def build_rag(foods, db_path, model_name='all-MiniLM-L6-v2'):
    """
    构建 RAG 知识库

    参数：
        foods: 食物数据列表
        db_path: ChromaDB 存储路径
        model_name: Embedding 模型名称
    """
    print("=" * 50)
    print("开始构建 RAG 知识库")
    print("=" * 50)

    # 1. 加载 Embedding 模型
    print(f"\n[1/4] 加载 Embedding 模型: {model_name}")
    print("  首次运行需要下载模型，请稍候...")
    model = SentenceTransformer(model_name)
    print(f"[OK] 模型加载成功")

    # 2. 初始化 ChromaDB
    print(f"\n[2/4] 初始化 ChromaDB: {db_path}")
    client = chromadb.PersistentClient(path=db_path)
    print(f"[OK] ChromaDB 初始化成功")

    # 3. 创建集合
    print(f"\n[3/4] 创建集合: foods")
    # 如果集合已存在，删除重建
    try:
        client.delete_collection("foods")
        print("  已删除旧集合")
    except:
        pass

    collection = client.create_collection(
        name="foods",
        metadata={"description": "Food nutrition database"}
    )
    print(f"[OK] 集合创建成功")

    # 4. 向量化并存入数据
    print(f"\n[4/4] 向量化并存入数据...")
    print(f"  总数据量: {len(foods)}")

    # 分批处理
    batch_size = 100
    for i in range(0, len(foods), batch_size):
        batch = foods[i:i + batch_size]

        # 准备数据
        ids = []
        documents = []
        metadatas = []

        for food in batch:
            food_id = str(food.get('food_id', ''))
            text = create_food_text(food)
            metadata = {
                'name_en': food.get('name_en', ''),
                'category': food.get('category', ''),
                'protein': food.get('nutrition', {}).get('protein', 0),
                'fat': food.get('nutrition', {}).get('fat', 0),
                'carbs': food.get('nutrition', {}).get('carbs', 0),
                'calories': food.get('nutrition', {}).get('calories', 0),
                'tags': ', '.join(food.get('tags', []))
            }

            ids.append(food_id)
            documents.append(text)
            metadatas.append(metadata)

        # 生成向量
        embeddings = model.encode(documents).tolist()

        # 存入 ChromaDB
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        if (i + batch_size) % 500 == 0 or i + batch_size >= len(foods):
            print(f"  已处理 {min(i + batch_size, len(foods))}/{len(foods)}")

    print(f"\n[OK] 数据存入完成")
    print(f"  集合大小: {collection.count()}")

    return collection


def test_retrieval(collection, model, query, n_results=5):
    """
    测试检索效果

    参数：
        collection: ChromaDB 集合
        model: Embedding 模型
        query: 查询文本
        n_results: 返回结果数量
    """
    print(f"\n查询: {query}")

    # 向量化查询
    query_embedding = model.encode([query]).tolist()

    # 检索
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    # 显示结果
    print(f"Top {n_results} 结果:")
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"\n  {i}. {metadata['name_en']}")
        print(f"     分类: {metadata['category']}")
        print(f"     蛋白质: {metadata['protein']}g | 脂肪: {metadata['fat']}g | 碳水: {metadata['carbs']}g")
        print(f"     热量: {metadata['calories']}kcal")
        print(f"     标签: {metadata['tags']}")

    return results


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent

    # 输入文件
    input_file = os.path.join(project_root, 'data', 'processed', 'foods_cleaned.json')

    # ChromaDB 路径
    db_path = os.path.join(project_root, 'data', 'knowledge_base', 'chroma')

    # 加载数据
    print(f"加载数据: {input_file}")
    foods = load_json(input_file)
    print(f"加载了 {len(foods)} 条食物数据")

    # 构建 RAG 知识库
    collection = build_rag(foods, db_path)

    # 测试检索
    print("\n" + "=" * 50)
    print("测试检索效果")
    print("=" * 50)

    # 加载模型用于测试
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 测试查询
    test_queries = [
        "high protein low fat food",
        "chicken breast",
        "vegetables",
        "rice and pasta",
        "fish and seafood"
    ]

    for query in test_queries:
        test_retrieval(collection, model, query, n_results=3)
        print("-" * 50)


if __name__ == '__main__':
    main()

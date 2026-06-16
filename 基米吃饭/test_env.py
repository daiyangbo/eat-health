# Environment Test Script
import sys

def test_environment():
    print("=" * 50)
    print("        Environment Test")
    print("=" * 50)
    print()

    # Test Python version
    print(f"[1] Python Version: {sys.version}")
    print()

    # Test torch
    try:
        import torch
        print(f"[2] PyTorch: {torch.__version__}")
        print(f"    CUDA Available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"    CUDA Version: {torch.version.cuda}")
            print(f"    GPU: {torch.cuda.get_device_name(0)}")
    except ImportError as e:
        print(f"[2] PyTorch: FAILED - {e}")
    print()

    # Test transformers
    try:
        import transformers
        print(f"[3] Transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"[3] Transformers: FAILED - {e}")
    print()

    # Test datasets
    try:
        import datasets
        print(f"[4] Datasets: {datasets.__version__}")
    except ImportError as e:
        print(f"[4] Datasets: FAILED - {e}")
    print()

    # Test accelerate
    try:
        import accelerate
        print(f"[5] Accelerate: {accelerate.__version__}")
    except ImportError as e:
        print(f"[5] Accelerate: FAILED - {e}")
    print()

    # Test chromadb
    try:
        import chromadb
        print(f"[6] ChromaDB: {chromadb.__version__}")
    except ImportError as e:
        print(f"[6] ChromaDB: FAILED - {e}")
    print()

    # Test sentence-transformers
    try:
        import sentence_transformers
        print(f"[7] Sentence-Transformers: {sentence_transformers.__version__}")
    except ImportError as e:
        print(f"[7] Sentence-Transformers: FAILED - {e}")
    print()

    # Test pandas
    try:
        import pandas as pd
        print(f"[8] Pandas: {pd.__version__}")
    except ImportError as e:
        print(f"[8] Pandas: FAILED - {e}")
    print()

    # Test numpy
    try:
        import numpy as np
        print(f"[9] NumPy: {np.__version__}")
    except ImportError as e:
        print(f"[9] NumPy: FAILED - {e}")
    print()

    # Test tqdm
    try:
        import tqdm
        print(f"[10] TQDM: {tqdm.__version__}")
    except ImportError as e:
        print(f"[10] TQDM: FAILED - {e}")
    print()

    # Test pyyaml
    try:
        import yaml
        print(f"[11] PyYAML: {yaml.__version__}")
    except ImportError as e:
        print(f"[11] PyYAML: FAILED - {e}")
    print()

    # Test python-dotenv
    try:
        import dotenv
        print(f"[12] Python-Dotenv: OK")
    except ImportError as e:
        print(f"[12] Python-Dotenv: FAILED - {e}")
    print()

    print("=" * 50)
    print("        Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_environment()

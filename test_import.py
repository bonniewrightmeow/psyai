#!/usr/bin/env python
print("Testing transformers import...")
try:
    from transformers import pipeline
    print("✓ Successfully imported pipeline from transformers")
    print(f"pipeline type: {type(pipeline)}")
except ImportError as e:
    print(f"✗ Failed to import: {e}")
    import sys
    print(f"Python: {sys.executable}")
    print(f"Python version: {sys.version}")
    import transformers
    print(f"Transformers version: {transformers.__version__}")
    print(f"Transformers file: {transformers.__file__}")
    print(f"Available in transformers: {'pipeline' in dir(transformers)}")

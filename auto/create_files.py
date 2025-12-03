#!/usr/bin/env python3
import os
import sys

# 检查当前目录
dir_path = '/d:/MyResearch/codeComplex/auto/'
print(f"Current directory: {os.getcwd()}")
print(f"Target directory: {dir_path}")

# 检查目录是否存在
if not os.path.exists(dir_path):
    print(f"Directory {dir_path} does not exist, creating...")
    os.makedirs(dir_path, exist_ok=True)

# 列出目录内容
print(f"Contents of {dir_path}:")
try:
    for item in os.listdir(dir_path):
        print(f"  {item}")
except Exception as e:
    print(f"Error listing directory: {e}")

# 尝试创建一个测试文件
test_file = os.path.join(dir_path, "test.txt")
try:
    with open(test_file, 'w') as f:
        f.write("Test file created successfully")
    print(f"Created test file: {test_file}")
    # 验证文件存在
    if os.path.exists(test_file):
        print(f"✓ Test file exists")
    else:
        print(f"✗ Test file does not exist")
except Exception as e:
    print(f"Error creating test file: {e}")
    import traceback
    traceback.print_exc()

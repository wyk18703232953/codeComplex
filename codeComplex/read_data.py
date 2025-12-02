import json

# 读取文件并打印内容
try:
    with open('d:/MyResearch/codeComplex/data/data.jsonl', 'r', encoding='utf-8') as f:
        # 读取前10行进行展示
        for i in range(10):
            line = f.readline()
            if not line:
                break
            # 尝试解析JSON确保格式正确
            try:
                data = json.loads(line)
                print(f"Line {i+1}:")
                print(f"Problem: {data.get('problem', 'N/A')}")
                print(f"From: {data.get('from', 'N/A')}")
                print(f"Complexity: {data.get('complexity', 'N/A')}")
                print("Source code preview:")
                source = data.get('src', '')
                # 只显示源代码的前几行
                source_preview = '\n'.join(source.split('\n')[:5])
                print(source_preview)
                if len(source.split('\n')) > 5:
                    print("... (more lines omitted)")
                print("-" * 50)
            except json.JSONDecodeError:
                print(f"Line {i+1}: Invalid JSON format")
                print("-" * 50)

    # 统计文件总行数
    with open('d:/MyResearch/codeComplex/data/data.jsonl', 'r', encoding='utf-8') as f:
        line_count = sum(1 for _ in f)
    print(f"\nTotal number of records in the file: {line_count}")
    
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error reading file: {e}")
import json

# 打开JSONL文件
jsonl_path = "d:\MyResearch\codeComplex\data\data.jsonl"

print("正在分析data.jsonl文件，查找包含测试用例信息的样本...")
print("="*60)

with open(jsonl_path, 'r', encoding='utf-8') as f:
    line_number = 0
    test_case_count = 0
    
    for line in f:
        line_number += 1
        try:
            data = json.loads(line)
            src = data.get('src', '')
            
            # 检查src字段是否包含测试用例特征
            has_test_cases = False
            matched_markers = []
            test_case_markers = [
                "Test: #",  "Checker Log",
                "Sample Input", "Sample Output", "Sample Input 1", "Sample Output 1",
                "inputCopy", "outputCopy",
                "/*"
            ]
            
            for marker in test_case_markers:
                if marker in src:
                    has_test_cases = True
                    matched_markers.append(marker)
            
            if has_test_cases:
                test_case_count += 1
                print(f"行号 {line_number}: 包含测试用例信息")
                print(f"  复杂度: {data.get('complexity', 'unknown')}")
                print(f"  问题: {data.get('problem', '').strip()[:50]}...")
                print(f"  匹配到的特征字符串: {', '.join(matched_markers)}")
                # print(f"  src内容: {src}")  # 打印前200个字符
                print("="*60)
            
            # 只分析前20行
            # if line_number >= 20:
            #     break
                
        except json.JSONDecodeError:
            print(f"行号 {line_number}: JSON解析错误")
            print("-"*60)

print("="*60)
print(f"分析完成！在前{line_number}行中，找到{test_case_count}个包含测试用例信息的样本。")

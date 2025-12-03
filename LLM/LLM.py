from openai import OpenAI
import os
import re
import json

def validate_code_complexity(src, expected_complexity, api_key=None, base_url=None):
    """
    验证代码的时间复杂度是否与期望复杂度一致，并返回详细记录
    
    参数:
    src (str): 源代码
    expected_complexity (str): 期望的时间复杂度，如 'linear', 'quadratic', 'constant', 'nlogn', 'logn' 等
    api_key (str, optional): OpenAI API密钥，如果不提供则使用默认密钥
    base_url (str, optional): API基础URL，如果不提供则使用默认URL
    
    返回:
    dict: 包含验证结果的详细记录
        - is_match (bool): 复杂度是否匹配
        - expected_complexity (str): 期望的复杂度
        - model_raw_output (str): 模型原始输出
        - model_analyzed_complexity (str): 分析后的模型复杂度
        - error (str): 错误信息（如有）
    """
    # 设置默认API参数
    if api_key is None:
        api_key = "sk-3sNQAO5ydpVp29WWoCqvM7Ajqzd1I5WKOpe29cpoT3DoMrZe"
    if base_url is None:
        base_url = "https://yunwu.ai/v1"
    
    # 创建OpenAI客户端
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # 定义提示词，要求模型分析代码复杂度
    system_prompt = """你是一位算法分析专家，精通时间复杂度分析。
    你的任务是：
    1. 分析给定代码的时间复杂度
    2. 仅返回复杂度的标准术语，如：constant、linear、logn、nlogn、quadratic、cubic、np。
    3. 不要输出任何解释或额外信息，只输出复杂度术语本身"""
    
    user_prompt = f"""请分析以下代码的时间复杂度，并仅返回标准的复杂度术语：
    ```
    {src}
    ```
    
    请严格按照要求，只输出复杂度术语，不要添加任何其他内容！"""
    
    # 初始化记录字典
    record = {
        'is_match': False,
        'expected_complexity': expected_complexity.lower().strip(),
        'model_raw_output': None,
        'model_analyzed_complexity': None,
        'error': None
    }
    
    try:
        # 调用大模型API
        response = client.chat.completions.create(
            model="gpt-5.1",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=False
        )
        
        # 提取模型原始回复
        model_raw_output = response.choices[0].message.content.strip().lower()
        record['model_raw_output'] = model_raw_output
        
        # 清理模型输出，提取关键复杂度术语
        
        # 比较复杂度
        is_match = compare_complexity(model_raw_output, record['expected_complexity'])
        record['is_match'] = is_match
        
        # 记录日志
        print(f"期望复杂度: {record['expected_complexity']}")
        print(f"模型原始输出: {record['model_raw_output']}")
        # print(f"模型分析复杂度: {record['model_analyzed_complexity']}")
        print(f"匹配结果: {record['is_match']}")
        
        return record
        
    except Exception as e:
        error_msg = str(e)
        record['error'] = error_msg
        print(f"分析代码复杂度时出错: {error_msg}")
        return record


def compare_complexity(actual, expected):
    """
    比较两个复杂度是否匹配，考虑可能的同义词和近似表达
    """
    # 定义复杂度等价映射
    equivalence = {
        'constant': {'constant', 'o(1)', '1'},
        'linear': {'linear', 'o(n)', 'n'},
        'logn': {'logn', 'log n', 'o(log n)', 'o(logn)'},
        'nlogn': {'nlogn', 'n log n', 'o(n log n)', 'o(n logn)'},
        'quadratic': {'quadratic', 'o(n^2)', 'n^2'},
        'cubic': {'cubic', 'o(n^3)', 'n^3'},
        'np': {'np', 'o(n^p)', 'n^p'}
    }
    
    # 检查是否在等价集合中
    if expected in equivalence:
        return actual in equivalence[expected] or actual == expected
    
    # 直接比较
    return actual == expected

def batch_validate_from_jsonl(jsonl_file_path, max_items=None, save_results=True, output_file=None):
    """
    从JSONL文件批量验证代码复杂度并记录详细实验过程
    
    参数:
    jsonl_file_path (str): JSONL文件路径
    max_items (int): 最大处理项目数，如果为None则处理所有项目
    save_results (bool): 是否保存结果到文件
    output_file (str): 输出文件路径，如果为None则自动生成
    
    返回:
    tuple: (统计结果字典, 详细记录列表)
    """
    total = 0
    correct = 0
    failed = 0
    detailed_records = []  # 存储详细记录
    
    # 确保结果目录存在
    results_dir = "D:/MyResearch/codeComplex/results/LLM"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # 如果未指定输出文件，自动生成
    if save_results and output_file is None:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(results_dir, f"complexity_validation_results_{timestamp}.json")
    elif save_results and output_file and not os.path.isabs(output_file):
        # 如果指定了相对路径，转换为绝对路径到results目录
        output_file = os.path.join(results_dir, output_file)
    
    try:
        with open(jsonl_file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if max_items is not None and i >= max_items:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    src = data.get('src', '')
                    expected_complexity = data.get('complexity', '')
                    problem = data.get('problem', '')
                    source = data.get('from', '')
                    
                    if src and expected_complexity:
                        total += 1
                        print(f"\n--- 处理第 {total} 个代码样本 ---")
                        # 验证代码复杂度
                        validation_result = validate_code_complexity(src, expected_complexity)
                        
                        # 创建详细记录
                        record = {
                            'sample_id': i + 1,
                            'problem': problem[:100] + '...' if len(problem) > 100 else problem,
                            'source': source,
                            'expected_complexity': validation_result['expected_complexity'],
                            'model_raw_output': validation_result['model_raw_output'],
                            'is_match': validation_result['is_match'],
                            'error': validation_result['error']
                        }
                        detailed_records.append(record)
                        
                        # 更新统计信息
                        if validation_result['is_match']:
                            correct += 1
                        else:
                            failed += 1
                
                except json.JSONDecodeError:
                    error_msg = "JSON格式错误"
                    print(f"第 {i+1} 行格式错误")
                    # 记录格式错误的样本
                    record = {
                        'sample_id': i + 1,
                        'problem': '',
                        'source': '',
                        'expected_complexity': '',
                        'model_raw_output': None,
                        'model_analyzed_complexity': None,
                        'is_match': False,
                        'error': error_msg
                    }
                    detailed_records.append(record)
                    failed += 1
                except Exception as e:
                    error_msg = str(e)
                    print(f"处理第 {i+1} 行时出错: {error_msg}")
                    # 记录处理错误的样本
                    record = {
                        'sample_id': i + 1,
                        'problem': '',
                        'source': '',
                        'expected_complexity': '',
                        'model_raw_output': None,
                        'model_analyzed_complexity': None,
                        'is_match': False,
                        'error': error_msg
                    }
                    detailed_records.append(record)
                    failed += 1
    
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
    
    # 计算准确率
    accuracy = (correct / total * 100) if total > 0 else 0
    
    results = {
        'total': total,
        'correct': correct,
        'failed': failed,
        'accuracy': accuracy,
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    # 保存结果到文件
    if save_results and output_file:
        try:
            all_results = {
                'summary': results,
                'detailed_records': detailed_records,
                'input_file': jsonl_file_path,
                'max_items': max_items
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            print(f"\n结果已保存到文件: {output_file}")
        except Exception as e:
            print(f"保存结果时出错: {str(e)}")
    
    print(f"\n验证完成!")
    print(f"总样本数: {total}")
    print(f"正确匹配: {correct}")
    print(f"错误匹配: {failed}")
    print(f"准确率: {accuracy:.2f}%")
    
    return results, detailed_records

# 添加datetime导入
import datetime

# 示例用法
if __name__ == "__main__":
    # 示例1：单独验证一个代码片段
    # print("=== 示例1: 单独验证代码片段 ===")
    # sample_code = """
    # def linear_search(arr, target):
    #     for i in range(len(arr)):
    #         if arr[i] == target:
    #             return i
    #     return -1
    # """
    # expected = "linear"
    # result = validate_code_complexity(sample_code, expected)
    # print(f"验证结果: {result['is_match']}")
    # print(f"详细记录: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # 示例2：从JSONL文件批量验证
    print("\n=== 示例2: 从JSONL文件批量验证 ===")
    jsonl_path = "d:/MyResearch/codeComplex/data/data.jsonl"
    if os.path.exists(jsonl_path):
        # 处理所有样本
        batch_results, detailed_records = batch_validate_from_jsonl(jsonl_path, max_items=None, save_results=True)
        
        # 显示所有详细记录
        print(f"\n所有详细记录 ({len(detailed_records)} 条):")
        for i, record in enumerate(detailed_records):
            print(f"\n记录 {i+1}:")
            print(f"样本ID: {record['sample_id']}")
            print(f"问题: {record['problem']}")
            print(f"来源: {record['source']}")
            print(f"期望复杂度: {record['expected_complexity']}")
            print(f"模型原始输出: {record['model_raw_output']}")
            print(f"匹配结果: {record['is_match']}")
            if record['error']:
                print(f"错误: {record['error']}")
    else:
        print(f"文件不存在: {jsonl_path}")

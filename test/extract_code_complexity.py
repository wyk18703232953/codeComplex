import json
import os
def get_source_and_complexity(file_path, max_lines=float('inf'), filter_complexity=None):
    """
    从JSONL文件中提取每一行的源代码和复杂度信息
    
    参数:
    file_path (str): JSONL文件路径
    max_lines (int): 最大处理行数，默认为处理所有行
    filter_complexity (str, optional): 按复杂度筛选，如 'linear', 'quadratic' 等，默认不筛选
    
    返回:
    list: 包含字典的列表，每个字典包含'src', 'complexity'和其他相关字段
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在")
    
    results = []
    line_number = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_number += 1
                if line_number > max_lines:
                    break
                
                # 跳过空行
                line = line.strip()
                if not line:
                    continue
                
                try:
                    data = json.loads(line)
                    # 提取源代码和复杂度信息
                    src = data.get('src', '')
                    complexity = data.get('complexity', 'unknown')
                    problem = data.get('problem', '')
                    source = data.get('from', '')
                    
                    # 如果指定了复杂度筛选，则只添加符合条件的记录
                    if filter_complexity and complexity != filter_complexity:
                        continue
                    
                    results.append({
                        'src': src,
                        'complexity': complexity,
                        'problem': problem,
                        'from': source,
                        'line_number': line_number
                    })
                    
                except json.JSONDecodeError as e:
                    print(f"行 {line_number} 解析错误: {e}")
                except Exception as e:
                    print(f"处理行 {line_number} 时出错: {e}")
    
    except Exception as e:
        raise Exception(f"读取文件时出错: {e}")
    
    return results

# 兼容旧函数名
def extract_code_complexity(file_path, max_lines=float('inf')):
    """
    从JSONL文件中提取每一行的源代码和复杂度信息（兼容旧接口）
    
    参数:
    file_path (str): JSONL文件路径
    max_lines (int): 最大处理行数，默认为处理所有行
    
    返回:
    list: 包含字典的列表，每个字典包含'src'和'complexity'字段
    """
    return get_source_and_complexity(file_path, max_lines)

def display_results(results, preview_lines=5, show_problem_info=True):
    """
    展示提取的结果，包括源代码预览
    
    参数:
    results (list): 提取的结果列表
    preview_lines (int): 源代码预览显示的行数
    show_problem_info (bool): 是否显示问题信息
    """
    print(f"总共提取了 {len(results)} 条记录\n")
    
    for i, item in enumerate(results):
        print(f"记录 #{item['line_number']}:")
        print(f"复杂度: {item['complexity']}")
        
        if show_problem_info and 'problem' in item and 'from' in item:
            print(f"问题: {item['problem']}")
            print(f"来源: {item['from']}")
        
        print("源代码预览:")
        
        # 显示源代码的前几行
        source_lines = item['src'].split('\n')
        preview = '\n'.join(source_lines[:preview_lines])
        print(preview)
        
        if len(source_lines) > preview_lines:
            print(f"... (还有 {len(source_lines) - preview_lines} 行)")
        
        print("-" * 50)

def count_complexity_types(results):
    """
    统计不同复杂度类型的数量
    
    参数:
    results (list): 提取的结果列表
    
    返回:
    dict: 复杂度类型及其对应的数量
    """
    counts = {}
    for item in results:
        complexity = item['complexity']
        counts[complexity] = counts.get(complexity, 0) + 1
    return counts

# 测试函数
if __name__ == "__main__":
    file_path = 'd:/MyResearch/codeComplex/data/data.jsonl'
    
    try:
        # 示例1: 提取前5条记录
        # print("=== 示例1: 提取前5条记录 ===")
        # results = get_source_and_complexity(file_path, max_lines=5)
        # display_results(results)
        
        # 示例2: 按复杂度筛选 - 只提取线性复杂度的代码
        # print("\n=== 示例2: 筛选线性复杂度(linear)的代码 ===")
        # linear_results = get_source_and_complexity(file_path, max_lines=2, filter_complexity='linear')
        # display_results(linear_results[:3], preview_lines=3)
        # print(f"找到 {len(linear_results)} 条线性复杂度的代码")
        
        # 示例3: 按复杂度筛选 - 只提取二次复杂度的代码
        # print("\n=== 示例3: 筛选二次复杂度(quadratic)的代码 ===")
        # quadratic_results = get_source_and_complexity(file_path, max_lines=2, filter_complexity='quadratic')
        # display_results(quadratic_results[:3], preview_lines=3)
        # print(f"找到 {len(quadratic_results)} 条二次复杂度的代码")
        
        # 示例4: 统计前100条记录中各种复杂度的分布
        print("\n=== 示例4: 统计前200条记录的复杂度分布 ===")
        sample_results = get_source_and_complexity(file_path, max_lines=1000)
        complexity_counts = count_complexity_types(sample_results)
        print("复杂度分布:")
        for complexity, count in complexity_counts.items():
            print(f"  {complexity}: {count} 条")
            
    except Exception as e:
        print(f"发生错误: {e}")
    
    print("\n函数使用示例:")
    print("1. 获取所有代码和复杂度: get_source_and_complexity(file_path)")
    print("2. 获取前100条: get_source_and_complexity(file_path, max_lines=100)")
    print("3. 筛选特定复杂度: get_source_and_complexity(file_path, filter_complexity='linear')")
    print("4. 显示结果: display_results(results, preview_lines=5)")
    print("5. 统计复杂度分布: count_complexity_types(results)")
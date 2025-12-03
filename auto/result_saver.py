#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结果保存模块
将最终的比较结果以标准化JSON格式保存到文件中
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


def save_results(results: List[Dict[str, Any]], output_dir: str = '.', 
                 input_file: str = '', max_items: int = 0) -> str:
    """
    将分析结果保存为标准化JSON格式文件，严格参照示例结构
    
    Args:
        results (List[Dict[str, Any]]): 包含分析结果的列表
        output_dir (str, optional): 输出目录路径，默认为当前目录
        input_file (str, optional): 输入数据文件路径，默认为空字符串
        max_items (int, optional): 处理的最大样本数，默认为0
    
    Returns:
        str: 保存的文件名
    
    Raises:
        IOError: 文件写入错误时抛出
    """
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'complexity_validation_auto_results_{timestamp}.json'
    file_path = os.path.join(output_dir, filename)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成summary部分
    total = len(results)
    correct = sum(1 for r in results if r['is_match'])
    failed = sum(1 for r in results if not r['is_match'])
    accuracy = (correct / total * 100) if total > 0 else 0.0
    
    summary = {
        'total': total,
        'correct': correct,
        'failed': failed,
        'accuracy': round(accuracy, 1),
        'timestamp': datetime.now().isoformat()
    }
    
    # 转换结果为示例格式（注意字段名是ouput而不是output）
    detailed_records = []
    for result in results:
        # 确保字段名与示例一致
        detailed_record = {
            'sample_id': result['sample_id'],
            'problem': result['problem'],
            'source': result['source'],
            'expected_complexity': result['expected_complexity'],
            'ouput': result['output'],  # 注意：示例中是ouput，不是output
            'is_match': result['is_match'],
            'error': result['error']
        }
        detailed_records.append(detailed_record)
    
    # 组装完整的结果结构
    final_results = {
        'summary': summary,
        'detailed_records': detailed_records,
        'input_file': input_file,
        'max_items': max_items
    }
    
    # 保存结果到JSON文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
        return filename
    except IOError as e:
        raise IOError(f"Error writing results to file: {str(e)}")
    except Exception as e:
        raise IOError(f"Unexpected error saving results: {str(e)}")


def format_result(sample_id: int, problem: str, source: str, 
                 expected_complexity: str, output: str, 
                 is_match: bool, error: str = None) -> Dict[str, Any]:
    """
    格式化单个结果为标准化格式
    
    Args:
        sample_id (int): 样本ID
        problem (str): 问题描述
        source (str): Java源代码
        expected_complexity (str): 预期复杂度
        output (str): 分析得到的复杂度
        is_match (bool): 分析结果与预期是否匹配
        error (str, optional): 分析过程中出现的错误信息，默认为None
    
    Returns:
        Dict[str, Any]: 标准化的结果字典
    """
    return {
        'sample_id': sample_id,
        'problem': problem,
        'source': source,
        'expected_complexity': expected_complexity,
        'output': output,
        'is_match': is_match,
        'error': error
    }

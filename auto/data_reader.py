#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据读取模块
读取并解析JSONL数据集，提取Java源代码样本及其关联元数据
"""

import json
from typing import Generator, Dict, Any
from utils import DataFormatError, FileReadError


def read_jsonl_file(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """
    逐行读取JSONL文件，生成Java代码样本及其元数据
    
    Args:
        file_path (str): JSONL文件路径
    
    Yields:
        Dict[str, Any]: 包含Java代码样本及其元数据的字典
    
    Raises:
        FileReadError: 文件无法读取时抛出
        DataFormatError: JSON格式错误时抛出
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            line_number = 0
            while True:
                line = f.readline()
                if not line:
                    break
                line_number += 1
                line = line.strip()
                if not line:
                    continue
                
                try:
                    sample = json.loads(line)
                    yield sample
                except json.JSONDecodeError as e:
                    raise DataFormatError(f"Line {line_number}: Invalid JSON format - {str(e)}")
    except FileNotFoundError:
        raise FileReadError(f"File not found: {file_path}")
    except PermissionError:
        raise FileReadError(f"Permission denied: {file_path}")
    except IOError as e:
        raise FileReadError(f"IO error reading file: {str(e)}")


def extract_java_samples(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """
    从JSONL文件中提取Java代码样本，返回标准化格式
    
    Args:
        file_path (str): JSONL文件路径
    
    Yields:
        Dict[str, Any]: 标准化的Java代码样本字典，包含以下字段：
            - sample_id: 样本ID
            - problem: 问题描述
            - source: Java源代码
            - expected_complexity: 预期复杂度
    
    Raises:
        FileReadError: 文件无法读取时抛出
        DataFormatError: 数据格式错误时抛出
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            line_number = 0
            while True:
                line = f.readline()
                if not line:
                    break
                line_number += 1
                line = line.strip()
                if not line:
                    continue
                
                try:
                    sample = json.loads(line)
                    # 提取必要字段，支持多种字段名
                    sample_id = sample.get('sample_id', line_number)
                    problem = sample.get('problem', '')
                    # 支持'source'或'src'作为Java源代码字段
                    source = sample.get('source', '') or sample.get('src', '')
                    # 支持'expected_complexity'或'complexity'作为预期复杂度字段
                    expected_complexity = sample.get('expected_complexity', '') or sample.get('complexity', '')
                    
                    # 验证必要字段
                    if not source:
                        raise DataFormatError(f"Missing or empty source field in sample {sample_id}")
                    if not expected_complexity:
                        raise DataFormatError(f"Missing or empty complexity field in sample {sample_id}")
                    
                    # 返回标准化样本
                    yield {
                        'sample_id': int(sample_id),
                        'problem': str(problem),
                        'source': str(source),
                        'expected_complexity': str(expected_complexity)
                    }
                except json.JSONDecodeError as e:
                    raise DataFormatError(f"Line {line_number}: Invalid JSON format - {str(e)}")
    except FileNotFoundError:
        raise FileReadError(f"File not found: {file_path}")
    except PermissionError:
        raise FileReadError(f"Permission denied: {file_path}")
    except IOError as e:
        raise FileReadError(f"IO error reading file: {str(e)}")
    except Exception as e:
        raise DataFormatError(f"Error processing file: {str(e)}")

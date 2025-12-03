#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心分析模块
Java代码时间复杂度静态分析，识别复杂度相关结构并计算复杂度标识
"""

import javalang
from typing import Dict, List, Optional, Tuple
from utils import AnalysisError


def analyze_java_complexity(source_code: str) -> str:
    """
    分析Java代码的时间复杂度
    
    Args:
        source_code (str): Java源代码字符串
    
    Returns:
        str: 时间复杂度标识，取值范围：constant、linear、logn、nlogn、quadratic、cubic、np
    
    Raises:
        AnalysisError: 无法解析或识别的代码结构时抛出
    """
    try:
        # 解析Java代码，生成AST
        tree = javalang.parse.parse(source_code)
        
        # 分析AST，获取复杂度相关信息
        complexity_info = _analyze_ast(tree)
        
        # 直接从源代码字符串检测对数模式（备用方法）
        # 这对于简单的for循环模式非常有效
        source_lower = source_code.lower()
        # 检查常见的对数循环模式
        log_patterns = [
            'i *= 2', 'i *=2', 'i /= 2', 'i /=2',
            'j *= 2', 'j *=2', 'j /= 2', 'j /=2',
            'k *= 2', 'k *=2', 'k /= 2', 'k /=2'
        ]
        for pattern in log_patterns:
            if pattern in source_lower:
                complexity_info['has_logarithmic_loop'] = True
                break
        
        # 计算最终复杂度
        final_complexity = _calculate_complexity(complexity_info)
        
        return final_complexity
    except javalang.parser.JavaSyntaxError as e:
        raise AnalysisError(f"Java syntax error: {str(e)}")
    except Exception as e:
        raise AnalysisError(f"Unexpected error during analysis: {str(e)}")


def _analyze_ast(tree) -> Dict[str, any]:
    """
    遍历AST，分析复杂度相关结构
    
    Args:
        tree: Java代码的AST
    
    Returns:
        Dict[str, any]: 包含复杂度相关信息的字典
    """
    # 初始化复杂度信息
    complexity_info = {
        'loop_depth': 0,
        'max_loop_depth': 0,
        'has_nested_loops': False,
        'has_recursion': False,
        'has_binary_search': False,
        'has_sorting_algorithm': False,
        'has_quadratic_pattern': False,
        'has_cubic_pattern': False,
        'has_exponential_pattern': False,
        'has_logarithmic_loop': False,
        'loop_types': [],
        'method_calls': [],
        'recursive_calls': 0
    }
    
    # 1. 首先，识别递归调用
    function_stack = []
    for path, node in javalang.ast.walk_tree(tree):
        node_type = type(node).__name__
        
        if node_type == 'MethodDeclaration':
            if hasattr(node, 'name') and node.name:
                function_stack.append(node.name)
        
        elif node_type == 'MethodInvocation':
            if hasattr(node, 'member'):
                method_name = str(node.member).lower()
                complexity_info['method_calls'].append(method_name)
                
                # 检测递归
                if function_stack and method_name == function_stack[-1].lower():
                    complexity_info['has_recursion'] = True
                    complexity_info['recursive_calls'] += 1
                
                # 检测排序算法
                sorting_keywords = ['sort', 'quicksort', 'mergesort', 'heapsort', 'bubblesort', 'insertionsort']
                if any(keyword in method_name for keyword in sorting_keywords):
                    complexity_info['has_sorting_algorithm'] = True
                
                # 检测二分查找
                if 'binary' in method_name and 'search' in method_name:
                    complexity_info['has_binary_search'] = True
        
        elif node_type == 'MethodDeclaration':
            if function_stack:
                function_stack.pop()
    
    # 2. 然后，计算循环嵌套深度
    max_depth = 0
    
    # 定义一个函数来计算特定节点的最大嵌套深度
    def calculate_max_depth(node, current_depth=0):
        nonlocal max_depth
        node_type = type(node).__name__
        
        if node_type in ['ForStatement', 'WhileStatement', 'DoStatement']:
            current_depth += 1
            if current_depth > max_depth:
                max_depth = current_depth
        
        # 遍历子节点
        if hasattr(node, 'children'):
            for child in node.children:
                if isinstance(child, (list, tuple)):
                    for item in child:
                        if hasattr(item, 'children'):
                            calculate_max_depth(item, current_depth)
                elif hasattr(child, 'children'):
                    calculate_max_depth(child, current_depth)
    
    # 遍历所有节点，计算最大嵌套深度
    for path, node in javalang.ast.walk_tree(tree):
        calculate_max_depth(node)
    
    # 3. 更新复杂度信息
    complexity_info['max_loop_depth'] = max_depth
    
    # 4. 设置复杂度模式
    if max_depth >= 2:
        complexity_info['has_nested_loops'] = True
    if max_depth == 2:
        complexity_info['has_quadratic_pattern'] = True
    elif max_depth == 3:
        complexity_info['has_cubic_pattern'] = True
    elif max_depth > 3:
        complexity_info['has_exponential_pattern'] = True
    
    # 5. 检测对数循环
    has_log_pattern = False
    for path, node in javalang.ast.walk_tree(tree):
        node_type = type(node).__name__
        if node_type == 'ForStatement':
            if hasattr(node, 'update') and node.update:
                update_str = str(node.update).lower()
                log_patterns = ['*= 2', '*=2', '/= 2', '/=2', 'i *=', 'i /=']
                for pattern in log_patterns:
                    if pattern in update_str:
                        has_log_pattern = True
                        break
    
    if has_log_pattern:
        complexity_info['has_logarithmic_loop'] = True
    
    return complexity_info


def _calculate_complexity(complexity_info: Dict[str, any]) -> str:
    """
    根据复杂度信息计算最终的复杂度标识
    
    Args:
        complexity_info (Dict[str, any]): 包含复杂度相关信息的字典
    
    Returns:
        str: 时间复杂度标识
    """
    # 检查是否有指数级复杂度模式
    if complexity_info['has_exponential_pattern'] or complexity_info['recursive_calls'] > 1:
        return 'np'
    
    # 检查递归
    if complexity_info['has_recursion']:
        if complexity_info['has_binary_search']:
            return 'logn'
        # 递归函数的复杂度
        # 简单递归（如阶乘）是线性复杂度
        # 嵌套递归（如斐波那契）是指数复杂度
        if complexity_info['recursive_calls'] == 1:
            return 'linear'  # 单次递归调用，线性复杂度
        else:
            return 'np'  # 多次递归调用，指数复杂度
    
    # 检查是否有排序算法
    if complexity_info['has_sorting_algorithm']:
        # 排序算法通常是O(nlogn)，除非是冒泡排序等O(n²)算法
        sorting_method_calls = [call for call in complexity_info['method_calls'] if 'sort' in call]
        has_quadratic_sorting = any(call in ['bubblesort', 'insertionsort', 'selectionsort'] for call in sorting_method_calls)
        
        if has_quadratic_sorting:
            return 'quadratic'
        else:
            # 检查是否有额外的循环
            if complexity_info['max_loop_depth'] == 1:
                return 'nlogn'
            elif complexity_info['max_loop_depth'] == 2:
                return 'nlogn'  # O(nlogn) + O(n) 还是 O(nlogn)
    
    # 检查循环深度和类型
    max_depth = complexity_info['max_loop_depth']
    
    # 检查是否有二分查找模式
    if complexity_info['has_binary_search']:
        if max_depth == 0:
            # 递归二分查找
            return 'logn'
        elif max_depth == 1:
            return 'logn'
        elif max_depth == 2:
            return 'nlogn'  # 例如：for循环 + 二分查找
    
    # 特殊处理：直接检查是否为对数复杂度
    # 只有当明确检测到对数循环模式时，才返回logn
    if max_depth == 1:
        # 单层循环，检查是否为对数循环
        # 只信任has_logarithmic_loop标志，不使用过于激进的启发式
        if complexity_info['has_logarithmic_loop']:
            return 'logn'
    
    # 检查是否有对数循环
    if complexity_info['has_logarithmic_loop']:
        if max_depth == 1:
            return 'logn'
        elif max_depth == 2:
            return 'nlogn'  # 外层线性循环 + 内层对数循环
    
    # 额外检查特殊模式
    if complexity_info['has_quadratic_pattern'] and max_depth >= 2:
        return 'quadratic'
    elif complexity_info['has_cubic_pattern'] and max_depth >= 3:
        return 'cubic'
    
    # 根据循环深度确定复杂度
    if max_depth == 0:
        # 无循环，检查是否有递归
        if complexity_info['has_recursion']:
            return 'linear'  # 递归函数，无循环，线性复杂度
        return 'constant'  # 无循环，常数复杂度
    elif max_depth == 1:
        # 特殊检查：如果是单层for循环，可能是对数复杂度
        # 这里我们直接返回linear，因为对数复杂度已经在前面检查过了
        return 'linear'    # 单层循环，线性复杂度
    elif max_depth == 2:
        return 'quadratic'  # 两层循环，平方复杂度
    elif max_depth == 3:
        return 'cubic'      # 三层循环，立方复杂度
    else:
        return 'np'         # 四层及以上循环，视为NP复杂度

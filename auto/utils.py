#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
包含常量定义、通用工具函数和异常类
"""

# 支持的时间复杂度类型
COMPLEXITY_TYPES = {
    "constant": 0,
    "linear": 1,
    "logn": 2,
    "nlogn": 3,
    "quadratic": 4,
    "cubic": 5,
    "np": 6
}

# 错误类型
class AnalysisError(Exception):
    """分析过程中的异常类"""
    pass

class DataFormatError(Exception):
    """数据格式错误异常类"""
    pass

class FileReadError(Exception):
    """文件读取错误异常类"""
    pass


def get_complexity_type(complexity_str):
    """
    获取复杂度类型的数值表示
    
    Args:
        complexity_str (str): 复杂度字符串
    
    Returns:
        int: 复杂度数值表示
    """
    return COMPLEXITY_TYPES.get(complexity_str, -1)


def validate_complexity(complexity_str):
    """
    验证复杂度类型是否合法
    
    Args:
        complexity_str (str): 复杂度字符串
    
    Returns:
        bool: 是否为合法复杂度类型
    """
    return complexity_str in COMPLEXITY_TYPES

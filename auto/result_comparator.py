#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
结果比较与统计模块
将分析得到的时间复杂度与数据集中自带的复杂度标签进行比较，计算统计指标
"""

from typing import List, Dict, Any, Tuple
from utils import validate_complexity


def compare_results(results: List[Dict[str, Any]]) -> Tuple[Dict[str, float], Dict[str, Any]]:
    """
    比较分析结果与预期复杂度，计算统计指标
    
    Args:
        results (List[Dict[str, Any]]): 包含分析结果的列表，每个元素包含expected_complexity和output字段
    
    Returns:
        Tuple[Dict[str, float], Dict[str, Any]]: 
            - 第一个字典包含整体统计指标
            - 第二个字典包含按复杂度类型的详细统计
    """
    # 初始化统计变量
    total_samples = len(results)
    correct_samples = 0
    total_by_class = {}
    correct_by_class = {}
    predicted_by_class = {}
    
    # 统计结果
    for result in results:
        expected = result['expected_complexity']
        predicted = result['output']
        is_match = result['is_match']
        
        # 更新总统计
        if is_match:
            correct_samples += 1
        
        # 更新按类别统计
        total_by_class[expected] = total_by_class.get(expected, 0) + 1
        predicted_by_class[predicted] = predicted_by_class.get(predicted, 0) + 1
        if is_match:
            correct_by_class[expected] = correct_by_class.get(expected, 0) + 1
    
    # 计算整体准确率
    accuracy = correct_samples / total_samples if total_samples > 0 else 0.0
    
    # 计算按类别统计的精确率、召回率和F1分数
    class_stats = {}
    for complexity in total_by_class.keys():
        # 真实正例（TP）：该类被正确预测为该类
        tp = correct_by_class.get(complexity, 0)
        
        # 假负例（FN）：该类被错误预测为其他类
        fn = total_by_class[complexity] - tp
        
        # 假正例（FP）：其他类被错误预测为该类
        fp = predicted_by_class.get(complexity, 0) - tp
        
        # 计算精确率、召回率和F1分数
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        class_stats[complexity] = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'support': total_by_class[complexity]
        }
    
    # 计算宏平均和微平均
    macro_precision = sum(stats['precision'] for stats in class_stats.values()) / len(class_stats) if class_stats else 0.0
    macro_recall = sum(stats['recall'] for stats in class_stats.values()) / len(class_stats) if class_stats else 0.0
    macro_f1 = sum(stats['f1_score'] for stats in class_stats.values()) / len(class_stats) if class_stats else 0.0
    
    # 微平均与准确率相同
    micro_precision = accuracy
    micro_recall = accuracy
    micro_f1 = accuracy
    
    # 组装整体统计指标
    overall_stats = {
        'accuracy': accuracy,
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'macro_f1': macro_f1,
        'micro_precision': micro_precision,
        'micro_recall': micro_recall,
        'micro_f1': micro_f1,
        'total_samples': total_samples,
        'correct_samples': correct_samples
    }
    
    return overall_stats, class_stats


def generate_statistics_report(results: List[Dict[str, Any]]) -> str:
    """
    生成详细的统计报告
    
    Args:
        results (List[Dict[str, Any]]): 包含分析结果的列表
    
    Returns:
        str: 格式化的统计报告字符串
    """
    overall_stats, class_stats = compare_results(results)
    
    # 生成报告
    report = []
    report.append("=" * 60)
    report.append("时间复杂度分析结果统计报告")
    report.append("=" * 60)
    report.append(f"总样本数: {overall_stats['total_samples']}")
    report.append(f"正确样本数: {overall_stats['correct_samples']}")
    report.append(f"准确率: {overall_stats['accuracy']:.4f}")
    report.append("")
    report.append("宏平均指标:")
    report.append(f"  精确率: {overall_stats['macro_precision']:.4f}")
    report.append(f"  召回率: {overall_stats['macro_recall']:.4f}")
    report.append(f"  F1分数: {overall_stats['macro_f1']:.4f}")
    report.append("")
    report.append("微平均指标:")
    report.append(f"  精确率: {overall_stats['micro_precision']:.4f}")
    report.append(f"  召回率: {overall_stats['micro_recall']:.4f}")
    report.append(f"  F1分数: {overall_stats['micro_f1']:.4f}")
    report.append("")
    report.append("按复杂度类型的详细统计:")
    report.append("-" * 60)
    report.append(f"{'复杂度类型':<15} {'精确率':<10} {'召回率':<10} {'F1分数':<10} {'支持数':<8}")
    report.append("-" * 60)
    
    # 按复杂度类型排序输出
    for complexity in sorted(class_stats.keys()):
        stats = class_stats[complexity]
        report.append(f"{complexity:<15} {stats['precision']:<10.4f} {stats['recall']:<10.4f} {stats['f1_score']:<10.4f} {stats['support']:<8}")
    
    report.append("=" * 60)
    
    return '\n'.join(report)


def compare_individual_result(expected: str, predicted: str) -> bool:
    """
    比较单个结果，判断预测是否正确
    
    Args:
        expected (str): 预期复杂度
        predicted (str): 预测的复杂度
    
    Returns:
        bool: 预测是否正确
    """
    # 验证复杂度类型合法性
    if not validate_complexity(expected) or not validate_complexity(predicted):
        return False
    
    return expected == predicted

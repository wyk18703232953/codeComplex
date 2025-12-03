#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试结果比较与统计模块
"""

import unittest
from result_comparator import compare_individual_result, compare_results, generate_statistics_report


class TestResultComparator(unittest.TestCase):
    """测试结果比较与统计功能"""
    
    def test_compare_individual_result_match(self):
        """测试比较单个匹配结果"""
        result = compare_individual_result("linear", "linear")
        self.assertTrue(result)
    
    def test_compare_individual_result_mismatch(self):
        """测试比较单个不匹配结果"""
        result = compare_individual_result("linear", "quadratic")
        self.assertFalse(result)
    
    def test_compare_individual_result_invalid(self):
        """测试比较无效的复杂度类型"""
        result = compare_individual_result("linear", "invalid_type")
        self.assertFalse(result)
    
    def test_compare_results(self):
        """测试比较多个结果"""
        results = [
            {
                "sample_id": 1,
                "expected_complexity": "constant",
                "output": "constant",
                "is_match": True
            },
            {
                "sample_id": 2,
                "expected_complexity": "linear",
                "output": "linear",
                "is_match": True
            },
            {
                "sample_id": 3,
                "expected_complexity": "quadratic",
                "output": "linear",
                "is_match": False
            }
        ]
        
        overall_stats, class_stats = compare_results(results)
        
        # 测试整体统计
        self.assertEqual(overall_stats['total_samples'], 3)
        self.assertEqual(overall_stats['correct_samples'], 2)
        self.assertEqual(overall_stats['accuracy'], 2/3)
        
        # 测试按类别统计
        self.assertIn("constant", class_stats)
        self.assertIn("linear", class_stats)
        self.assertIn("quadratic", class_stats)
        self.assertEqual(class_stats["constant"]["support"], 1)
        self.assertEqual(class_stats["linear"]["support"], 1)
        self.assertEqual(class_stats["quadratic"]["support"], 1)
    
    def test_generate_statistics_report(self):
        """测试生成统计报告"""
        results = [
            {
                "sample_id": 1,
                "expected_complexity": "constant",
                "output": "constant",
                "is_match": True
            },
            {
                "sample_id": 2,
                "expected_complexity": "linear",
                "output": "linear",
                "is_match": True
            }
        ]
        
        report = generate_statistics_report(results)
        self.assertIn("时间复杂度分析结果统计报告", report)
        self.assertIn("总样本数: 2", report)
        self.assertIn("准确率: 1.0000", report)
    
    def test_empty_results(self):
        """测试空结果列表"""
        results = []
        overall_stats, class_stats = compare_results(results)
        
        self.assertEqual(overall_stats['total_samples'], 0)
        self.assertEqual(overall_stats['accuracy'], 0.0)
        self.assertEqual(len(class_stats), 0)
        
        report = generate_statistics_report(results)
        self.assertIn("总样本数: 0", report)


if __name__ == '__main__':
    unittest.main()

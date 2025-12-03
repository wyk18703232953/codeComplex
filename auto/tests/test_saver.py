#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试结果保存模块
"""

import unittest
import tempfile
import os
import json
from result_saver import save_results, format_result


class TestResultSaver(unittest.TestCase):
    """测试结果保存功能"""
    
    def test_format_result(self):
        """测试格式化单个结果"""
        result = format_result(
            sample_id=1,
            problem="Test problem",
            source="public class Test {}",
            expected_complexity="constant",
            output="constant",
            is_match=True
        )
        
        # 测试结果格式
        self.assertEqual(result['sample_id'], 1)
        self.assertEqual(result['problem'], "Test problem")
        self.assertEqual(result['source'], "public class Test {}")
        self.assertEqual(result['expected_complexity'], "constant")
        self.assertEqual(result['output'], "constant")
        self.assertTrue(result['is_match'])
        self.assertIsNone(result['error'])
        
        # 测试带错误信息的结果
        result_with_error = format_result(
            sample_id=2,
            problem="Test problem 2",
            source="invalid java code",
            expected_complexity="linear",
            output="error",
            is_match=False,
            error="Java syntax error"
        )
        
        self.assertEqual(result_with_error['error'], "Java syntax error")
        self.assertFalse(result_with_error['is_match'])
    
    def test_save_results(self):
        """测试保存结果到文件"""
        results = [
            format_result(
                sample_id=1,
                problem="Test 1",
                source="public class Test1 {}",
                expected_complexity="constant",
                output="constant",
                is_match=True
            ),
            format_result(
                sample_id=2,
                problem="Test 2",
                source="public class Test2 {}",
                expected_complexity="linear",
                output="linear",
                is_match=True
            )
        ]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = save_results(results, temp_dir)
            file_path = os.path.join(temp_dir, filename)
            
            # 测试文件是否存在
            self.assertTrue(os.path.exists(file_path))
            
            # 测试文件名格式
            self.assertIn("complexity_validation_auto_results_", filename)
            self.assertIn(".json", filename)
            
            # 测试文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            # 检查文件结构
            self.assertIn("summary", saved_data)
            self.assertIn("detailed_records", saved_data)
            
            # 检查详细记录
            detailed_records = saved_data["detailed_records"]
            self.assertEqual(len(detailed_records), 2)
            self.assertEqual(detailed_records[0]['sample_id'], 1)
            self.assertEqual(detailed_records[1]['expected_complexity'], "linear")
            
            # 检查summary
            summary = saved_data["summary"]
            self.assertEqual(summary["total"], 2)
            self.assertEqual(summary["correct"], 2)
            self.assertEqual(summary["failed"], 0)
    
    def test_save_results_default_dir(self):
        """测试使用默认目录保存结果"""
        results = [
            format_result(
                sample_id=1,
                problem="Test",
                source="public class Test {}",
                expected_complexity="constant",
                output="constant",
                is_match=True
            )
        ]
        
        # 保存到当前目录
        filename = save_results(results)
        
        try:
            # 测试文件是否存在
            self.assertTrue(os.path.exists(filename))
        finally:
            # 清理测试文件
            if os.path.exists(filename):
                os.unlink(filename)


if __name__ == '__main__':
    unittest.main()

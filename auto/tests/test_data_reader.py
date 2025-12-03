#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据读取模块
"""

import unittest
import tempfile
import os
from data_reader import read_jsonl_file, extract_java_samples, FileReadError, DataFormatError


class TestDataReader(unittest.TestCase):
    """测试数据读取功能"""
    
    def setUp(self):
        """创建临时测试文件"""
        # 创建有效的JSONL测试数据
        self.valid_jsonl = """
{"sample_id": 1, "problem": "Test 1", "source": "public class Test1 {}", "expected_complexity": "constant"}
{"sample_id": 2, "problem": "Test 2", "source": "public class Test2 {}", "expected_complexity": "linear"}
{"sample_id": 3, "problem": "Test 3", "source": "public class Test3 {}", "expected_complexity": "quadratic"}
        """
        
        # 创建无效的JSONL测试数据
        self.invalid_jsonl = """
{"sample_id": 1, "problem": "Test 1", "source": "public class Test1 {}", "expected_complexity": "constant"}
invalid json line
{"sample_id": 3, "problem": "Test 3", "source": "public class Test3 {}", "expected_complexity": "quadratic"}
        """
        
        # 创建缺少字段的JSONL测试数据
        self.missing_fields_jsonl = """
{"sample_id": 1, "source": "public class Test1 {}", "expected_complexity": "constant"}
{"sample_id": 2, "problem": "Test 2", "expected_complexity": "linear"}
{"sample_id": 3, "problem": "Test 3", "source": "public class Test3 {}"}
        """
    
    def test_read_valid_jsonl(self):
        """测试读取有效的JSONL文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            f.write(self.valid_jsonl)
            temp_file = f.name
        
        try:
            samples = list(read_jsonl_file(temp_file))
            self.assertEqual(len(samples), 3)
            self.assertEqual(samples[0]['sample_id'], 1)
            self.assertEqual(samples[1]['expected_complexity'], "linear")
        finally:
            os.unlink(temp_file)
    
    def test_read_invalid_jsonl(self):
        """测试读取无效的JSONL文件"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            f.write(self.invalid_jsonl)
            temp_file = f.name
        
        try:
            with self.assertRaises(DataFormatError):
                list(read_jsonl_file(temp_file))
        finally:
            os.unlink(temp_file)
    
    def test_extract_valid_samples(self):
        """测试从有效JSONL中提取样本"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            f.write(self.valid_jsonl)
            temp_file = f.name
        
        try:
            samples = list(extract_java_samples(temp_file))
            self.assertEqual(len(samples), 3)
            self.assertEqual(samples[0]['sample_id'], 1)
            self.assertEqual(samples[1]['problem'], "Test 2")
            self.assertEqual(samples[2]['expected_complexity'], "quadratic")
        finally:
            os.unlink(temp_file)
    
    def test_extract_missing_fields(self):
        """测试从缺少字段的JSONL中提取样本"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            f.write(self.missing_fields_jsonl)
            temp_file = f.name
        
        try:
            # 期望从缺少字段的JSONL中提取样本会抛出异常
            with self.assertRaises(DataFormatError):
                list(extract_java_samples(temp_file))
        finally:
            os.unlink(temp_file)
    
    def test_file_not_found(self):
        """测试读取不存在的文件"""
        with self.assertRaises(FileReadError):
            list(read_jsonl_file("non_existent_file.jsonl"))


if __name__ == '__main__':
    unittest.main()

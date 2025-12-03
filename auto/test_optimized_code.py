#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的代码功能
"""

import sys
import os
from java_complexity_analyzer import analyze_java_complexity
from result_saver import save_results, format_result

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath('.'))


def test_complexity_analyzer():
    """
    测试优化后的复杂度分析功能
    """
    print("=== 测试复杂度分析功能 ===")
    
    # 测试用例1：常数复杂度
    constant_code = """
    public class Test {
        public static void main(String[] args) {
            int a = 5;
            int b = 10;
            int sum = a + b;
            System.out.println(sum);
        }
    }
    """
    
    # 测试用例2：线性复杂度
    linear_code = """
    public class Test {
        public static void main(String[] args) {
            int[] arr = {1, 2, 3, 4, 5};
            for (int i = 0; i < arr.length; i++) {
                System.out.println(arr[i]);
            }
        }
    }
    """
    
    # 测试用例3：对数复杂度（i *= 2）
    logn_code = """
    public class Test {
        public static void main(String[] args) {
            for (int i = 1; i < 100; i *= 2) {
                System.out.println(i);
            }
        }
    }
    """
    
    # 测试用例4：nlogn复杂度（排序算法）
    nlogn_code = """
    import java.util.Arrays;
    
    public class Test {
        public static void main(String[] args) {
            int[] arr = {5, 3, 1, 4, 2};
            Arrays.sort(arr);
            for (int num : arr) {
                System.out.println(num);
            }
        }
    }
    """
    
    # 测试用例5：平方复杂度
    quadratic_code = """
    public class Test {
        public static void main(String[] args) {
            int[][] matrix = {{1, 2}, {3, 4}};
            for (int i = 0; i < matrix.length; i++) {
                for (int j = 0; j < matrix[i].length; j++) {
                    System.out.println(matrix[i][j]);
                }
            }
        }
    }
    """
    
    test_cases = [
        (constant_code, "constant", "常数复杂度"),
        (linear_code, "linear", "线性复杂度"),
        (logn_code, "logn", "对数复杂度"),
        (nlogn_code, "nlogn", "nlogn复杂度"),
        (quadratic_code, "quadratic", "平方复杂度")
    ]
    
    for code, expected, description in test_cases:
        try:
            result = analyze_java_complexity(code)
            status = "✓" if result == expected else "✗"
            print(f"{status} {description}: 预期={expected}, 结果={result}")
        except Exception as e:
            print(f"✗ {description}: 错误 - {e}")
    
    print()


def test_result_saver():
    """
    测试优化后的结果保存功能
    """
    print("=== 测试结果保存功能 ===")
    
    # 创建测试结果
    test_results = [
        format_result(
            sample_id=1,
            problem="Test Problem 1",
            source="CODEFORCES",
            expected_complexity="constant",
            output="constant",
            is_match=True
        ),
        format_result(
            sample_id=2,
            problem="Test Problem 2",
            source="CODEFORCES",
            expected_complexity="linear",
            output="linear",
            is_match=True
        ),
        format_result(
            sample_id=3,
            problem="Test Problem 3",
            source="CODEFORCES",
            expected_complexity="nlogn",
            output="linear",
            is_match=False
        )
    ]
    
    try:
        # 保存结果
        filename = save_results(test_results, output_dir=".", input_file="./data.jsonl", max_items=3)
        print(f"✓ 结果保存成功，文件名：{filename}")
        
        # 验证文件存在
        if os.path.exists(filename):
            print(f"✓ 文件 {filename} 存在")
            
            # 读取并验证文件内容
            import json
            with open(filename, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            # 验证结构
            if "summary" in saved_data and "detailed_records" in saved_data:
                print("✓ 文件结构符合规范")
                
                # 验证summary内容
                summary = saved_data["summary"]
                expected_summary_keys = ["total", "correct", "failed", "accuracy", "timestamp"]
                if all(key in summary for key in expected_summary_keys):
                    print(f"✓ Summary包含所有必要字段")
                    print(f"  统计信息：总样本={summary['total']}, 正确={summary['correct']}, 失败={summary['failed']}, 准确率={summary['accuracy']}%")
                
                # 验证detailed_records内容
                detailed_records = saved_data["detailed_records"]
                if len(detailed_records) == len(test_results):
                    print(f"✓ Detailed_records包含 {len(detailed_records)} 条记录")
                    
                    # 验证字段名
                    sample_record = detailed_records[0]
                    if "ouput" in sample_record:  # 注意：示例中是ouput，不是output
                        print("✓ 记录字段名符合规范（使用ouput而非output）")
        
        # 清理测试文件
        if os.path.exists(filename):
            os.remove(filename)
            print(f"✓ 测试文件已清理")
            
    except Exception as e:
        print(f"✗ 结果保存失败：{e}")
    
    print()


if __name__ == "__main__":
    test_complexity_analyzer()
    test_result_saver()
    print("=== 测试完成 ===")

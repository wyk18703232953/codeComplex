#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试复杂度分析模块
"""

import unittest
from java_complexity_analyzer import analyze_java_complexity, AnalysisError


class TestJavaComplexityAnalyzer(unittest.TestCase):
    """测试Java代码复杂度分析功能"""
    
    def test_constant_complexity(self):
        """测试常数复杂度代码"""
        java_code = """
        public class Test {
            public static void main(String[] args) {
                int a = 5;
                int b = 10;
                int sum = a + b;
                System.out.println(sum);
            }
        }
        """
        result = analyze_java_complexity(java_code)
        self.assertEqual(result, "constant")
    
    def test_linear_complexity(self):
        """测试线性复杂度代码"""
        java_code = """
        public class Test {
            public static void main(String[] args) {
                int[] arr = {1, 2, 3, 4, 5};
                for (int i = 0; i < arr.length; i++) {
                    System.out.println(arr[i]);
                }
            }
        }
        """
        result = analyze_java_complexity(java_code)
        self.assertEqual(result, "linear")
    
    def test_quadratic_complexity(self):
        """测试平方复杂度代码"""
        java_code = """
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
        result = analyze_java_complexity(java_code)
        self.assertEqual(result, "quadratic")
    
    def test_cubic_complexity(self):
        """测试立方复杂度代码"""
        java_code = """
        public class Test {
            public static void main(String[] args) {
                int[][][] cube = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}}; 
                for (int i = 0; i < cube.length; i++) {
                    for (int j = 0; j < cube[i].length; j++) {
                        for (int k = 0; k < cube[i][j].length; k++) {
                            System.out.println(cube[i][j][k]);
                        }
                    }
                }
            }
        }
        """
        result = analyze_java_complexity(java_code)
        self.assertEqual(result, "cubic")
    
    def test_invalid_java_code(self):
        """测试无效Java代码"""
        invalid_code = """
        public class Test {
            public static void main(String[] args) {
                System.out.println("Hello";
            }
        }
        """
        with self.assertRaises(AnalysisError):
            analyze_java_complexity(invalid_code)
    
    def test_recursive_function(self):
        """测试递归函数"""
        recursive_code = """
        public class Test {
            public static void main(String[] args) {
                int result = factorial(5);
                System.out.println(result);
            }
            
            public static int factorial(int n) {
                if (n <= 1) {
                    return 1;
                }
                return n * factorial(n - 1);
            }
        }
        """
        result = analyze_java_complexity(recursive_code)
        self.assertEqual(result, "linear")
    
    def test_binary_search(self):
        """测试二分查找算法"""
        binary_search_code = """
        public class Test {
            public static void main(String[] args) {
                int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9};
                int target = 5;
                int result = binarySearch(arr, target);
                System.out.println(result);
            }
            
            public static int binarySearch(int[] arr, int target) {
                int left = 0;
                int right = arr.length - 1;
                while (left <= right) {
                    int mid = left + (right - left) / 2;
                    if (arr[mid] == target) {
                        return mid;
                    } else if (arr[mid] < target) {
                        left = mid + 1;
                    } else {
                        right = mid - 1;
                    }
                }
                return -1;
            }
        }
        """
        result = analyze_java_complexity(binary_search_code)
        self.assertEqual(result, "logn")


if __name__ == '__main__':
    unittest.main()

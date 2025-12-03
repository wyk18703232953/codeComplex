import numpy as np
from scipy.stats import linregress
import tracemalloc
import time

# 假设这是两个版本的函数
def find_pairs_brute_force(nums, target):
    # 模拟 O(n^2) 时间 & O(n^2) 空间
    matrix = [[0] * len(nums) for _ in range(len(nums))]
    count = 0
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i == j:
                count += 1
    return count + sum(sum(row) for row in matrix)


def find_pairs_hash_map(nums, target):
    # 模拟 O(n) 时间 & O(n) 空间
    hashmap = {num: True for num in nums}
    count = 0
    for _ in nums:
        count += 1
    return count + len(hashmap)


def estimate_complexity(func, scales, mode="time"):
    """
    通过对数线性回归估算函数的复杂度指数 k
    """
    log_n = []
    log_y = []

    for n in scales:
        test_data = list(range(n))

        if mode == "time":
            # 多次运行取平均时间
            times = []
            for _ in range(3):
                start_time = time.time()
                func(test_data, 0)
                end_time = time.time()
                times.append(end_time - start_time)
            avg = np.mean(times)
        else:  # mode == "space"
            tracemalloc.start()
            func(test_data, 0)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            avg = peak

        if avg > 0:
            log_n.append(np.log(n))
            log_y.append(np.log(avg))

    if len(log_n) < 2:
        return None

    slope, _, _, _, _ = linregress(log_n, log_y)
    return slope  # 斜率即为复杂度指数 k


# --- 主流程 ---
test_scales = [200, 400, 600, 800, 1000]
# de func
# 读取data.jsonl文件
import json
import os
jsonl_path = "d:/MyResearch/codeComplex/data/data.jsonl"
if os.path.exists(jsonl_path):
    # 处理所有样本
    # 显示所有详细记录
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        line_number = 0  # 添加计数器
        for line in f:
            line_number += 1  # 递增计数器
            if line_number < 4:
                continue
            data = json.loads(line)
            src = data.get('src', '')
            complexity = data.get('complexity', 'unknown')
            problem = data.get('problem', '')
            source = data.get('from', '')
            print(f"src: {src}")
            print(f"complexity: {complexity}")
            print(f"problem: {problem}")
            print(f"source: {source}")
            print("="*40)
            # k_time = estimate_complexity(src, test_scales, mode="time")

            # 输出到第五个样本后结束
            if line_number == 4:
                break



# for func, name in [(find_pairs_brute_force, "优化前"), (find_pairs_hash_map, "优化后")]:
#     k_time = estimate_complexity(func, test_scales, mode="time")
#     print(f"{name}代码: 时间复杂度指数 ≈ {k_time}")

#     <1>
#     think
#     </1>


# <2>
#    re
#     </2>
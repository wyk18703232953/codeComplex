import numpy as np
from scipy.stats import linregress
import time
import matplotlib.pyplot as plt

# 假设这是两个版本的函数
def find_pairs_brute_force(nums, target):
    # 模拟 O(n^2) 时间复杂度
    # 保留必要的操作以确保时间复杂度特征明显
    count = 0
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i <= j:  # 确保有实际计算工作
                count += i + j
    return count


def find_pairs_hash_map(nums, target):
    # 模拟 O(n) 时间复杂度
    seen = set()
    count = 0
    for num in nums:
        complement = target - num
        if complement in seen:
            count += 1
        seen.add(num)
    return count


def estimate_time_complexity(func, scales, num_runs=5, min_time=0.001):
    """
    通过对数线性回归精确估算函数的时间复杂度指数 k
    
    参数:
    - func: 要测试的函数
    - scales: 输入规模的列表
    - num_runs: 每个规模下的运行次数，取平均值减少噪声
    - min_time: 最小运行时间阈值，确保测量准确
    
    返回:
    - complexity_info: 包含复杂度指数、统计信息和时间测量结果的字典
    """
    execution_times = []
    log_n = []
    log_times = []
    results = []
    
    for n in scales:
        test_data = list(range(n))
        total_time = 0
        actual_runs = 0
        
        # 确保每个规模的运行时间足够长以获得准确测量
        while total_time < min_time and actual_runs < num_runs * 10:  # 最多运行num_runs*10次
            start_time = time.time()
            func(test_data, 0)  # 传入target=0
            end_time = time.time()
            
            run_time = end_time - start_time
            total_time += run_time
            actual_runs += 1
        
        avg_time = total_time / actual_runs
        execution_times.append(avg_time)
        results.append({
            'n': n,
            'avg_time': avg_time,
            'runs': actual_runs
        })
        
        # 记录对数数据用于线性回归
        if avg_time > 0:
            log_n.append(np.log(n))
            log_times.append(np.log(avg_time))
    
    # 执行对数线性回归
    if len(log_n) >= 2:
        slope, intercept, r_value, p_value, std_err = linregress(log_n, log_times)
        
        # 根据斜率推断时间复杂度类型
        complexity_type = classify_complexity(slope)
        
        return {
            'slope': slope,  # 复杂度指数k
            'intercept': intercept,
            'r_squared': r_value ** 2,  # 决定系数，衡量拟合质量
            'p_value': p_value,
            'std_err': std_err,
            'complexity_type': complexity_type,
            'measurements': results,
            'execution_times': execution_times
        }
    else:
        return None

def classify_complexity(slope, tolerance=0.3):
    """
    根据复杂度指数k对时间复杂度进行分类
    
    参数:
    - slope: 复杂度指数k
    - tolerance: 分类的容差范围
    
    返回:
    - 复杂度类型的字符串表示
    """
    if abs(slope - 0) < tolerance:
        return "O(1) - 常数时间"
    elif abs(slope - 1) < tolerance:
        return "O(n) - 线性时间"
    elif abs(slope - 2) < tolerance:
        return "O(n²) - 平方时间"
    elif abs(slope - 3) < tolerance:
        return "O(n³) - 立方时间"
    elif abs(slope - 0.5) < tolerance:
        return "O(√n) - 平方根时间"
    elif abs(slope - np.log2(2)) < tolerance:
        return "O(log n) - 对数时间"
    elif abs(slope - 1.5) < tolerance:
        return "O(n log n) - 线性对数时间"
    elif slope > 3:
        return f"O(n^{slope:.2f}) - 多项式时间"
    else:
        return f"O(n^{slope:.2f}) - 未知复杂度模式"

def plot_time_complexity(results, func_name):
    """
    可视化时间复杂度测量结果
    
    参数:
    - results: estimate_time_complexity函数的返回结果
    - func_name: 函数名称，用于图表标题
    """
    if not results:
        return
    
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    
    # 提取数据
    n_values = [m['n'] for m in results['measurements']]
    times = [m['avg_time'] for m in results['measurements']]
    
    # 创建图形
    plt.figure(figsize=(10, 6))
    
    # 绘制实际测量值
    plt.scatter(n_values, times, color='blue', label='实际测量时间')
    
    # 绘制拟合曲线
    fit_times = [np.exp(results['intercept']) * (n ** results['slope']) for n in n_values]
    plt.plot(n_values, fit_times, color='red', linestyle='--', label='拟合曲线')
    
    # 设置对数-对数坐标以更好地显示复杂度
    plt.xscale('log')
    plt.yscale('log')
    
    # 添加标签和标题
    plt.xlabel('输入规模 (n)')
    plt.ylabel('执行时间 (秒)')
    plt.title(f'{func_name} 的时间复杂度分析\n{results["complexity_type"]}, 复杂度指数 k = {results["slope"]:.3f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 保存图表
    plt.savefig(f'complexity_plot_{func_name.replace(" ", "_")}.png')
    plt.close()


# --- 主流程 ---
# 使用更大的规模范围以获得更准确的复杂度估计
test_scales = [100, 200, 400, 800, 1600, 3200]

print("=== 时间复杂度分析报告 ===")
print()

for func, name in [(find_pairs_brute_force, "暴力搜索方法"), (find_pairs_hash_map, "哈希表优化方法")]:
    print(f"\n分析 {name} 的时间复杂度...")
    
    # 估算时间复杂度
    result = estimate_time_complexity(func, test_scales)
    
    if result:
        print(f"复杂度指数 k ≈ {result['slope']:.3f}")
        print(f"推断的复杂度类型: {result['complexity_type']}")
        print(f"拟合优度 R² = {result['r_squared']:.4f}")
        print(f"标准误差 = {result['std_err']:.4f}")
        print()
        print("详细测量结果:")
        print("{:<10} {:<15} {:<10}".format('输入规模n', '平均执行时间(秒)', '运行次数'))
        print("-" * 40)
        for measurement in result['measurements']:
            print(f"{measurement['n']:<10} {measurement['avg_time']:<15.9f} {measurement['runs']:<10}")
        
        # 可视化结果
        try:
            plot_time_complexity(result, name)
            print(f"\n复杂度分析图表已保存: complexity_plot_{name.replace(' ', '_')}.png")
        except Exception as e:
            print(f"\n警告: 无法生成可视化图表: {e}")
    else:
        print("无法估算复杂度，请增加测试规模或运行次数。")

print("\n=== 分析完成 ===")
print("注意: 复杂度估算基于实验测量，可能受到环境因素影响。")
print("对于小输入规模，常数因子和系统开销可能导致估算不准确。")
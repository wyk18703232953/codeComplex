#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序入口
协调整个分析流程：数据读取、复杂度分析、结果比较、统计计算和结果保存
"""

import sys
import logging
from typing import List, Dict, Any
from data_reader import extract_java_samples, FileReadError, DataFormatError
from java_complexity_analyzer import analyze_java_complexity, AnalysisError
from result_comparator import compare_individual_result, generate_statistics_report
from result_saver import save_results, format_result

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main(data_file: str = '../data/data.jsonl', output_dir: str = '.') -> None:
    """
    主程序入口，执行完整的分析流程
    
    Args:
        data_file (str, optional): JSONL数据集文件路径，默认为'./data.jsonl'
        output_dir (str, optional): 输出结果目录路径，默认为当前目录
    """
    logger.info("=== 开始Java代码时间复杂度分析与验证 ===")
    
    results = []
    
    try:
        # 1. 读取数据
        logger.info(f"1. 正在读取数据文件: {data_file}")
        samples = list(extract_java_samples(data_file))
        total_samples = len(samples)
        logger.info(f"   成功读取 {total_samples} 个Java代码样本")
        
        # 2. 复杂度分析
        logger.info("2. 正在进行复杂度分析...")
        for i, sample in enumerate(samples, 1):
            logger.info(f"   分析样本 {i}/{total_samples} (ID: {sample['sample_id']})")
            
            sample_id = sample['sample_id']
            problem = sample['problem']
            source = sample['source']
            expected_complexity = sample['expected_complexity']
            
            try:
                # 分析Java代码复杂度
                output = analyze_java_complexity(source)
                error = None
                
                # 比较结果
                is_match = compare_individual_result(expected_complexity, output)
                
                logger.info(f"   样本 {sample_id}: 预期={expected_complexity}, 分析结果={output}, {'匹配' if is_match else '不匹配'}")
            except AnalysisError as e:
                # 处理分析错误
                output = "error"
                is_match = False
                error = str(e)
                logger.error(f"   样本 {sample_id}: 分析错误 - {error}")
            
            # 格式化结果
            result = format_result(
                sample_id=sample_id,
                problem=problem,
                source=source,
                expected_complexity=expected_complexity,
                output=output,
                is_match=is_match,
                error=error
            )
            results.append(result)
        
        # 3. 生成统计报告
        logger.info("3. 正在生成统计报告...")
        report = generate_statistics_report(results)
        logger.info(f"\n{report}")
        
        # 4. 保存结果
        logger.info("4. 正在保存结果...")
        filename = save_results(results, output_dir)
        logger.info(f"   结果已保存到文件: {filename}")
        
        logger.info("=== Java代码时间复杂度分析与验证完成 ===")
        
    except FileReadError as e:
        logger.error(f"文件读取错误: {str(e)}")
        sys.exit(1)
    except DataFormatError as e:
        logger.error(f"数据格式错误: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"意外错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # 支持命令行参数
    import argparse
    
    parser = argparse.ArgumentParser(description='Java代码时间复杂度分析与验证系统')
    parser.add_argument('--data', '-d', type=str, default='../data/data.jsonl',
                        help='JSONL数据集文件路径')
    parser.add_argument('--output', '-o', type=str, default='results',
                        help='输出结果目录路径')
    
    args = parser.parse_args()
    
    main(data_file=args.data, output_dir=args.output)

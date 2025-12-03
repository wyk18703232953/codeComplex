# Java代码时间复杂度分析与验证系统实现方案

## 目录结构设计
```
/d:/MyResearch/codeComplex/auto/
├── __init__.py              # 包初始化文件
├── complexity_analyzer.py   # 时间复杂度分析模块
├── data_reader.py           # 数据读取模块
├── result_comparator.py     # 结果比较与统计模块
├── main.py                  # 主程序入口
├── result_persistence.py    # 结果持久化模块
└── tests/                   # 单元测试目录
    ├── __init__.py
    ├── test_complexity_analyzer.py
    ├── test_data_reader.py
    ├── test_result_comparator.py
    └── test_result_persistence.py
```

## 模块设计与功能说明

### 1. complexity_analyzer.py - 时间复杂度分析模块
- **核心功能**：通过静态代码分析识别Java代码的时间复杂度
- **核心函数**：`analyze_complexity(source_code: str) -> str`
  - 接收Java源代码字符串
  - 返回时间复杂度标识（constant、linear、logn、nlogn、quadratic、cubic、np）
  - 包含完善的异常处理机制
- **实现思路**：
  - 识别循环结构（for、while、do-while）
  - 分析递归调用
  - 识别嵌套循环深度
  - 检测常见算法模式

### 2. data_reader.py - 数据读取模块
- **核心功能**：读取并解析JSONL格式的数据集文件
- **核心函数**：`read_data(file_path: str) -> List[Dict]`
  - 接收文件路径
  - 返回包含所有Java源代码样本及其关联元数据的列表
  - 优化读取性能，处理格式错误
- **实现思路**：
  - 使用逐行读取方式处理大文件
  - 对每行进行JSON解析和错误处理
  - 提取关键字段：src、complexity、problem、from

### 3. result_comparator.py - 结果比较与统计模块
- **核心功能**：比较分析结果与预期结果，计算统计指标
- **核心函数**：`compare_results(results: List[Dict]) -> Dict`
  - 接收分析结果列表
  - 返回包含统计指标的字典
- **统计指标**：
  - 准确性（Accuracy）
  - 精确率（Precision）
  - 召回率（Recall）
  - F1分数（F1-Score）
  - 各类复杂度的分类统计

### 4. main.py - 主程序入口
- **核心功能**：实现一键运行机制，按顺序执行各个模块
- **核心流程**：
  1. 读取数据
  2. 复杂度分析
  3. 结果比较
  4. 统计计算
  5. 结果保存
- **日志输出**：
  - 处理进度追踪
  - 错误信息记录
  - 统计结果展示

### 5. result_persistence.py - 结果持久化模块
- **核心功能**：将比较结果以标准化JSON格式保存到文件
- **核心函数**：`save_results(results: List[Dict]) -> str`
  - 接收结果列表
  - 生成符合格式要求的文件名
  - 保存结果到JSON文件
  - 返回生成的文件名
- **文件名格式**：`complexity_validation_auto_results_YYYYMMDD_HHMMSS.json`
- **文件内容字段**：
  - sample_id（整数类型）
  - problem（字符串类型）
  - source（字符串类型）
  - expected_complexity（字符串类型）
  - output（字符串类型）
  - is_match（布尔类型）
  - error（可为null或字符串类型）

## 开发规范遵循
- 符合Python PEP 8编码规范
- 包含必要的文档字符串
- 关键函数编写单元测试
- 所有代码文件放置在指定目录

## 实现顺序
1. 创建目录结构
2. 实现基础模块（data_reader.py, result_persistence.py）
3. 实现核心分析模块（complexity_analyzer.py）
4. 实现结果比较模块（result_comparator.py）
5. 实现主程序入口（main.py）
6. 编写单元测试
7. 集成测试和优化

## 技术栈
- Python 3.7+
- 标准库：json, os, sys, re, datetime, logging
- 第三方库：无（保持轻量级）
from services.prompt_manager import *
from services.llm_call_manager import *


def parse_bidding_product(input_text):
    prompt = get_prompt("bidding_product")
    response = llm_single_call(prompt + "\n\n" + input_text)
    expected_headers = ["招标单位", "产品名称", "产品数量", "产品预算单价(元)", "预算总金额(元)", "最高限价(元)"]
    result = parse_markdown_table(response, expected_headers)
    return result


def parse_winning_product(input_text):
    prompt = get_prompt("winning_product")
    response = llm_single_call(prompt + "\n\n" + input_text)
    expected_headers = ["招标单位", "供应商", "产品名称", "产品品牌", "产品型号", "产品数量", "产品单价(元)", "中标总价(元)"]
    result = parse_markdown_table(response, expected_headers)
    return result


def parse_markdown_table(markdown_table, expected_headers=None):
    """
    解析Markdown表格源代码，返回表格中的各个字段信息，并按照预期表头顺序排列
    支持模糊匹配表头

    参数:
        markdown_table (str): Markdown表格的源代码
        expected_headers (list, optional): 预期的表头列表，用于处理表头错误和顺序

    返回:
        list: 包含表格每行数据的字典列表，按照预期表头顺序排列
    """
    # 分割表格行
    lines = [line.strip() for line in markdown_table.strip().split('\n') if line.strip()]

    # 至少需要表头行和分隔行
    if len(lines) < 2:
        return []

    # 提取实际表头
    actual_headers = [header.strip() for header in lines[0].strip('|').split('|')]
    actual_headers = [h.strip() for h in actual_headers]

    # 如果没有提供预期表头，则使用实际表头
    if not expected_headers:
        expected_headers = expected_headers = actual_headers.copy()

    # 创建实际表头到预期表头的映射
    header_mapping = {}

    # 标准化表头以便于比较
    def normalize_header(header):
        """标准化表头，去除标点符号、空格，并转为小写"""
        import re
        # 去除标点符号和括号
        normalized = re.sub(r'[^\w\s]', '', header)
        # 去除多余空格
        normalized = re.sub(r'\s+', '', normalized)
        return normalized.lower()

    # 预处理标准化表头
    normalized_actual_headers = [normalize_header(h) for h in actual_headers]
    normalized_expected_headers = [normalize_header(h) for h in expected_headers]

    # 精确匹配和简单模糊匹配（使用标准化后的表头）
    for i, normalized_actual in enumerate(normalized_actual_headers):
        # 精确匹配标准化后的表头
        if normalized_actual in normalized_expected_headers:
            index = normalized_expected_headers.index(normalized_actual)
            header_mapping[i] = index
            continue

        # 模糊匹配1: 检查是否一个是另一个的子串
        for j, normalized_expected in enumerate(normalized_expected_headers):
            if normalized_actual in normalized_expected or normalized_expected in normalized_actual:
                header_mapping[i] = j
                break

    # 对于未匹配的表头，使用更复杂的模糊匹配
    for i, actual_header in enumerate(actual_headers):
        if i not in header_mapping:
            best_match = -1
            best_score = 0

            # 分词比较
            actual_words = set(normalize_header(actual_header).split())

            for j, expected_header in enumerate(expected_headers):
                expected_words = set(normalize_header(expected_header).split())

                # 计算共同词的数量
                common_words = actual_words.intersection(expected_words)

                # 计算相似度分数
                if len(actual_words) == 0 or len(expected_words) == 0:
                    continue

                # Jaccard相似度: 交集大小除以并集大小
                similarity = len(common_words) / len(actual_words.union(expected_words))

                if similarity > best_score:
                    best_score = similarity
                    best_match = j

            # 如果找到相似度高于阈值的匹配
            if best_score > 0.3:  # 可调整阈值
                header_mapping[i] = best_match
            elif i < len(expected_headers):
                # 如果没有找到好的匹配，使用相同位置
                header_mapping[i] = i

    # 处理数据行
    result = []

    for i in range(2, len(lines)):
        line = lines[i]
        # 跳过空行或只有分隔符的行
        if not line or line.strip() == '|':
            continue

        # 分割单元格
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        cells = [c.strip() for c in cells]

        # 创建行数据字典，初始化所有预期表头字段为空字符串
        row_data = {header: '' for header in expected_headers}

        # 根据映射填充数据
        for j in range(len(cells)):
            if j in header_mapping and header_mapping[j] < len(expected_headers):
                row_data[expected_headers[header_mapping[j]]] = cells[j]

        result.append(row_data)

    return result


# 使用示例
def test_markdown_parser():
    markdown_table = """
    | 产品品牌 | 供应商 | 招标单位 | 产品名称 | 中标总价 | 产品型号 | 产品数量 | 产品单价 |
    |----------|---------|---------|----------|----------|----------|----------|------------|
    | 中科搏康 | 成都信诚昌达贸易有限公司 | 成都市第三人民医院 | 无创脑血氧监护仪 | 427,800.00 | BRS-100B | 1.00(套) | 427,800.00 |
    | 开立 | 四川中科智慧健康管理集团有限公司 | 成都市第三人民医院 | 床旁彩色多普勒超声仪 | 541,000.00 | X5 | 1.00(套) | 541,000.00 |
    """

    expected_headers = ["招标单位", "供应商", "产品名称", "产品品牌", "产品型号", "产品数量", "产品单价(元)",
                        "中标总价(元)"]

    result = parse_markdown_table(markdown_table, expected_headers)
    for item in result:
        print(item)


if __name__ == '__main__':
    test_markdown_parser()
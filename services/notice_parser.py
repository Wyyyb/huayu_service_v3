from services.prompt_manager import *
from services.llm_call_manager import *
import time
import re


def parse_bidding_product(input_text):
    prompt = get_prompt("bidding_product")
    start_time = time.time()
    response = llm_single_call(prompt + "\n\n" + input_text)
    expected_headers = ["招标单位", "产品名称", "产品数量", "产品预算单价(元)", "预算总金额(元)", "最高限价(元)"]
    try:
        result = parse_markdown_table(response, expected_headers)
    except Exception as e:
        print("exception in parse_markdown_table(response, expected_headers)", e)
        print("llm original response", response)
        result = None
    return result, response, time.time() - start_time


def parse_winning_product(input_text):
    prompt = get_prompt("winning_product")
    start_time = time.time()
    response = llm_single_call(prompt + "\n\n" + input_text)
    expected_headers = ["招标单位", "供应商", "产品名称", "产品品牌", "产品型号", "产品数量", "产品单价(元)", "中标总价(元)"]
    try:
        result = parse_markdown_table(response, expected_headers)
    except Exception as e:
        print("exception in parse_markdown_table(response, expected_headers)", e)
        print("llm original response", response)
        result = None
    return result, response, time.time() - start_time


def parse_other_info(input_text, service_type):
    prompt = get_prompt(service_type)
    start_time = time.time()
    response = llm_single_call(prompt + "\n\n" + input_text)
    try:
        result = parse_response(response, service_type)
    except Exception as e:
        print("exception in parse_response(response, service_type)", e)
        print("llm original response", response)
        result = None
    return result, response, time.time() - start_time


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


def parse_response(response_text, function_type):
    if function_type == "code_extraction":
        return parse_code_response(response_text)
    elif function_type == "district_time":
        return parse_district_response(response_text)
    elif function_type == "bid_type":
        return parse_bid_type(response_text)
    elif function_type == "notice_type":
        return parse_notice_type(response_text)
    elif function_type == "contact_info":
        return parse_contact_info(response_text)
    else:
        return None


def parse_code_response(response_text):
    """
    解析 LLM 的回答，将“项目编号、招标编号、合同编号、采购计划编号、包号、标段号”等提取到字典中。

    :param response_text: LLM 返回的文本（格式化为键值对）
    :return: 包含提取信息的字典
    """
    # 定义要提取的字段
    keys = ["项目编号", "招标编号", "合同编号", "采购编号", "采购计划编号", "意向编号",
            "包号", "标段号", "订单号", "流水号"]
    extracted_data = {}

    # 遍历字段并使用正则表达式提取对应值
    for key in keys:
        pattern = rf"{key}\s*[:：]\s*(.*)"
        match = re.search(pattern, response_text)
        if match:
            extracted_data[key] = match.group(1).strip()  # 提取并去掉多余空格
        else:
            extracted_data[key] = "无"  # 如果没找到，则标记为“无”

    return extracted_data


def parse_district_response(response_text):
    """
    解析 LLM 的回答，将“地区、发布时间、报名截止时间、获取招标文件开始时间、
    获取招标文件截止时间、递交投标文件开始时间、递交投标文件截止时间、报价截止时间、开标时间”提取到字典中。

    :param response_text: LLM 返回的文本（格式化为键值对）
    :return: 包含提取信息的字典
    """
    # 定义要提取的字段
    keys = [
        "采购地区",
        "发布时间",
        "报名截止时间",
        "获取招标文件开始时间",
        "获取招标文件截止时间",
        "递交投标文件开始时间",
        "递交投标文件截止时间",
        "报价截止时间",
        "开标时间"
    ]
    extracted_data = {}

    # 遍历字段并使用正则表达式提取对应值
    for key in keys:
        pattern = rf"{key}\s*[:：]\s*(.*)"
        match = re.search(pattern, response_text)
        if match:
            extracted_data[key] = match.group(1).strip()  # 提取并去掉多余空格
        else:
            extracted_data[key] = "无"  # 如果没找到，则标记为“无”

    return extracted_data


def parse_notice_type(response_text):
    """
    将 LLM 的分类结果转换为标准化的公告类型。

    :param response_text: LLM 返回的分类结果文本
    :return: 公告类型字符串，如果无法分类则返回 '其他'
    """
    # 定义所有可能的公告类型
    valid_categories = [
        "招标", "结果", "中标", "成交", "废标", "流标", "终止",
        "入围", "预告", "变更", "信息", "合同", "验收",
        "违规", "预审", "其他"
    ]

    category = response_text.strip()
    if category in valid_categories:
        return {"公告类型": category}
    else:
        return {"公告类型": "其他"}


def parse_bid_type(response_text):
    """
    将 LLM 的采购类型分类结果转换为标准化的采购类型。

    :param response_text: LLM 返回的分类结果文本
    :return: 采购类型字符串，如果无法分类则返回 '其他'
    """
    # 定义所有可能的采购类型
    valid_categories = [
        "公开招标", "竞争性磋商", "竞争性谈判", "询价", "单一来源",
        "邀请招标", "协议竞价", "电子反拍", "网上询价", "网上竞价",
        "协议采购", "批量采购", "定点采购", "定点服务", "电商直购"
    ]

    # 去掉多余的空格或换行符并验证分类结果
    category = response_text.strip()
    if category in valid_categories:
        return {"采购类型": category}
    else:
        return {"采购类型": "其他"}  # 如果结果不在有效类别中，则返回“其他”


def parse_contact_info(response_text):
    """
    解析 LLM 的返回结果，将联系人信息提取到一个列表中，每个联系人信息存储为一个字典。

    :param response_text: LLM 返回的联系人信息文本
    :return: 包含联系人信息的列表，每个元素为包含详细信息的字典
    """
    # 定义正则表达式模式，用于提取联系人信息块
    contact_pattern = re.compile(
        r"所属企业名称\s*[:：]\s*(.*?)\s*联系人名字\s*[:：]\s*(.*?)\s*联系电话\s*[:：]\s*(.*?)\s*账号类型\s*[:：]\s*(.*?)"
    )

    # 匹配所有联系人信息块
    matches = contact_pattern.findall(response_text)
    contact_list = []

    # 遍历匹配结果，构建联系人字典
    for match in matches:
        contact_dict = {
            "所属企业名称": match[0].strip() if match[0].strip() else "无",
            "联系人名字": match[1].strip() if match[1].strip() else "无",
            "联系电话": match[2].strip() if match[2].strip() else "无",
            "账号类型": match[3].strip() if match[3].strip() else "无",
        }
        contact_list.append(contact_dict)

    return contact_list


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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import base64

# 服务配置
BASE_URL = "http://localhost:8888"

def example_text_services():
    """文本服务使用示例"""
    print("=== 文本服务使用示例 ===")
    
    # 示例1：招标公告产品服务
    print("\n1. 招标公告产品服务")
    data = {
        "service_type": "bidding_product",
        "notice_id": "BID001",
        "content": "宜城市人民医院招标公告：采购胰岛素泵四台，预算单价30000元，预算金额120000元，最高限价120000元。",
        "extra_info": {"source": "政府采购网"}
    }
    
    response = requests.post(f"{BASE_URL}/api/text", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 失败: {response.status_code}")
    
    # 示例2：编号提取服务
    print("\n2. 编号提取服务")
    data = {
        "service_type": "code_extraction",
        "notice_id": "ID001",
        "content": "项目编号：yc23460020(cgp)，招标编号：yc23460020(cgp)，合同编号：HT2024001",
        "extra_info": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/text", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 失败: {response.status_code}")
    
    # 示例3：联系人信息解析
    print("\n3. 联系人信息解析")
    data = {
        "service_type": "contact_info",
        "notice_id": "CON001",
        "content": "宜城市人民医院联系人：廖主任，电话：0710-4268367；亿诚建设项目管理有限公司联系人：李工，电话：15671329168",
        "extra_info": {}
    }
    
    response = requests.post(f"{BASE_URL}/api/text", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 失败: {response.status_code}")

def example_multimodal_services():
    """多模态服务使用示例"""
    print("\n=== 多模态服务使用示例 ===")
    
    # 示例：PDF处理（模拟）
    print("\n1. PDF文本提取（模拟）")
    data = {
        "notice_id": "DOC001",
        "file_type": "pdf",
        "file_data": "JVBERi0xLjQKJcOkw7zDtsO8=",  # 有效的base64数据
        "extra_info": {"source": "example"}
    }
    
    response = requests.post(f"{BASE_URL}/api/multimodal", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 失败: {response.status_code}")
    
    # 示例：图片处理（模拟）
    print("\n2. 图片OCR文本提取（模拟）")
    data = {
        "notice_id": "IMG001",
        "file_data_list": [
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",  # 模拟base64图片数据
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        ],
        "extra_info": {"source": "example"}
    }
    
    response = requests.post(f"{BASE_URL}/api/multimodal", json=data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 成功: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 失败: {response.status_code}")

def example_health_check():
    """健康检查示例"""
    print("=== 健康检查示例 ===")
    
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 服务状态: {json.dumps(result, ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 健康检查失败: {response.status_code}")

def main():
    """主函数"""
    print("华语服务引擎使用示例")
    print("=" * 60)
    
    try:
        # 健康检查
        example_health_check()
        
        # 文本服务示例
        example_text_services()
        
        # 多模态服务示例
        example_multimodal_services()
        
        print("\n" + "=" * 60)
        print("示例执行完成！")
        print("注意：当前返回的是模拟数据，实际使用时需要实现具体的解析逻辑。")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保服务已启动在 http://localhost:8888")
    except Exception as e:
        print(f"❌ 执行异常: {str(e)}")

if __name__ == "__main__":
    main() 
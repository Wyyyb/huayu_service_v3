#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

# 本地服务配置
BASE_URL = "http://localhost:8888"
TIMEOUT = 10

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功")
            print(f"   服务状态: {data.get('status')}")
            print(f"   服务名称: {data.get('service')}")
            print(f"   版本: {data.get('version')}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {str(e)}")
        return False

def test_text_service(service_type, notice_id, content, extra_info=None):
    """测试文本服务"""
    print(f"=== 测试文本服务: {service_type} ===")
    try:
        url = f"{BASE_URL}/api/text"
        data = {
            "service_type": service_type,
            "notice_id": notice_id,
            "content": content,
            "extra_info": extra_info or {}
        }
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=TIMEOUT)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ 文本服务-{service_type} ({(end_time-start_time):.2f}s)")
                print(f"   返回数据: {json.dumps(result.get('data', {}), ensure_ascii=False, indent=2)}")
                return True
            else:
                print(f"❌ 文本服务-{service_type} 失败: {result.get('error')}")
                return False
        else:
            print(f"❌ 文本服务-{service_type} HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 文本服务-{service_type} 异常: {str(e)}")
        return False

def test_multimodal_service():
    """测试多模态服务"""
    print("=== 测试多模态服务 ===")
    try:
        url = f"{BASE_URL}/api/multimodal"
        data = {
            "notice_id": "DOC001",
            "file_type": "pdf",
            "file_data": "JVBERi0xLjQKJcOkw7zDtsO8=",  # 有效的base64数据
            "extra_info": {"source": "test"}
        }
        
        start_time = time.time()
        response = requests.post(url, json=data, timeout=TIMEOUT)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print(f"✅ 多模态服务 ({(end_time-start_time):.2f}s)")
                print(f"   返回数据: {json.dumps(result.get('data', {}), ensure_ascii=False, indent=2)}")
                return True
            else:
                print(f"❌ 多模态服务失败: {result.get('error')}")
                return False
        else:
            print(f"❌ 多模态服务HTTP错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 多模态服务异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("华语服务引擎本地测试脚本")
    print("=" * 60)
    
    # 测试健康检查
    health_ok = test_health_check()
    if not health_ok:
        print("❌ 健康检查失败，请确保服务已启动")
        return
    
    print()
    
    # 测试文本服务
    text_services = [
        ("bidding_product", "BID001", "某公司招标公告内容，包含产品信息..."),
        ("winning_product", "WIN001", "中标公告内容，包含中标产品信息..."),
        ("code_extraction", "ID001", "项目编号：PRJ2024001，招标编号：TDR2024001..."),
        ("district_time", "LOC001", "湖北省武汉市，发布时间：2024年1月1日..."),
        ("notice_type", "TYPE001", "招标公告，紧急程度：普通..."),
        ("bid_type", "PUR001", "政府采购，采购方式：公开招标..."),
        ("contact_info", "CON001", "联系人：张三，电话：13800138000...")
    ]
    
    text_success_count = 0
    for service_type, notice_id, content in text_services:
        if test_text_service(service_type, notice_id, content):
            text_success_count += 1
        print()
    
    # 测试多模态服务
    multimodal_ok = test_multimodal_service()
    
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"文本服务测试: {text_success_count}/7 成功")
    print(f"多模态服务测试: {'1/1' if multimodal_ok else '0/1'} 成功")
    total_success = text_success_count + (1 if multimodal_ok else 0)
    print(f"总体成功率: {total_success}/8 ({(total_success/8)*100:.1f}%)")
    
    if text_success_count == 7 and multimodal_ok:
        print("🎉 所有测试通过！服务运行正常。")
    else:
        print("⚠️  部分测试失败，请检查服务配置。")

if __name__ == "__main__":
    main() 
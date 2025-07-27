#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
from abc import ABC, abstractmethod
from services.notice_parser import *
import pytz
import datetime


def get_beijing_time_pytz():
    # 获取UTC时间
    utc_now = datetime.datetime.now(pytz.utc)
    # 转换为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_now = utc_now.astimezone(beijing_tz)
    beijing_now = beijing_now.strftime("%Y-%m-%d %H:%M:%S")
    return beijing_now


class BaseProcessor(ABC):
    """处理器基类"""
    
    @abstractmethod
    def process(self, notice_id, content, extra_info=None):
        """处理核心逻辑"""
        pass

class BiddingNoticeProcessor(BaseProcessor):
    """招标公告产品服务处理器"""
    
    def process(self, notice_id, content, extra_info=None):
        """处理招标公告产品信息"""
        # TODO: 实现具体的招标公告产品解析逻辑
        data, ori_response, cost_time = parse_bidding_product(content)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": "bidding_product",
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class WinningNoticeProcessor(BaseProcessor):
    """中标公告产品服务处理器"""
    
    def process(self, notice_id, content, extra_info=None):
        """处理中标公告产品信息"""
        # TODO: 实现具体的中标公告产品解析逻辑
        data, ori_response, cost_time = parse_winning_product(content)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": "winning_product",
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class IdExtractionProcessor(BaseProcessor):
    """编号提取服务处理器"""

    def process(self, notice_id, content, extra_info=None):
        """提取各种编号信息"""
        service = "code_extraction"
        data, ori_response, cost_time = parse_other_info(content, service)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": service,
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class LocationTimeProcessor(BaseProcessor):
    """地区时间提取服务处理器"""
    
    def process(self, notice_id, content, extra_info=None):
        """提取地区和时间信息"""
        service = "district_time"
        data, ori_response, cost_time = parse_other_info(content, service)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": service,
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class NoticeTypeClassificationProcessor(BaseProcessor):
    """公告类型分类处理器"""
    
    def process(self, notice_id, content, extra_info=None):
        """分类公告类型"""
        service = "notice_type"
        data, ori_response, cost_time = parse_other_info(content, service)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": service,
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class PurchaseTypeClassificationProcessor(BaseProcessor):
    """采购类型分类处理器"""
    
    def process(self, notice_id, content, extra_info=None):
        """分类采购类型"""
        service = "bid_type"
        data, ori_response, cost_time = parse_other_info(content, service)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": service,
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class ContactInfoProcessor(BaseProcessor):
    """联系人信息解析处理器"""
    
    def process(self, notice_id, content, extra_info=None):
        """解析联系人信息"""
        service = "contact_info"
        data, ori_response, cost_time = parse_other_info(content, service)
        request_time = get_beijing_time_pytz()
        result = {
            "notice_id": notice_id,
            "service_type": service,
            "input_text": content,
            "result": data,
            "original_response": ori_response,
            "cost_time": cost_time,
            "request_time": request_time,
        }
        return result

class MultimodalProcessor:
    """多模态服务处理器"""
    
    def process_file(self, notice_id, file_data, file_type, extra_info=None):
        """处理单个文件"""
        if file_type == 'pdf':
            return self.process_pdf(notice_id, file_data, extra_info)
        elif file_type == 'images':
            return self.process_single_image(notice_id, file_data, extra_info)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def process_images(self, notice_id, file_data_list, extra_info=None):
        """处理多张图片"""
        # TODO: 实现具体的多图片OCR逻辑
        extracted_texts = []
        for i, file_data in enumerate(file_data_list):
            # 解码base64数据
            if isinstance(file_data, str):
                try:
                    file_data = base64.b64decode(file_data)
                except Exception as e:
                    raise ValueError(f"Invalid base64 data for image {i+1}: {str(e)}")
            
            # TODO: 实现图片OCR逻辑
            extracted_texts.append(f"待实现 - 图片{i+1}的OCR文本提取")
        
        result = {
            "notice_id": notice_id,
            "service_type": "multimodal_images",
            "file_type": "images",
            "image_count": len(file_data_list),
            "extracted_texts": extracted_texts,
            "combined_text": " ".join(extracted_texts)
        }
        return result
    
    def process_pdf(self, notice_id, file_data, extra_info):
        """处理PDF文件"""
        # TODO: 实现具体的PDF文本提取逻辑
        result = {
            "notice_id": notice_id,
            "service_type": "multimodal_pdf",
            "file_type": "pdf",
            "extracted_text": "待实现 - PDF文本提取",
            "page_count": "待实现",
            "file_size": len(file_data)
        }
        return result
    
    def process_single_image(self, notice_id, file_data, extra_info):
        """处理单张图片"""
        # TODO: 实现具体的单图片OCR逻辑
        result = {
            "notice_id": notice_id,
            "service_type": "multimodal_images",
            "file_type": "images",
            "image_count": 1,
            "extracted_texts": ["待实现 - 单张图片的OCR文本提取"],
            "combined_text": "待实现 - 单张图片的OCR文本提取"
        }
        return result 
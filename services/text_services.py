#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
import json
from datetime import datetime
from services.processors import (
    BiddingNoticeProcessor,
    WinningNoticeProcessor,
    IdExtractionProcessor,
    LocationTimeProcessor,
    NoticeTypeClassificationProcessor,
    PurchaseTypeClassificationProcessor,
    ContactInfoProcessor
)

class TextServiceHandler(tornado.web.RequestHandler):
    def post(self):
        """文本服务接口"""
        try:
            # 解析请求参数
            data = json.loads(self.request.body)
            
            # 验证必需参数
            required_fields = ['service_type', 'notice_id', 'content']
            for field in required_fields:
                if field not in data:
                    self.send_error_response(f"Missing required field: {field}")
                    return
            
            service_type = data['service_type']
            notice_id = data['notice_id']
            content = data['content']
            extra_info = data.get('extra_info', {})
            
            # 根据服务类型调用相应的处理器
            processor = self.get_processor(service_type)
            if not processor:
                self.send_error_response(f"Unsupported service type: {service_type}")
                return
            
            # 处理请求
            result = processor.process(notice_id, content, extra_info)
            
            # 返回成功响应
            self.send_success_response(result)
            
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON format")
        except Exception as e:
            self.send_error_response(f"Internal server error: {str(e)}")
    
    def get_processor(self, service_type):
        """根据服务类型获取对应的处理器"""
        processors = {
            'bidding_product': BiddingNoticeProcessor(),
            'winning_product': WinningNoticeProcessor(),
            'code_extraction': IdExtractionProcessor(),
            'district_time': LocationTimeProcessor(),
            'notice_type': NoticeTypeClassificationProcessor(),
            'bid_type': PurchaseTypeClassificationProcessor(),
            'contact_info': ContactInfoProcessor()
        }
        return processors.get(service_type)
    
    def send_success_response(self, data):
        """发送成功响应"""
        response = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.write(response)
    
    def send_error_response(self, error_message):
        """发送错误响应"""
        response = {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "error": error_message
        }
        self.write(response) 
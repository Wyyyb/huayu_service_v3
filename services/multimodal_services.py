#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
import json
import base64
import os
from datetime import datetime
from services.processors import MultimodalProcessor

class MultimodalServiceHandler(tornado.web.RequestHandler):
    def post(self):
        """多模态服务接口"""
        try:
            # 检查Content-Type
            content_type = self.request.headers.get('Content-Type', '')
            
            if 'multipart/form-data' in content_type:
                # 文件上传方式
                self.handle_file_upload()
            else:
                # JSON方式
                self.handle_json_request()
                
        except Exception as e:
            self.send_error_response(f"Internal server error: {str(e)}")
    
    def handle_file_upload(self):
        """处理文件上传请求"""
        try:
            # 获取表单数据
            notice_id = self.get_argument('notice_id')
            extra_info_str = self.get_argument('extra_info', '{}')
            extra_info = json.loads(extra_info_str) if extra_info_str else {}
            
            # 获取上传的文件
            files = self.request.files.get('file', [])
            if not files:
                self.send_error_response("No file uploaded")
                return
            
            file_obj = files[0]
            filename = file_obj['filename']
            file_data = file_obj['body']
            
            # 检查文件类型
            file_type = self.get_file_type(filename)
            if not file_type:
                self.send_error_response("Unsupported file type")
                return
            
            # 处理文件
            processor = MultimodalProcessor()
            result = processor.process_file(notice_id, file_data, file_type, extra_info)
            
            # 返回结果
            self.send_success_response(result)
            
        except Exception as e:
            self.send_error_response(f"File upload error: {str(e)}")
    
    def handle_json_request(self):
        """处理JSON请求"""
        try:
            data = json.loads(self.request.body)
            
            # 验证必需参数
            if 'notice_id' not in data:
                self.send_error_response("Missing required field: notice_id")
                return
            
            notice_id = data['notice_id']
            extra_info = data.get('extra_info', {})
            
            # 处理PDF文件
            if 'file_type' in data and data['file_type'] == 'pdf' and 'file_data' in data:
                try:
                    file_data = base64.b64decode(data['file_data'])
                    processor = MultimodalProcessor()
                    result = processor.process_file(notice_id, file_data, 'pdf', extra_info)
                    self.send_success_response(result)
                    return
                except Exception as e:
                    self.send_error_response(f"Invalid base64 data: {str(e)}")
                    return
            
            # 处理图片文件
            if 'file_data_list' in data:
                file_data_list = data['file_data_list']
                if not file_data_list:
                    self.send_error_response("No image data provided")
                    return
                
                try:
                    processor = MultimodalProcessor()
                    result = processor.process_images(notice_id, file_data_list, extra_info)
                    self.send_success_response(result)
                    return
                except Exception as e:
                    self.send_error_response(f"Image processing error: {str(e)}")
                    return
            
            self.send_error_response("Invalid request format")
            
        except json.JSONDecodeError:
            self.send_error_response("Invalid JSON format")
        except Exception as e:
            self.send_error_response(f"JSON request error: {str(e)}")
    
    def get_file_type(self, filename):
        """根据文件名判断文件类型"""
        if not filename:
            return None
        
        ext = os.path.splitext(filename)[1].lower()
        
        if ext == '.pdf':
            return 'pdf'
        elif ext in ['.png', '.jpg', '.jpeg']:
            return 'images'
        else:
            return None
    
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
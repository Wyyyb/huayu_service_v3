#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
from datetime import datetime

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        """健康检查接口"""
        response = {
            "status": "healthy",
            "service": "huayu_service_engine",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
        self.write(response) 
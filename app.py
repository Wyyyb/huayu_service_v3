#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import json
import base64
import os
from datetime import datetime
from services.text_services import TextServiceHandler
from services.multimodal_services import MultimodalServiceHandler
from handlers.health_handler import HealthHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({
            "message": "华语服务引擎",
            "version": "1.0.0",
            "status": "running"
        })

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/health", HealthHandler),
        (r"/api/text", TextServiceHandler),
        (r"/api/multimodal", MultimodalServiceHandler),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("华语服务引擎启动成功，监听端口: 8888")
    tornado.ioloop.IOLoop.current().start() 
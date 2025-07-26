#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import signal
import time

def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    print("\n正在关闭服务...")
    sys.exit(0)

def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    
    print("华语服务引擎启动中...")
    print("=" * 50)
    
    try:
        # 检查依赖
        print("检查依赖...")
        import tornado
        import json
        print("✅ 依赖检查通过")
        
        # 导入应用
        print("加载应用...")
        from app import make_app
        app = make_app()
        print("✅ 应用加载成功")
        
        # 启动服务
        port = 8888
        print(f"启动服务在端口 {port}...")
        app.listen(port)
        print(f"✅ 服务启动成功: http://localhost:{port}")
        print("=" * 50)
        print("服务已启动，按 Ctrl+C 停止服务")
        print("=" * 50)
        
        # 启动事件循环
        import tornado.ioloop
        tornado.ioloop.IOLoop.current().start()
        
    except ImportError as e:
        print(f"❌ 依赖导入失败: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 服务启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
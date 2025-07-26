# 华语服务引擎

基于Tornado的Python服务引擎，提供多种文本处理和多模态服务。

## 功能特性

### 文本服务
- **招标公告产品服务** (`bidding_product`) - 处理招标公告产品信息
- **中标公告产品服务** (`winning_product`) - 处理中标公告产品信息  
- **编号提取服务** (`code_extraction`) - 提取各种编号信息
- **地区时间提取服务** (`district_time`) - 提取地区和时间信息
- **公告类型分类** (`notice_type`) - 分类公告类型
- **采购类型分类** (`bid_type`) - 分类采购类型
- **联系人信息解析** (`contact_info`) - 解析联系人信息

### 多模态服务
- **PDF文本提取** - 从PDF文件中提取文本
- **图片OCR文本提取** - 从图片文件中提取文本

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

### 方式一：直接启动
```bash
python app.py
```

### 方式二：使用启动脚本（推荐）
```bash
python start_server.py
```

服务将在 `http://localhost:8888` 启动。

## API接口

### 1. 文本服务接口

**POST** `/api/text`

请求参数：
```json
{
    "service_type": "bidding_product",
    "notice_id": "BID001",
    "content": "招标公告内容...",
    "extra_info": {
        "source": "政府采购网"
    }
}
```

### 2. 多模态服务接口

**POST** `/api/multimodal`

支持文件上传和JSON两种方式：

#### 文件上传方式
```bash
curl -X POST http://localhost:8888/api/multimodal \
  -F "notice_id=DOC001" \
  -F "extra_info={\"source\":\"upload\"}" \
  -F "file=@document.pdf"
```

#### JSON方式
```json
{
    "notice_id": "DOC001",
    "file_type": "pdf",
    "file_data": "base64编码的文件数据",
    "extra_info": {
        "source": "api"
    }
}
```

### 3. 健康检查接口

**GET** `/health`

## 项目结构

```
huayu_service_v3/
├── app.py                 # 主应用文件
├── requirements.txt       # 依赖文件
├── README.md             # 项目说明
├── handlers/             # 处理器目录
│   ├── __init__.py
│   └── health_handler.py # 健康检查处理器
└── services/             # 服务目录
    ├── __init__.py
    ├── text_services.py  # 文本服务处理器
    ├── multimodal_services.py # 多模态服务处理器
    └── processors.py     # 核心处理器
```

## 开发说明

所有核心解析逻辑都在 `services/processors.py` 文件中，每个处理器都有对应的 `process` 方法，目前返回模拟数据，需要根据实际需求实现具体的解析逻辑。

## 测试

### 本地测试
```bash
python test_local_services.py
```

### 远程测试
可以使用项目中的 `test_remote_services.py` 脚本来测试远程服务功能。

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **启动服务**
   ```bash
   python start_server.py
   ```

3. **测试服务**
   ```bash
   python test_local_services.py
   ```

4. **查看使用示例**
   ```bash
   python example_usage.py
   ``` 
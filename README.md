# GrabNumber

这是一个简单的 Flask 应用程序，用于通过表单提交数据并发送注册请求。

## 目录结构

```
grabNumber/
│
├── app.py
├── grabNumber/
│   ├── __init__.py
│   └── RegistrationClient.py
├── templates/
│   └── index.html
├── static/
│   └── css/
│       └── style.css
├── README.md
└── requirements.txt
```

## 安装

1. 克隆此仓库到本地：

    ```bash
    git clone https://github.com/yourusername/grabNumber.git
    cd grabNumber
    ```

2. 创建并激活虚拟环境：

    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    ```

3. 安装依赖项：

    ```bash
    pip install -r requirements.txt
    ```

## 运行应用程序

1. 启动 Flask 应用程序：

    ```bash
    python app.py
    ```

2. 打开浏览器并访问 `http://127.0.0.1:5000`。

## 使用

在主页上输入 `Token` 和 `EID`，然后点击提交按钮。表单数据将通过 AJAX 请求发送到服务器，并显示成功弹框。

## 文件说明

- `app.py`：Flask 应用程序的主文件，定义了路由和处理逻辑。
- `templates/index.html`：包含表单的 HTML 模板。
- `grabNumber/RegistrationClient.py`：处理注册请求的客户端类。
- `README.md`：项目的说明文件。
- `requirements.txt`：项目的依赖项文件。

## 作者

- **TIGER林** - [3024169080](https://github.com/3024169080)

## 许可证

此项目使用 MIT 许可证。有关更多信息，请参阅 LICENSE 文件。
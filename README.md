![image](https://github.com/user-attachments/assets/cd1942fc-aaa7-4354-9df9-dd9c6979aa16)
![image](https://github.com/user-attachments/assets/6d7d8552-73f6-4b84-abc0-3af61096a00e)

# Automatic-monitoring-of-web-pages
# 产品介绍：网页数据监控工具

## 概述
本产品是一个基于 Python 的网页数据监控工具，能够自动监测指定网页的内容变化，并在变化发生时发送系统通知。该工具支持多网址监控，用户可以自定义监控的网页区域，适用于需要实时监控网页内容的场景，如价格变动、新闻更新等。

## 功能特点
1. **多网址监控**：支持同时监控多个网址，用户可以在配置文件中指定要监控的网页及其对应的监控区域。
2. **区域选择**：用户可以通过 CSS 选择器或 XPath 定位网页中的特定区域进行监控，支持监控整个页面或特定元素。
3. **系统通知**：当监测到网页内容变化时，工具会通过系统通知提醒用户，确保用户及时获取信息。
4. **日志记录**：所有变化都会记录到 `changes_log.json` 文件中，方便用户查看历史变化记录。
5. **用户配置**：支持使用已登录的 Firefox 浏览器配置，保留用户的登录状态和浏览历史。

## 技术栈
- **Python**：主程序语言，使用 Python 进行开发。
- **Selenium**：用于自动化浏览器操作，支持 Firefox 浏览器。
- **BeautifulSoup**：用于解析网页内容。
- **Plyer**：用于发送系统通知。
- **多线程**：使用 Python 的 threading 模块实现多网址的并发监控。

## 安装与使用
### 环境要求
- Python 3.x
- Firefox 浏览器
- geckodriver（Firefox 的 WebDriver）

### 安装步骤
1. **安装依赖库**：
   ```bash
   pip install selenium beautifulsoup4 plyer
   ```

2. **下载 geckodriver**：
   - 从 [geckodriver releases](https://github.com/mozilla/geckodriver/releases) 下载适合你的window操作系统的版本，并将其添加到系统 PATH。

3. **配置监控网址**：
   - 在 `main.py` 文件中配置要监控的网址和区域。

### 运行程序
- 使用 `run_monitor.bat` 文件启动监控工具，双击该文件即可在后台运行监控任务。

## 代码结构
- `run_monitor.bat`：批处理文件，用于启动 Python 脚本。
- `main.py`：主程序，负责初始化监控器并启动监控。
- `multi_monitor.py`：实现多网址监控的逻辑。
- `webpage_monitor.py`：实现单个网页监控的逻辑，包括内容获取、比较和通知。

## 结论
本网页监控工具为用户提供了一个高效、灵活的方式来监测网页内容的变化，适用于各种需要实时监控的场景。通过简单的配置，用户可以轻松上手并开始使用。

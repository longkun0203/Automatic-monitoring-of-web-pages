from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
from plyer import notification
import time
import difflib
import json
from datetime import datetime
import os

class WebpageMonitor:
    def __init__(self, url, check_interval=300, selectors=None):
        self.url = url
        self.check_interval = check_interval
        # selectors 格式: {'区域名称': {'type': 'css|xpath', 'value': '选择器'}}
        self.selectors = selectors or {'full_page': None}  # 如果没有指定选择器，则监控整个页面
        self.previous_contents = {name: None for name in self.selectors}
        self.setup_driver()
        
    def setup_driver(self):
        firefox_options = FirefoxOptions()
        
        # 使用已有的Firefox配置文件
        profile_path = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
        
        # 查找默认配置文件
        try:
            profiles = [f for f in os.listdir(profile_path) if f.endswith('.default-release')]
            if profiles:
                profile_name = profiles[0]
                firefox_profile_path = os.path.join(profile_path, profile_name)
                firefox_options.set_preference('profile', firefox_profile_path)
                print(f"使用Firefox配置文件: {firefox_profile_path}")
            else:
                print("未找到默认配置文件，将使用新配置文件")
        except Exception as e:
            print(f"读取配置文件时出错: {str(e)}")
        
        try:
            # 初始化WebDriver
            service = Service(log_output=os.devnull)
            self.driver = webdriver.Firefox(
                service=service,
                options=firefox_options
            )
            
            # 设置超时时间
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            print(f"成功连接到Firefox浏览器")
            return True
            
        except Exception as e:
            print(f"连接Firefox浏览器失败: {str(e)}")
            return False
        
    def get_page_content(self):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 检查driver是否还活着
                try:
                    self.driver.current_url
                except:
                    print("浏览器连接已断开，重新连接...")
                    self.setup_driver()
                
                # 访问页面
                self.driver.get(self.url)
                time.sleep(5)  # 等待页面加载
                
                # 检查页面是否正确加载
                if "ERR_" in self.driver.page_source or "无法访问此网站" in self.driver.page_source:
                    raise Exception("页面加载失败")
                
                # 获取所有监控区域的内容
                contents = {}
                for name, selector in self.selectors.items():
                    if selector is None:
                        # 如果没有选择器，获取整个页面内容
                        contents[name] = self.driver.page_source
                    else:
                        try:
                            if selector['type'] == 'css':
                                element = self.driver.find_element('css selector', selector['value'])
                            elif selector['type'] == 'xpath':
                                element = self.driver.find_element('xpath', selector['value'])
                            contents[name] = element.get_attribute('outerHTML')
                        except Exception as e:
                            print(f"获取区域 '{name}' 内容失败: {str(e)}")
                            contents[name] = None
                
                return contents
                
            except Exception as e:
                print(f"获取页面内容时出错 (尝试 {retry_count + 1}/{max_retries}): {str(e)}")
                retry_count += 1
                
                if retry_count >= max_retries:
                    print("达到最大重试次数，重新初始化浏览器...")
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.setup_driver()
                
                time.sleep(5)  # 等待一段时间后重试
        
        return None
            
    def compare_contents(self, new_contents):
        if not new_contents:
            return False
            
        has_changes = False
        changes_summary = []
        
        for name, new_content in new_contents.items():
            if self.previous_contents[name] is None:
                self.previous_contents[name] = new_content
                continue
            
            if new_content != self.previous_contents[name]:
                # 使用difflib查找具体变化
                diff = list(difflib.unified_diff(
                    self.previous_contents[name].splitlines(),
                    new_content.splitlines(),
                    lineterm=''
                ))
                
                # 记录变化
                self.log_changes(name, diff)
                
                # 添加到变化摘要
                changes_summary.append(f"区域 '{name}' 发生变化:\n" + '\n'.join(diff[:3]))
                
                self.previous_contents[name] = new_content
                has_changes = True
        
        if has_changes:
            # 发送带有变化摘要的通知
            notification.notify(
                title='网页监控提醒',
                message=f'检测到页面变化！\n网址: {self.url}\n\n' + '\n\n'.join(changes_summary),
                timeout=15
            )
        
        return has_changes
        
    def log_changes(self, area_name, changes):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "area": area_name,
            "changes": changes
        }
        
        with open("changes_log.json", "a", encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False)
            f.write("\n")
            
    def notify_change(self):
        """发送系统通知"""
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')  # 确保icon.png存在
        notification.notify(
            title='网页监控提醒',
            message=f'检测到页面变化！\n网址: {self.url}',
            app_icon=icon_path,
            timeout=10
        )
    
    def start_monitoring(self):
        print(f"开始监控网页: {self.url}")
        try:
            while True:
                new_contents = self.get_page_content()
                if new_contents:
                    if self.compare_contents(new_contents):
                        print(f"[{datetime.now()}] 检测到页面变化！")
                        self.notify_change()  # 发送系统通知
                    else:
                        print(f"[{datetime.now()}] 页面无变化")
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n停止监控")
        finally:
            self.driver.quit() 
from webpage_monitor import WebpageMonitor
from datetime import datetime
import threading
import time

class MultiWebpageMonitor:
    def __init__(self, urls, check_interval=300):
        """
        初始化多网址监控器
        :param urls: 字典，格式为 {'名称': 'URL'}
        :param check_interval: 检查间隔（秒）
        """
        self.monitors = {}
        self.check_interval = check_interval
        self.threads = {}
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 尝试创建所有监控器
                for name, config in urls.items():
                    try:
                        monitor = WebpageMonitor(
                            url=config['url'],
                            check_interval=check_interval,
                            selectors=config.get('selectors')
                        )
                        self.monitors[name] = monitor
                    except Exception as e:
                        print(f"创建监控器 '{name}' 失败: {str(e)}")
                
                if self.monitors:
                    print(f"成功创建了 {len(self.monitors)} 个监控器")
                    return
            except Exception as e:
                print(f"第 {retry_count + 1} 次尝试创建监控器失败: {str(e)}")
                retry_count += 1
                time.sleep(2)
    
    def monitor_site(self, name):
        """单个网站的监控线程"""
        monitor = self.monitors[name]
        print(f"开始监控 {name}: {monitor.url}")
        
        try:
            while True:
                new_content = monitor.get_page_content()
                if new_content:
                    if monitor.compare_contents(new_content):
                        print(f"[{datetime.now()}] {name} 检测到页面变化！")
                        monitor.notify_change()
                    else:
                        print(f"[{datetime.now()}] {name} 页面无变化")
                time.sleep(self.check_interval)
        except Exception as e:
            print(f"{name} 监控出错: {str(e)}")
        finally:
            monitor.driver.quit()
    
    def start_monitoring(self):
        """启动所有网站的监控"""
        for name in self.monitors:
            thread = threading.Thread(target=self.monitor_site, args=(name,))
            thread.daemon = True
            self.threads[name] = thread
            thread.start()
        
        try:
            # 保持主线程运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n��止所有监控")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """停止所有监控"""
        for name, monitor in self.monitors.items():
            try:
                monitor.driver.quit()
            except:
                pass 
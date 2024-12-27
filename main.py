from multi_monitor import MultiWebpageMonitor

if __name__ == "__main__":
    # 设置要监控的网址和区域
    urls = {
        "网站1": {
            "url": "https://s.foxlet.cn/",
            "selectors": {
                "标题": {
                    "type": "css",
                    "value": ".jinsom-post-list"  # 示例：监控h1标题
                },
                #"价格": {
                #    "type": "xpath",
                #    "value": "//div[@class='price']"  # 示例：监控价格区域
                #}
            }
        },
        "网站2": {
            "url": "https://s.foxlet.cn/mall",
            "selectors": {
                "商品列表": {
                    "type": "css",
                    "value": ".jinsom-shop-goods-box"  # 示例：监控商品列表区域
                }
            }
        }
    }
    
    # 创建多网址监控器实例（设置检查间隔为30秒）
    monitor = MultiWebpageMonitor(urls, check_interval=300)
    
    # 开始监控
    monitor.start_monitoring() 
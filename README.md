# shadowsocks-admin
基于Flask的[shadowsocks多用户版本](http://git.oschina.net/arrti/shadowsocks/tree/dev)的后台管理网站，主要对shadowsocks多用户版本使用的mysql和redis数据库进行管理，同时与其通过unix socket进行交互。
# 功能
## dashboard  
* 统计用户的服务状态
* 统计服务器流量使用情况
* 显示近1个小时内服务在线的用户

## user manage
* 显示全部未过期的用户
* 搜索用户
* 编辑用户信息
* 一键禁用用户

## user add
* 新增用户
* 返回新增用户的shadowsocks config内容

# 参数配置
* 网站参数配置位于`settings.py`文件
* shadowsocks相关内容位于`shadowsocks.py`文件

# requirements
* WTForms
* Flask-SQLAlchemy
* Flask-Login
* Flask-Script
* Flask-And-Redis
* Flask-Mail
* Flask-WTF
* PyMySQL

# Todo
* 管理员登陆界面

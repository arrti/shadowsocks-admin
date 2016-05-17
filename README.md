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

# 依赖
* WTForms
* Flask-SQLAlchemy
* Flask-Login
* Flask-Script
* Flask-And-Redis
* Flask-Mail
* Flask-WTF
* PyMySQL
* Pillow

# 使用

## 建立数据表
通过mysql导入`ss_admin/db/shadowsocks-admin.sql`，建立用于管理员登录的`admin`表，同时建立计划任务，每月1日凌晨01:00将用户表`user`(在shadowsocks多用户版本中建立)中的统计用户使用的流量`u`和`d`清零。

## 添加管理员
`add_admin.py`位于项目根目录下，执行`python add_admin.py -u your_email_address -p your_password_to_login`，会将管理员用于登录的email和加密后的密码保存到`admin`表中，默认使用的是与shadowsocks多用户版本相同的配置，根据需要修改文件中的数据库配置参数即可。

# Todo
* <s>管理员登录界面</s>
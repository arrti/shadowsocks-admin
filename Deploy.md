## 安装依赖
（1）建立虚拟环境（可选）
我使用的是Anaconda3，建立一个Python2.7的虚拟环境：
```
$ conda create -n flask_py27 python=2.7
```
建立好后，使用`soure activate flask_py27`激活虚拟环境，然后执行`pip -V`就可以看到确实使用的是虚拟环境下的pip：
```
$ pip -V
pip 9.0.1 from /anaconda3/envs/flask_py27/lib/python2.7/site-packages (python 2.7)
```
（2）安装需要的包
```
pip install -r requirements.txt
```
（3）安装Redis
```
sudo apt-get install redis-server
```
启动服务：
```
service redis-server start
```
测试，执行`redis-cli`，进入redis命令行模式，发送`ping`，收到`PONG`：
```
127.0.0.1:6379> ping
PONG
```

修改`/etc/redis/redis.conf`配置`requirepass`选项来设置密码，密码会以明文方式保存在redis配置文件中。     
使用命令`redis-cli -h 127.0.0.1 -p 6379 -a 密码`即可登陆，本地的话可以不写IP和端口，直接`redis-cli -a 密码`。
Python访问：
```
r = redis.Redis(host=’127.0.0.1’, port=6379, db=0, password=密码)
```

（4）安装MySQL
```
sudo apt-get install mysql-server
```
期间要求输入Mysql的`root`用户密码，输入并记住即可。    
执行`mysql -u root -p`并输入密码即可以`root`用户身份登陆MySQL：
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.00 sec)

mysql> 
```

在生产环境下安全使用Redis和MySQL数据库有较多的注意事项，比如修改默认的端口号等，这里不详细展开。

（5）安装nginx
```
sudo apt-get install nginx
```

（6）安装uwsgi
```
pip install uwsgi
```

如果运行uwsgi的时候提示`uwsgi: error while loading shared libraries: libpcre.so.1: cannot open shared object file: No such file or directory`错误，我使用的是16.04版本的ubuntu，类似的错误经常出现，可以先尝试在`/usr`目录下搜索`libpcre`，如果找到了`libpcre.so`，只需要将它链接到`/usr/lib`目录下即可：
```
sudo ln -s /usr/lib/x86_64-linux-gnu/libpcre.so /usr/lib/libpcre.so.1
```
如果没有，安装`libpcre`即可：
```
sudo apt-get install libpcre3 libpcre3-dev
```
安装后如果还是提示一样的错误，再按照上面的方法链接它即可。

## 配置
（1）安装多用户版本的shadowoscks
参考项目的[说明](https://github.com/arrti/shadowsocks/tree/multiuser)即可，很简单。
（2）建立数据库和表
创建数据库：
```
create database shadowsocks;
```
创建用户并为用户分配操作新建立的数据库的全部权限：
```
grant all privileges on shadowsocks.* to ss@localhost IDENTIFIED by 'shadowsocks';
flush  privileges;
```
上面的操作建立了一个名为`ss`的用户，其密码是`shadowsocks`，赋予了操作数据`shadowsocks`的全部权限。    
可以使用你自己的用户名和密码，涉及到数据库用户名和密码的文件有：
* `settings.py`：
```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://ss" \ # <-------mysql用户名‘ss’，改成你自己的
                           ":" \
                           "shadowsocks" \ # <------mysql密码’shadowsocks‘，改成你自己的
                           "@" \
                           "localhost/" \
                           "shadowsocks" \
                           "?charset=utf8"

REDIS_URL = 'redis://:shadowsocks@localhost:6379/0' # <------redis密码’shadowsocks‘，改成你自己的
```
* `add_admin.py`中的`Config_DB`类；
* [多用户版本的shadowoscks](https://github.com/arrti/shadowsocks/tree/multiuser)项目中`multiuserdb.py`文件的`Config_DB`类。


下面我们**以`ss`用户身份来登录MySQL，完成余下的配置工作**。
导入管理员表`admin`（`db/shadowsocks-admin.sql`）：
```
use shadowsocks;
source path_to_db/shadowsocks-admin.sql;
```
以同样的方式来导入[多用户版本的shadowoscks](https://github.com/arrti/shadowsocks/tree/multiuser)项目中的`shadowsocks.sql`，将会建立用户表`user`。

使用`python add_admin.py -u your_email_address -p your_password_to_login`可以快速添加一个管理员。

（3）nginx的配置文件
`config/nginx/shadowsocks-admin.conf`：
```
server {

    listen 80;
    server_name 127.0.0.1; # <------服务器名
    root /path/to/shadowsocks-admin/ss_admin/static; # <-----要设置为项目的静态目录的路径
	location /{
		include      uwsgi_params;
		uwsgi_pass   unix:/tmp/sa_nginx.sock;
	}
}
```

（4）uwsgi的配置文件
`config/uwsgi/shadowsocks-admin.ini`：
```
[uwsgi]
#python module to import
app = run
module = %(app)

#application and virtualenv path
pythonpath = /path/to/shadowsocks-admin # <-------项目的根目录
virtualenv = /path/to/virtualenv # <-------我使用了虚拟环境，这里要设置为虚拟环境的目录，如：/anaconda3/envs/flask_py27
#socket file's location
socket = /tmp/sa_nginx.sock

#permissions for the socket file
chmod-socket = 666

#the variable that holds a flask application inside the module imported at line #6
callable = app

#location of log files
logto = /var/log/uwsgi/%n.log

# spawn 1 process
processes = 1

# each process with 20 threads
threads = 20
```


（5）邮件
使用Flask-Mail来发送邮件，以使用QQ邮箱的stmp为例进行说明，配置如下：
```
# settings.py

MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'QQ邮箱'
MAIL_PASSWORD = 'QQ邮箱用于第三方客户端登录的授权码'
```

QQ邮箱的设置：
在“设置”->“账户”页面
* 开启pop3/stmp服务    
![](http://wx2.sinaimg.cn/mw690/64219fd1ly1ff2mwppwe9j20jt00rmx0.jpg)
* 获取授权码    
![](http://wx1.sinaimg.cn/mw690/64219fd1ly1ff2mwrahktj20dy01gmx1.jpg)
* 注意这里要使用flask的配置中要使用`TLS`     
![](http://wx4.sinaimg.cn/mw690/64219fd1ly1ff2mwqdevyj20hh04p74o.jpg)

## 运行
* 将`config/nginx/shadowsocks-admin.conf`文件链接到`/etc/nginx/conf.d`，然后执行`sudo service nginx start`来启动nginx服务；
* 执行`uwsgi --ini /path/to/shadowsocks-admin/config/uwsgi/shadowsocks-admin.ini`（`shadowsocks-admin.ini`的绝对路径）来启动uwsgi服务；
* 启动[多用户版本的shadowoscks](https://github.com/arrti/shadowsocks/tree/multiuser)的server服务。   

现在在浏览器上输入`127.0.0.1`（也就是nginx配置文件的`server_name`）即可打开管理网站的登录界面：    
![](http://wx1.sinaimg.cn/mw690/64219fd1ly1ff2mwovhz0j20u10h4wfb.jpg)

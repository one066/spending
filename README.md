# 团队开支记账系统
- 提供团队记账功能，每一笔记账都会和所有人发送开支邮件，在每个月(10号晚上8点)固定时间开出账单，并发送邮件。
- 保存每个月的账单，并通过折线图、饼图、表等展现出来


## 有前端页面，也可以通过api 对接机器人。


> 可以使用默docker-compose 启动mysql、redis、nginx等服务。
- 配置: docker-compose.yml 写入 qq 邮箱的配置
- 启动：docker 文件夹下, ```docker compose up -d```
- 初始化数据库(第一次使用必须操作): 进入 spending 镜像 ```python manage.py create_db```
- 添加组员(第一次使用必须操作): ```python manage.py add_user ```例：```python manage.py add_user -n one -p 123456 -e 111111111@qq.com```
- 查看组员: ```python manage.py show_user```
- 访问: ```http://127.0.0.1 即可```

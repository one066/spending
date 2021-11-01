def task1():
    """ 定时发邮箱
    """
    print('success')
    # mail.connect()
    # with app.app_context():
    #     data = Manager.to_leader_rollcall()
    #     df = pd.DataFrame(list(data))
    #     df.to_excel('static/data/data.xlsx', index=False, header=False, encoding='gbk', float_format='string')
    #
    #     body = f'{time.strftime("%Y-%m-%d")} 考勤情况'
    #     msg = Message("考勤情况",
    #                   sender='1875874066@qq.com',
    #                   recipients=['420422501@qq.com'],
    #                   body=body,
    #                   charset='gbk')
    #
    #     with app.open_resource('static/data/data.xlsx') as fp:
    #         # attach("文件名", "类型", 读取文件）
    #         msg.attach("data.xlsx", 'application/octet-stream', fp.read())
    #     with app.app_context():
    #         mail.send(msg)
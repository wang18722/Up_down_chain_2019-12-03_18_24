from celery_tasks.main import app

#可以设置name参数
@app.task(name='send_remind')
def send_remind():
    pass
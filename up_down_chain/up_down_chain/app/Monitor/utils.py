
#检测url函数封装
from datetime import datetime

from django_redis import get_redis_connection

from Monitor.models import MonitorsInfo
from oauth.models import CustomerInformation


def monitor(token,url):
    print(token)
    print(url)
    """解析出状态"""
    #token{}为字典格式
    #<QuerySet [{'username': 'oO5Eq6A0toEk2gINhc7TPMf9no24', 'password': 'pbkdf2_sha256$36000$HOKIyqI9cVxZ$3MXKiU4rPRf6qQHWeFAWI0Gf2Wb2Nm8nvJjKjv7iBow=', 'is_active': True, 'is_staff': False, 'email': '', 'country': '中国', 'CreateTime': datetime.date(2019, 6, 24), 'id': 2, 'headimgUrl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/zOZ9wWKyQXNsqE9UDicgfRVmh1ySE9vuJ5icZGRrJ66qfCPEUUfI152bAzYlcIvqg8LkYQ2aUAoyrAHcK9NGibuJw/132', 'first_name': '伊谢尔伦的风', 'last_login': datetime.datetime(2019, 6, 25, 8, 53, 39, 499556, tzinfo=<UTC>), 'city': '广州', 'last_name': '', 'is_superuser': False, 'date_joined': datetime.datetime(2019, 6, 24, 8, 31, 12, 793117, tzinfo=<UTC>), 'province': '广东', 'sex': '1'}]>
    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Im9PNUVxNkVINXUxbXF0cjNrZW91cU1qczR6YWsiLCJleHAiOjE1NjE1NDAzODcsImVtYWlsIjoiIn0.huyBm6lhlt7IRkRoF97Y54hdWEfwPGN_btiyHhevWVg
    #eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im9PNUVxNkEwdG9FazJnSU5oYzdUUE1mOW5vMjQiLCJlbWFpbCI6IiIsInVzZXJfaWQiOjIsImV4cCI6MTU2Mjc0ODgxOX0.1tEwCYEekvZv05LEfu8eRR8A4zQG0PS2tckqU5roxXE
    conn = get_redis_connection("monitor")
    obj_data = CustomerInformation.objects.filter(id = token["user_id"]).first()

    data_dict = {
        "username":obj_data.first_name,
        "country":obj_data.country,
        "city":obj_data.city,
        "province":obj_data.province,
        "headimgUrl":obj_data.headimgUrl

    }

    conn.set(token["user_id"],data_dict,600)

    #存储信息  和改变最后离开的url信息，同一天则更新，时间不同则新建
   # obj = MonitorsInfo.objects.filter(url=url,create_time=datetime.now().strftime("%Y-%m-%d")).first()
    #if not obj:
    saves = MonitorsInfo()
    saves.url = url
    saves.userid = token["user_id"]
    saves.username = obj_data.first_name
    saves.city = obj_data.city
    saves.province = obj_data.province
    saves.headimgUrl = obj_data.headimgUrl
    saves.save()




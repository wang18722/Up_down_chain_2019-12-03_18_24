from oauth.models import CustomerInformation


def jwt_response_payload_handler(token, user, request):
    """系统的方法,只返回了token,不满足需求,所以改写,使用我们自己的"""

    return {
        "token":token,
        "username":user.username if user else "",
        "user_id":user.id if user else "",
        'headimgUrl': user.headimgUrl if user else "",
    }

def get_user_by_account(account):

    try:
        user = CustomerInformation.objects.get(username=account)
    except CustomerInformation.DoesNotExist:
        user = None

    return user
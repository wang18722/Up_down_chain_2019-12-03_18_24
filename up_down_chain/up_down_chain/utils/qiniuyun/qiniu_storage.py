import qiniu
access_key = "a315reVm9pDHs7dlVDOAQbdrpyUN03rcE36Rvo8J"
secret_key = "UPFqPJOP8A79zS5zqDYGnAieuCBa-dNaakp71VBa"
bucket_name = "up_down_chain"


def storage(data):
    '''
        access_key      秘钥管理 - AK
        secret_key      秘钥管理 - SK
        bucket_name     空间名
    '''
    try:
        q = qiniu.Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = qiniu.put_data(token, None, data)
        # print(ret)
        # print(info)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传图片失败")

        # 返回七牛中保存的图片名
    return ret["key"]


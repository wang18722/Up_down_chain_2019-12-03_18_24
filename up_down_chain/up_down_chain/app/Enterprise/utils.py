from rest_framework.pagination import PageNumberPagination


class EnterprisesPageNum(PageNumberPagination):
    """分页器"""
    page_size_query_param = 'page_size'
    max_page_size = 10


# 做一个扩展性功能文件
# 1.接收一个id

def value(func):
    table_obj = {
        "ANlmy": 1,  # 农、林、牧、渔业
        "BCky": 2,  # 采矿业
        "CZzy": 3,  # 制造业
        "DDrrsgy": 4,  # 电力、热力、燃气及水生产和供应业
        "EJzy": 5,  # 建筑业
        "FPflsy": 6,  # 批发和零售业
        "GJcy": 7,  # 交通运输、仓储和邮政业
        "HZscyy": 8,  # 住宿和餐饮业
        "IXxrjy": 9,  # 信息传输、软件和信息技术服务业
        "JJry": 10,  # 金融业
        "KFdcy": 11,  # 房地产业
        "LZlsw": 12,  # 租赁和商务服务业
        "MKyjs": 13,  # 科学研究和技术服务业
        "NSlhjgg": 14,  # 水利、环境和公共设施管理业
        "OJmxl": 15,  # 居民服务、修理和其他服务业
        "PJy": 16,  # 教育
        "QWssh": 17,  # 卫生和社会工作
        "RWty": 18,  # 文化、体育和娱乐业
        "SGgsh": 19,  # 公共管理、社会保障和社会组织
        "TGj": 20,  # 国际组织
        #
    }

    key = list(table_obj.keys())[list(table_obj.values()).index(func)]

    return key


def num_func(func):
    table_obj = {
        "ACount": 1,  # 农、林、牧、渔业
        "BCount": 2,  # 采矿业
        "CCount": 3,  # 制造业
        "DCount": 4,  # 电力、热力、燃气及水生产和供应业
        "ECount": 5,  # 建筑业
        "FCount": 6,  # 批发和零售业
        "GCount": 7,  # 交通运输、仓储和邮政业
        "HCount": 8,  # 住宿和餐饮业
        "ICount": 9,  # 信息传输、软件和信息技术服务业
        "JCount": 10,  # 金融业
        "KCount": 11,  # 房地产业
        "LCount": 12,  # 租赁和商务服务业
        "MCount": 13,  # 科学研究和技术服务业
        "NCount": 14,  # 水利、环境和公共设施管理业
        "OCount": 15,  # 居民服务、修理和其他服务业
        "PCount": 16,  # 教育
        "QCount": 17,  # 卫生和社会工作
        "RCount": 18,  # 文化、体育和娱乐业
        "SCount": 19,  # 公共管理、社会保障和社会组织
        "TCount": 20,  # 国际组织
        #
    }

    key = list(table_obj.keys())[list(table_obj.values()).index(func)]

    return key






class EnterprisePageNum(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 20
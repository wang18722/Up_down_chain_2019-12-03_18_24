def toXML(dict_data):
    """
    设置xml
    :param dict_data:
    :return:
    """
    xml = '<xml>'
    for key,value in dict_data.items():
        xml = xml + '<'+key+'><![CDATA['+value+']]></'+key+'>'
    xml = xml + '</xml>'

    return xml


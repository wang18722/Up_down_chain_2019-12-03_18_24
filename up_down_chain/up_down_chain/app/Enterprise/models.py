# # from django.contrib.auth.models import AbstractUser
from django.db import models


#
#
# #
# # # Create your models here.
# #
class Provinces(models.Model):
    """省份表"""
    provinces = models.CharField(max_length=20, verbose_name="省份")

    class Meta:
        db_table = 'db_Provinces'
        verbose_name = '省份信息'


class Chain(models.Model):
    """下链行业表"""
    industry = models.CharField(max_length=28, verbose_name="行业")
    eng_industry = models.CharField(max_length=20, verbose_name="行业英文名")

    class Meta:
        db_table = 'db_Chain'
        verbose_name = '行业信息'
class Enterprises(models.Model):
    """企业信息"""
    enterprise = models.CharField(max_length=128, verbose_name="企业")
    access_count = models.IntegerField(verbose_name="访问数量",default=1)
    recommended_count = models.IntegerField(verbose_name="推荐总数",default=1)
    chain = models.ForeignKey("Chain", on_delete=models.CASCADE, verbose_name="外键")
    provinces = models.ForeignKey("Provinces", on_delete=models.CASCADE, verbose_name="外键")

    class Meta:
        db_table = 'db_Enterprises'

from Users.models import EnterpriseCertificationInfo
class Datasummary(models.Model):
    summary_id = models.AutoField(db_column='Summary_id', primary_key=True)  # Field name made lowercase.
    industry = models.CharField(db_column='Industry', max_length=255, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'datasummary'


class Function(models.Model):
    """功能模型类"""

    default_page = models.BooleanField(default=0,verbose_name="默认首页状态")
    i_recommend = models.BooleanField(default=0,verbose_name="我推荐状态")
    company_id = models.CharField(max_length=50, verbose_name="企业id")
    industry_id = models.CharField(max_length=50, verbose_name="行业id")
    follow = models.CharField(max_length=5,verbose_name="临时关注字段",null=True)
    user = models.ForeignKey(EnterpriseCertificationInfo, on_delete=models.CASCADE, verbose_name="外键",default='')

    class Meta:
        db_table = 'db_Function'
        verbose_name = '企业基本信息'


class Count(models.Model):
    """总数表"""
    count = models.CharField(max_length=16, verbose_name="总数")
    provinces = models.ForeignKey(Provinces, on_delete=models.CASCADE, verbose_name="外键")
    industry = models.ForeignKey(Chain, on_delete=models.CASCADE, verbose_name="外键")

    class Meta:
        db_table = 'db_Count'
        verbose_name = '行业信息'


class PreciseRetrieval(models.Model):
    """精准搜索表"""
    industry = models.CharField(max_length=30, verbose_name="行业")
    provinces = models.CharField(max_length=30, verbose_name="省份")
    business = models.CharField(max_length=30, verbose_name="业务")
    enterprise = models.CharField(max_length=30, verbose_name="企业名称")
    certification = models.BooleanField(verbose_name="企业认证", default=False)
    money = models.BigIntegerField(verbose_name="注册资金")
    mobile = models.CharField(max_length=11, verbose_name='手机号')

    class Mate:
        db_table = 'db_PreciseRetrieval'
        verbose_name = '数据信息'

    def __str__(self):
        return self.industry


class EnterpriseInformationForCustomer(models.Model):
    """用户自定义企业信息表"""
    company_id_customized = models.AutoField(db_column='Company_id_customized',
                                             primary_key=True)  # Field name made lowercase.
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True,
                                                  null=True)  # Field name made lowercase.
    column_registered_capital = models.CharField(db_column='Column_registered_capital', max_length=255, blank=True,
                                                 null=True)  # Field name made lowercase.
    status = models.CharField(max_length=50, blank=True, null=True)
    legal_representative = models.CharField(max_length=255, blank=True, null=True)
    registration_authority = models.CharField(max_length=255, blank=True, null=True)
    established_time = models.DateTimeField(blank=True, null=True)
    type_of_enterprise = models.CharField(max_length=50, blank=True, null=True)
    industry_involved = models.CharField(max_length=50, blank=True, null=True)
    staff_size = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mailbox = models.CharField(max_length=100, blank=True, null=True)
    official_website = models.CharField(max_length=2000, blank=True, null=True)
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True,
                                        null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    enterprise = models.ForeignKey(Enterprises, on_delete=models.CASCADE, verbose_name="外键", null=True)

    class Meta:
        db_table = 'Enterprise_information_for_customer'


class ACount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'A_count'

class BCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'B_count'

class CCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'C_count'

class DCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'D_count'

class ECount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'E_count'

class FCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'F_count'


class GCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'G_count'


class HCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'H_count'


class ICount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'I_count'


class JCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'J_count'


class KCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'K_count'


class LCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'L_count'


class MCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'M_count'


class NCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'N_count'


class OCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'O_count'


class PCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'P_count'


class QCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'Q_count'


class RCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'R_count'


class SCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'S_count'


class TCount(models.Model):
    access_count = models.IntegerField(blank=True, null=True)
    recommended_count = models.IntegerField(blank=True, null=True)
    company_id = models.CharField(primary_key=True, max_length=50)

    class Meta:

        db_table = 'T_count'


class DatasummaryForUp(models.Model):
    """上链数据表"""
    summary_id = models.AutoField(db_column='Summary_id', primary_key=True)  # Field name made lowercase.
    industry = models.CharField(db_column='Industry', max_length=255, blank=True, null=True)  # Field name made lowercase.
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    industryid = models.IntegerField(verbose_name="行业id")

    class Meta:

        db_table = 'datasummary_for_up'















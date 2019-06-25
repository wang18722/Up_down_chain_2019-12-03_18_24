from django.db import models


class ANlmy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'a_nlmy'


class BCky(models.Model):
    company_id = models.CharField(max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(primary_key=True,max_length=255)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)
    id = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'b_cky'




class CZzy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=50)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=5, blank=True, null=True)
    legal_representative = models.CharField(max_length=100, blank=True, null=True)
    registration_authority = models.CharField(max_length=200, blank=True, null=True)
    established_time = models.DateTimeField(blank=True, null=True)
    type_of_enterprise = models.CharField(max_length=50, blank=True, null=True)
    industry_involved = models.CharField(max_length=50, blank=True, null=True)
    staff_size = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mailbox = models.CharField(max_length=100, blank=True, null=True)
    official_website = models.TextField(blank=True, null=True)
    business_address = models.CharField(db_column='Business_address', max_length=200, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    registration_mark = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=50, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'c_zzy'


class DDrrsgy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'd_drrsgy'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class EJzy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'e_jzy'


class FPflsy(models.Model):
    company_id = models.CharField(max_length=50)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=5, blank=True, null=True)
    legal_representative = models.CharField(max_length=100, blank=True, null=True)
    registration_authority = models.CharField(max_length=200, blank=True, null=True)
    established_time = models.DateTimeField(blank=True, null=True)
    type_of_enterprise = models.CharField(max_length=50, blank=True, null=True)
    industry_involved = models.CharField(max_length=50, blank=True, null=True)
    staff_size = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mailbox = models.CharField(max_length=100, blank=True, null=True)
    official_website = models.TextField(blank=True, null=True)
    business_address = models.CharField(db_column='Business_address', max_length=200, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    registration_mark = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=50, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'f_pflsy'


class GJcy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_jcy'


class HZscyy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'h_zscyy'


class IXxrjy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'i_xxrjy'


class JJry(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'j_jry'


class KFdcy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'k_fdcy'


class LZlsw(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'l_zlsw'


class MKyjs(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'm_kyjs'


class NSlhjgg(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'n_slhjgg'


class OJmxl(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'o_jmxl'


class PJy(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'p_jy'


class QWssh(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'q_wssh'


class RWty(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'r_wty'


class SGgsh(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 's_ggsh'


class TGj(models.Model):
    company_id = models.CharField(primary_key=True, max_length=200)
    unified_social_credit_code = models.CharField(db_column='Unified_social_credit_code', max_length=50, blank=True, null=True)  # Field name made lowercase.
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
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
    business_address = models.CharField(db_column='Business_address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    business_scope = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    registration_mark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(db_column='Province', max_length=255, blank=True, null=True)  # Field name made lowercase.
    kind = models.TextField(db_column='Kind', blank=True, null=True)  # Field name made lowercase.
    industries = models.CharField(max_length=50, blank=True, null=True)
    industriesid = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_gj'

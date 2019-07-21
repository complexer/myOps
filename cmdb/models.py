from django.db import models


# from datetime import datetime
# import mongoengine
#
# class ObjectModel(mongoengine.Document):
#     object_id = mongoengine.StringField(max_length=32, required=True)
#     object_name = mongoengine.StringField(max_length=32)
#     attrList = mongoengine.ListField()
#     # create_time = mongoengine.DateTimeField(default=datetime.now)
#     create_time = mongoengine.StringField(max_length=32, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     create_user = mongoengine.StringField(max_length=32)


ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"异常"),
    (str(5), u"其它"),
    )

ASSET_TYPE = (
    (str(1), u"PC机"),
    (str(2), u"机架服务器"),
    (str(3), u"小型机"),
    (str(4), u"网络设备"),
    (str(5), u"安全设备"),
    (str(6), u"存储设备"),
    (str(7), u"其他")
    )


HOST_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"云主机")
    )


ASSET_ENV = (
    (str(1), u"开发环境"),
    (str(2), u"测试环境"),
    (str(3), u"预发布环境"),
    (str(4), u"生产环境")
    )


class HostModel(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", blank=True, null=True)
    ip = models.GenericIPAddressField(u"管理IP", max_length=15)
    ssh_port = models.CharField("ssh端口", max_length=32, default="22")
    mac = models.CharField(verbose_name=u"mac地址", max_length=32, blank=True, unique=True, null=True)
    username = models.CharField(verbose_name=u"账号", max_length=32, blank=True, null=True)
    password = models.CharField(verbose_name=u"密码", max_length=32, blank=True, null=True)
    other_ip = models.CharField(verbose_name=u"其它IP", max_length=100, blank=True, null=True)
    host_type = models.CharField(verbose_name=u"主机类型", choices=HOST_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField(verbose_name=u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(verbose_name=u"操作系统", max_length=100, blank=True, null=True)
    vendor = models.CharField(verbose_name=u"设备厂商", max_length=50, blank=True, null=True)
    up_time = models.CharField(verbose_name=u"上架时间", max_length=50, blank=True, null=True)
    cpu_model = models.CharField(verbose_name=u"CPU型号", max_length=100, blank=True, null=True)
    cpu_num = models.CharField(verbose_name=u"CPU数量", max_length=100, blank=True, null=True)
    memory = models.CharField(u"内存大小", max_length=30, blank=True, null=True)
    disk = models.CharField(u"硬盘信息", max_length=255, blank=True, null=True)
    sn = models.CharField(u"SN号码", max_length=60, blank=True, null=True)
    position = models.CharField(u"所在位置", max_length=100, blank=True, null=True)
    environment = models.CharField(u"环境", choices=ASSET_ENV, max_length=32, blank=True, null=True)
    is_delete = models.BooleanField("是否删除,1删除，0正常", default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, null=True)
    update_time = models.DateTimeField("更新时间", auto_now=True, null=True)
    remarks = models.TextField(u"备注信息", max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ("hostname", "ip")


class DeviceModel(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"设备名称", unique=True)
    company = models.CharField(max_length=50, verbose_name=u"设备品牌")
    model = models.CharField(max_length=50, verbose_name=u"设备型号")
    area = models.CharField(max_length=50, verbose_name=u"存放区域")
    purchase_date = models.DateField(verbose_name=u"购买日期", blank=False)
    mex_date = models.DateField(verbose_name="维保到期", blank=False)
    manager_addr = models.TextField(verbose_name="管理地址", max_length=200, blank=True)
    business_addr = models.CharField(verbose_name="业务地址", max_length=255, blank=True)
    username = models.CharField(verbose_name="登录账号", max_length=50)
    password = models.CharField(verbose_name="登录密码", max_length=50)
    sn_number = models.CharField(verbose_name=u"设备序列号", max_length=60, blank=True)
    device_type = models.CharField(verbose_name="设备类型", choices=ASSET_TYPE, max_length=30, blank=True)
    is_delete = models.BooleanField("是否删除,1删除，0正常", default=0)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    remarks = models.TextField(verbose_name="备注", blank=True)


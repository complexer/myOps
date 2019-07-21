from django.test import TestCase

from .models import HostModel

class ObjectTestCase(TestCase):
    def setUp(self):
        # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(current_time)
        # ObjectModel.objects.create(object_id='docker', object_name='k8s', attrList=[1,2],  create_user='lingjian')

        HostModel.objects.create(ip="192.168.34.20", account="root", password="111111")


    def test_object(self):
        # a = ObjectModel.objects.all()
        # print(a[2].create_time)
        hosts = HostModel.objects.all()
        print(hosts)
        # for host in hosts:
        #     print(host.ip)
        #     task = AnsibleTask([AnsibleHost(host.ip, 22, 'ssh', host.account, host.password)])
        #     res = task.exec_shell('echo "abc"')
        #     print(res)


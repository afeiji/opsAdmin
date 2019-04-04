#encoding:utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from asset.serilalizsers import HostSerilalizer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from asset.models import Host
from devops.settings import FJAccessKeyId, FJAccessKeySecret


# 创建AcsClient实例
client = AcsClient(
  FJAccessKeyId,
  FJAccessKeySecret,
  "cn-shenzhen"
)

def get_host():
    # 创建request，并设置参数
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_PageSize(10)
    # 发起API请求并显示返回值
    response = client.do_action_with_exception(request)
    return response

def save_host():
    host = get_host()
    stream = BytesIO(host)
    data = JSONParser().parse(stream)
    host_list = data['Instances']['Instance']
    host_list_instanceId = []
    for _host in host_list:
        data_dict = {}  # 序列化需要字典验证才能通过
        data_dict['cloud'] = 1  # 1是阿里云
        data_dict['cpu'] = str(_host['Cpu'])
        data_dict['memory'] = str(_host['Memory'])
        data_dict['creationtime'] = _host['CreationTime']
        data_dict['expiredTime'] = _host['ExpiredTime']
        data_dict['instancechargetype'] = _host['InstanceChargeType']
        data_dict['instanceId'] = _host['InstanceId']
        host_list_instanceId.append(_host['InstanceId'])
        data_dict['instancename'] = _host['InstanceName']
        data_dict['status'] = _host['Status']
        data_dict['privateipaddress'] = _host['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
        if len( _host['PublicIpAddress']['IpAddress']) > 0:
            data_dict['publicipaddress'] = _host['PublicIpAddress']['IpAddress'][0]
        data_dict['zoneid'] = _host['ZoneId']

        host_serilalizer = HostSerilalizer(data=data_dict)
        if host_serilalizer.is_valid():
            host_serilalizer.save()
        else:
            print("serializer.errors: ", host_serilalizer.errors)

        # 将不存在主机删除
    delete_host(host_list_instanceId)

def delete_host(host_list_instanceId):
    queryset = Host.objects.all()
    instanceId_list = []
    for obj in queryset:
        if obj.instanceId not in host_list_instanceId:
            obj.delete()

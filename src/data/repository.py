
from data.setting import session
from data.table import InstanceStatus,InstanceInfo,User,IpAddress
from sqlalchemy import func

def add_instanse_status_starting(name):

    add_user = User()
    add_user.name = name
    add_user.private_key = 'nothing'
    session.add(add_user)
    session.commit()
    userId = add_user.id

    add_status = InstanceStatus()
    add_status.userId = userId
    add_status.instanceStatus = 'starting'

    session.add(add_status)
    session.commit()
    instanceId = add_status.id
    session.close()
    return userId,instanceId

def count_utm_memory_size(utm):

    count_utm_memory = InstanceInfo()
    count = session.query(InstanceInfo).count()
    session.close()
    # session.close()

    memorys = 0

    if count > 0:
        memorys = session.query(func.sum(InstanceInfo.memory)).filter(InstanceInfo.utm == utm)
        session.close()
    return memorys

def add_instanse_status_intializing(instanceId):

    update_status = session.query(InstanceStatus).filter(InstanceStatus.id == instanceId)
    update_status.instanceStatus = 'intializing'

    session.commit()
    session.close()
    return

def add_instanse_status_running(instanceId):

    update_status = session.query(InstanceStatus).filter(InstanceStatus.id == instanceId)
    update_status.instanceStatus = 'running'

    session.commit()
    session.close()
    return

def register_private_key(userId,private_key):
    register_private_key = session.query(User).filter(User.id == userId).first()
    register_private_key.private_key = private_key
    session.commit()
    session.close()
    return

def register_instance_info(instanseId,docker_id,memory_size,cpu_size,utm):

    instance_info = InstanceInfo()

    instance_info.instanceId = instanseId
    instance_info.docker_id = docker_id

    instance_info.memory = memory_size
    instance_info.cpu = cpu_size
    instance_info.utm = utm

    session.add(instance_info)
    session.commit()
    session.close()
    return


def instance_info(instanceId, userId):

    user = session.query(User).filter(User.id == userId).first()
    session.commit()
    instance_info = session.query(InstanceInfo).filter(InstanceInfo.instanceId == instanceId).first()
    session.commit()

    return user.name, user.private_key, instance_info.utm, instance_info.ipAddress, instance_info.port, instance_info.docker_id

def update_instanse_status_stopping(instanceId):
    update_status = session.query(InstanceStatus).filter(InstanceStatus.id == instanceId)
    update_status.instanceStatus = 'stopping'
    session.commit()
    session.close()
    return

def getIpAddress():
    ipAddress = session.query(IpAddress).filter(IpAddress.used == 'unused').first()
    return ipAddress

def chengeIpAddressUsed(ipAddress_id):
    update_used = session.query(IpAddress).filter(IpAddress.id == ipAddress_id)
    update_used.used = 'used'
    session.commit()
    session.close()
    return


def getUserInfo(userId):
    userInfo = session.query(User).filter(User.id == userId).first()
    return userInfo

def delete_all(userId,instanceId):
    delete_instance_info = session.query(InstanceInfo).filter(InstanceInfo.id == instanceId).first()
    session.delete(delete_instance_info)
    session.commit()
    
    delete_instance_status = session.query(InstanceStatus).filter(InstanceStatus.id == instanceId).first()
    session.delete(delete_instance_status)
    session.commit()

    delete_user_info = session.query(User).filter(User.id == userId).first()
    session.delete(delete_user_info)

    session.commit()
    session.close()
    return
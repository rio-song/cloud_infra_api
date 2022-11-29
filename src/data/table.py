from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import  relationship


from data.setting import Engine
from data.setting import Base


# from setting import Engine
# from setting import Base



class User(Base):
    __tablename__ = 'users'
    __table_args__ = {
        'comment': 'user_master_table'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(200))
    private_key = Column('private_key', String(2000))
    instance_status = relationship("InstanceStatus")

class InstanceStatus(Base):
    __tablename__ = 'instance_status'
    __table_args__ = {
        'comment': 'instance_status_table'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    userId = Column('userId', Integer, \
                    ForeignKey('users.id',onupdate='CASCADE', ondelete='CASCADE'))
    instanceStatus = Column('instance_status', String(100))
    user = relationship("User", back_populates="instance_status")
    instance_info = relationship("InstanceInfo")


class InstanceInfo(Base):
    __tablename__ = 'instance_info'
    __table_args__ = {
        'comment': 'instance_info_table'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    instanceId = Column('instanceId', Integer, \
                    ForeignKey('instance_status.id',onupdate='CASCADE', ondelete='CASCADE'))
    utm = Column('utm', Integer)
    ipAddressId = Column= Column('ipAddressId', Integer, \
                    ForeignKey('ipAddress.id',onupdate='CASCADE', ondelete='CASCADE'))
    dockerId = Column('dockerId', String(200))
    port = Column('port', String(200))
    cpu = Column('cpu',  String(200))
    memory = Column('memory', Integer)

    instance_status = relationship("InstanceStatus", back_populates="instance_info")
    instance_status = relationship("IpAddress", back_populates="instance_info")


class IpAddress(Base):
    __tablename__ = 'ipAddress'
    __table_args__ = {
        'comment': 'ipAddress'
    }

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    IpAddress = Column('ipAddress', String(200))
    used = Column('used',  String(200),default='unused')
    instance_info = relationship("InstanceInfo")


if __name__ == "__main__":
    # create table
    Base.metadata.create_all(Engine)
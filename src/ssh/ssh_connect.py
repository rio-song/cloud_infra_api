
import paramiko
import io

def make_key():

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    client.connect('localhost',port=22, username='riosong', password='*pwd*')
    print("鍵生成スタート")

    key = paramiko.RSAKey.generate(2048)
    print("鍵生成完了")

    privateString = io.StringIO()
    key.write_private_key(privateString)
    print("公開鍵書き出し")
    public = key.get_base64()
    privarte = privateString.getvalue()

    path = './id_rsa.pub'
    f = open(path, 'w')
    f.write(public)
    f.close()

    return privarte

def connect_container_by_ssh(id_rsa):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect('localhost',port=22, username='riosong', password='*pwd*')
    client.exec_command("ssh root@localhost -i " + id_rsa, get_pty=True) 

    client.close()

    return


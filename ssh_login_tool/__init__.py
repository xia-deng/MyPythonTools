'''
基于Python的ssh 远程自动登陆代码
目的是为了保存多个远程环境，减少输入的时间
注意，该脚本只适用于Linux系统
'''

import sys
import pexpect

envs = {'TEST1': ['user', 'port', '10.1.1.1', 'p1'], 'TEST2': ['user', 'port', '10.2.2.2', 'p2'],
        'TEST3': ['user', 'port', '10.2.2.3', 'p4']}

'''
expect方法的第二个参数pattern是一个多值参数，可以传入多个判断条件
它的返回index==0是指一个都没匹配到
index==1表示匹配到了第一个，所以这里当index==2,表示，不需要密码就能登陆
'''
def ssh_login(env):
    ssh_newkey = "Are you sure you want to continue connecting"
    connected_key = "]#"
    username, port, ip, passw = select_envs(env)
    port = 22 if port is None else port
    ssh_cmd = pexpect.spawn('ssh %s@%s -p %s -y' % (username, ip, port), timeout=1)
    fout = file('mylog.txt', 'w')
    ssh_cmd.logfile = fout
    ret = ssh_cmd.expect([pexpect.TIMEOUT, ssh_newkey, connected_key, '[P|p]assword:'])
    print()
    if ret == 0:
        print('[-] Error Connecting')
        return
    if ret == 1:
        ssh_cmd.sendline('yes')
        ret = ssh_cmd.expect([pexpect.TIMEOUT, ssh_newkey, connected_key, '[P|p]assword:'])
        if ret == 0:
            print('[-] Error Connecting')
            return
    ssh_cmd.sendline(passw)
    ssh_cmd.expect(PROMPT)
    print(ssh_cmd.before)
    ssh_cmd.interact()
    ssh_cmd.close()


def select_envs(env):
    return envs[env][0], envs[env][1], envs[env][2], envs[env][3]


def show_envs():
    print('')
    print('Here is all the envs list here:')
    for item in envs:
        print('env:%s, attributes:%s' % (item, str(envs[item])))
    print('')


if __name__ == '__main__':
    for arg in sys.argv:
        print(arg)
    env = sys.argv[1].upper()
    if (envs.__contains__(env)):
        ssh_login(env)
    elif env == '--H':
        show_envs()
    else:
        print('not this env. use python ssh_login.py --h to list all the envs')

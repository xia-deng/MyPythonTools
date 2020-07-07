'''
基于Python的ssh 远程自动登陆代码
目的是为了保存多个远程环境，减少输入的时间
注意，该脚本只适用于Linux系统
'''

import sys
import pexpect

envs = {'TEST1': ['user', 'port', '10.1.1.1', 'p1'], 'TEST2': ['user', 'port', '10.2.2.2', 'p2'],
        'TEST3': ['user', 'port', '10.2.2.3', 'p4']}


def ssh_login(env):
    username, port, ip, passw = select_envs(env)
    port = 22 if port is None else port
    ssh_cmd = pexpect.spawn('ssh %s@%s -p %s -y' % (username, ip, port), timeout=30)
    fout = file('mylog.txt', 'w')
    ssh_cmd.logfile = fout
    password_index = ssh_cmd.expect('password')
    if password_index == 0:
        ssh_cmd.sendline(passw)
        index = ssh_cmd.expect('$')
        if index != 0:
            exit(b'password is not correct.')
        print(ssh_cmd.before)
        ssh_cmd.interact()
    else:
        print('the index is:%d,cannot find something.' % password_index)
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

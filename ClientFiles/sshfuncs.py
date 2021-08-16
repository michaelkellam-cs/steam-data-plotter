import paramiko as pm
import tkinter
from tkinter.filedialog import askopenfile

#ssh = pm.SSHClient()


# Attempts to log the SSH object (paramiko) in using a .PEM file as the password
def login(ip, user, password, ssh):
    #global ssh
    #host = '18.204.202.170'
    #username = 'admin'
    #password = pm.RSAKey.from_private_key_file('C:\\Users\\bobby\\Downloads\\defaultsshkeypair.pem')
    ssh.set_missing_host_key_policy(pm.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip, username=user, pkey=password, timeout=5)
        return True
    except:
        return False
    

# Gets the output of a linux command
def output(command, ssh):
    try:
        stdin, stdout, stderr = ssh.exec_command('sudo bash -c \'' + command + '\'', get_pty=True)
    except:
        print('Error...' + stderr + ', stdin: ' + stdin)
    ssh.exec_command(command, get_pty=True)
    my_str = ''
    for line in iter(stdout.readline, ""):
        #print(line, end="")
        my_str += line
    return my_str

# Verifies that the SSH connection is still active
def check_connection(ssh):
    try:
        ssh.exec_command('ls', timeout=5)
        return True
    except Exception as e:
        print("Connection lost : %s", e)
        return False



def add_game(appid, ssh):
    game_set = set()
    stdin, stdout, stderr = ssh.exec_command('sudo bash -c \'' + 'cat games.txt' + '\'', get_pty=True)
    for line in iter(stdout.readline, ""):
        #print(line, end="")
        game_set.add(line)
    found = check_found(appid, ssh)
    print('Does it? ' + str(str(appid) in game_set))
    app_str = 'echo \"' + str(appid) + '\" >> steamgame/games.txt'
    if not found:
        ssh.exec_command('sudo bash -c \'' + app_str + '\'', get_pty=True)
        return True
    return False


# Determines if a given appid already exists in the games.txt file.
def check_found(appid, ssh):
    game_set = set()
    stdin, stdout, stderr = ssh.exec_command('sudo bash -c \'' + 'cat steamgame/games.txt' + '\'', get_pty=True)
    for line in iter(stdout.readline, ""):
        #print(line, end="")
        game_set.add(line.strip())
    return appid in game_set
    

# Gets file name location of selected file
def get_file():
    pem_file = askopenfile()
    print(pem_file.name)
    return pem_file


#add_game(578080)


        
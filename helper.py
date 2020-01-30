from cryptography.fernet import Fernet
from gcsfs import GCSFileSystem
from environs import Env
import pystache

env = Env()
env.read_env()

GOOGLE_CLOUD_PROJECT = env('GOOGLE_CLOUD_PROJECT')
TOKEN_LOCATION = env('TOKEN_LOCATION')
BEAST_SECRET = env('BEAST_SECRET')
fs = GCSFileSystem(project=GOOGLE_CLOUD_PROJECT)
crypt = Fernet(BEAST_SECRET)

def get_template():
    with open('template.yaml') as f:
        return f.read()

def write_template(i, s):
    with open(f'secret-kube/{i}.yaml', 'w') as f:
        f.write(s)

for i,fi in enumerate(fs.ls(TOKEN_LOCATION)):
    with fs.open(fi, 'rb') as f:
        secret = crypt.decrypt(f.read())
        secret = secret.decode('utf8')
        token = fi.split('/')[-1]
        t = get_template()

        s = pystache.render(t, {'idx': i,
                            'token': token,
                            'secret': secret })
        write_template(i, s)

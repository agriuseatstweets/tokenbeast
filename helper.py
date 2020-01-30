from cryptography.fernet import Fernet
from gcsfs import GCSFileSystem
from environs import Env

env = Env()
env.read_env()

GOOGLE_CLOUD_PROJECT = env('GOOGLE_CLOUD_PROJECT')
TOKEN_LOCATION = env('TOKEN_LOCATION')
BEAST_SECRET = env('BEAST_SECRET')
fs = GCSFileSystem(project=GOOGLE_CLOUD_PROJECT)
crypt = Fernet(BEAST_SECRET)

for fi in fs.ls(TOKEN_LOCATION):
    with fs.open(fi, 'rb') as f:
        secret = crypt.decrypt(f.read())
        secret = secret.decode('utf8')
        key = fi.split('/')[-1]
        print(key, secret)

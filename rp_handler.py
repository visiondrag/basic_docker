import runpod
import time
import sys
from .code.func import list_current_folder

def handler(event):

    return list_current_folder()

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler })

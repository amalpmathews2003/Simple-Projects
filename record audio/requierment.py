import os

def install(module):
	try:
		os.system(f'pip3 install {module}')
	except Exception as e:
		os.system(f'pip install {module}')
	else:
		os.system(f'python3 -m pip install {module}')
	finally:
		os.system(f'python -m pip install {module}')
def unistall(module):
	try:
		os.system(f'pip3 uninstall -y {module}')
	except Exception as e:
		os.system(f'pip uninstall -y {module}')
	else:
		os.system(f'python3 -m pip uninstall -y {module}')
	finally:
		os.system(f'python -m pip uninstall -y {module}')

if __name__ == '__main__':
	install("playsound pyaudio ")
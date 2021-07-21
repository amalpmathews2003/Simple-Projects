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

if __name__ == '__main__':
	install('PyQt5')
	install('PyQtWebEngine')
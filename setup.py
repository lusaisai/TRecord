from setuptools import setup

setup(
    name='TRecord',
    version='1.0.0',
    packages=['trecord'],
    url='https://github.com/lusaisai/TRecord',
    license='MIT',
    author='lusaisai',
    author_email='lusaisai@163.com',
    description='An Interactive SQL Client',
    scripts=[
        'scripts/trecord'
    ]
)

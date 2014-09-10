from distutils.core import setup

setup(
    name='pypail',
    version='0.0.1',
    description="Access the Digital Ocean API with Python scripts",
    author='Nathan Osman',
    author_email='admin@quickmediasolutions.com',
    url='https://github.com/nathan-osman/pypail',
    license='MIT',
    packages=['pypail'],
    install_requires=['requests', 'python-dateutil'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)

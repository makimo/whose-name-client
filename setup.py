from setuptools import setup, find_packages

setup(
    name='whosename-client',
    version='1.0.0',
    description='Whosename API client',
    author='Michał Moroz <michal@makimo.pl>',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=('whosename',),
    package_dir={'': 'src'},
    install_requires=['docopt', 'requests'],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'whosename = whosename.query_service:main',
            'whosename-login = whosename.request_token:main',
        ],
    }
)
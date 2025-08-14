from setuptools import setup, find_packages

setup(
    name='inventory-management-system',
    version='1.0.0',
    description='A full-stack inventory management system',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'flask==2.3.3',
        'mysql-connector-python==8.2.0',
        'python-dotenv==1.1.1',
        'werkzeug==2.3.7'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)

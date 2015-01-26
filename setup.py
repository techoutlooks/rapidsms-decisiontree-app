from setuptools import setup, find_packages


setup(
    name='rapidsms-decisiontree-app',
    version=__import__('decisiontree').__version__,
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/caktus/rapidsms-decisiontree-app/',
    license='BSD',
    description=" ".join(__import__('decisiontree').__doc__.splitlines()).strip(),
    long_description=open('README.rst').read(),
    classifiers=(
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ),
    zip_safe=False,
    install_requires=['RapidSMS>=0.19.0'],
)

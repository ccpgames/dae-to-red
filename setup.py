

from pip.req    import parse_requirements
from setuptools import setup, find_packages

from dae_to_red import __version__

install_reqs = parse_requirements('requirements.txt')
reqs         = [str(ir.req) for ir in install_reqs]

setup(
    name='dae-to-red',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        dae_to_red=dae_to_red.main:main
    ''',
)
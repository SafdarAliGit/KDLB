from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in kdlb/__init__.py
from kdlb import __version__ as version

setup(
	name="kdlb",
	version=version,
	description="This is shiping and cargo management system",
	author="TechVentural",
	author_email="safdar211@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

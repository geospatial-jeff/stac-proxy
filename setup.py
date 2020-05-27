from setuptools import setup, find_packages

with open('./requirements.txt') as reqs:
    requirements = [line.rstrip() for line in reqs]

setup(name="stac-proxy",
      version='0.0.1',
      author='Jeff Albrecht',
      author_email='geospatialjeff@gmail.com',
      packages=find_packages(),
      install_requires=requirements,
      python_requires=">=3.7",
      include_package_data=True
)
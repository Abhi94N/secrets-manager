import os
import sys

from setuptools import find_packages
from setuptools import setup

v = sys.version_info
if v[:2] < (3, 6):
  error = "ERROR: IllumiDesk requires Python version 3.6 or above."
  print(error, file=sys.stderr)
  sys.exit(1)

shell = False
if os.name in ("nt", "dos"):
    shell = True
    warning = "WARNING: Windows is not officially supported"
    print(warning, file=sys.stderr)

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join("_version.py")) as f:
    exec(f.read(), {}, version_ns)


setup(
    name="secretsmanager",
    version=version_ns["__version__"],
    description="IllumiDesk secrets-manager package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/illumidesk/secrets-manager",
    author="The IllumiDesk Team",
    author_email="hello@illumidesk.com",
    license="Apache 2.0",
    packages=find_packages(where=".",exclude="./tests"),
    install_requires=[
        "boto3==1.21.19",
        "botocore==1.24.21",
        "pytest==7.1.1"
    ],  # noqa: E231
    package_data={
        "": ["*.html"],
    },  # noqa: E231
)


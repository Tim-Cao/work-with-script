from setuptools import setup

with open("README.markdown", "r") as f:
    long_description = f.read()

setup(
    author="Yang Cao",
    author_email="yang.cao@liferay.com",
    description="A package for working with scripts",
    install_requires=[
        "GitPython",
        "jira",
        "jproperties",
        "jsonpath-ng",
        "pandas",
        "PyGithub",
        "textual",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["work-with-script"],
    name="work-with-script",
    url="https://github.com/Tim-Cao/work-with-script",
    version="3.0.1",
)

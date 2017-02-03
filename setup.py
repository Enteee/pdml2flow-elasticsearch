# vim: set fenc=utf8 ts=4 sw=4 et :
from setuptools import setup, find_packages

# I really prefer Markdown to reStructuredText. PyPi does not.
# from: https://coderwall.com/p/qawuyq/use-markdown-readme-s-in-python-modules
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst', format='markdown')
    long_description = long_description.replace('\r','')
    with open('README.rst', 'w') as f:
        f.write(long_description)
except (OSError, ImportError):
    print('Pandoc not found. Long_description conversion failure.')
    # pandoc is not installed, fallback to using raw contents
    with open('README.md', 'r') as f:
        long_description = f.read()

# Setup the project
setup(
    name = 'pdml2flow-elasticsearch',
    keywords = 'pdml2flow plugin elasticsearch',
    version = '0.1',
    packages = find_packages(exclude=['test']),
    install_requires = [
        'pdml2flow',
        'python-dateutil'
    ],
    entry_points= {
        'pdml2flow.plugins': 'elasticsearch = plugins.elasticsearch:Elasticsearch'
    },
    # metadata
    author = 'Mischa Lehmann',
    author_email = 'ducksource@duckpond.ch',
    description = 'Saves pdml2flow output in elasticsearch',
    long_description = long_description,
    include_package_data = True,
    license = 'Apache 2.0',
    url = 'https://github.com/Enteee/pdml2flow-elasticsearch',
)

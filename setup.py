import os

from setuptools import find_packages, setup

NAME = "eea.climateadapt"
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()


long_description = (open("README.rst").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read()),

setup(name='eea.climateadapt',
      version=VERSION,
      description="EEA ClimateAdapt for Plone",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea zope plone python',
      author='European Environment Agency',
      author_email='webadmin@eea.europa.eu',
      url='http://eea.github.io',
      license='gpl',
      packages=find_packages(),
      # package_dir = {'': 'eea'},
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.dexterity',
          'plone.namedfile [blobs]',
          # -*- Extra requirements: -*-
          'z3c.jbot',
          'pycountry',
          'collective.dexteritytextindexer',
          'collective.easyform',
          'tokenlib',
          'eea.rabbitmq.client',    # schedule jobs
      ],
      extras_require={
          'test': [
              'plone.app.testing',
           ],
          'importer': [
              'zope.sqlalchemy',
              'psycopg2',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      [console_scripts]
      climateadapt_importer = eea.climateadapt._importer:main
      sync_to_arcgis = eea.climateadapt.scripts.sync_to_arcgis:main
      arcgis_cli = eea.climateadapt.scripts.cli_arcgis_client:main
      send_mayoradapt_reminders = eea.climateadapt.mayorsadapt.scripts:send_reminders
      get_broken_links = eea.climateadapt.browser.scripts:get_broken_links
      archive_news = eea.climateadapt.browser.scripts:archive_news
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins=["templer.localcommands"],

      )

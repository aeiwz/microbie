import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'microbie',      
  packages = ['microbie'], 
  version = '0.0.1',  
  license='MIT', 
  description = 'Microbiome analysis and visualise',
  author = 'aeiwz',                 
  author_email = 'theerayut_aeiw_123@hotmail.com',   
  url = 'https://github.com/aeiwz/microbie.git',  
  download_url = 'https://github.com/aeiwz/microbie/archive/refs/tags/v0.0.1.tar.gz',  
  keywords = ['Microbiome', 'Sequencing', 'Analysis', 'Visualisation'],
  install_requires=[            
          'scikit-learn',
          'pandas',
          'numpy',
          'matplotlib',
          'seaborn',
          'scipy',
          'statsmodels',
          'plotly',
          'lingress',
          'metbit'],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',        
    'Programming Language :: Python :: 3.12',
  ],
)

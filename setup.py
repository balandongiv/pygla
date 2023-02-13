from setuptools import setup

setup(name='pygla',
      version='0.0.3',
      description='Automate group learning assessment',
      author='rpb',
      author_email = 'balandongiv@gmail.com',
      packages=['gla'],
      long_description='The pygla system is a python-based implementation of the The Evolution of a Peer Assessment Method for use in Group based Teaching of HCI. pygla stands for Pythonic-Based Group Learning Assessment. This new system serves as an upgrade from the previous Microsoft architecture-based implementation. The previous implementation was limited in several ways. Firstly, manual data entry of each entry from the Microsoft Word form into the excel template was time-consuming and complex. This manual approach was also prone to human error and limited to domain experts. With new teaching assistants every semester, the module convener had to constantly conduct or explain the procedure multiple times.pygla addresses these limitations with the goal of automating the entire process. While the system does require some coding skills, the requirements are minimal. The Python library is capable of receiving peer assessment inputs conducted using Microsoft Forms and also supports manual data entry for peer assessments collected using Microsoft Word.',
      install_requires=[
            'pandas',
      ]
      )

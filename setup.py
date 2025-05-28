#there are many packages in python
#will be responsible ML model as a package, anybody can use it
#we can use our application as a package

from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)-> List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        [req.replace("\n"," ") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)



setup(
nme='mlproject',
version='0.0.1',
author='Neha',
author_email= 'nehagovekar2198@gmail.com',
packages=find_packages(),
#install_requires=['pandas', 'numpy','seaborn']
install_requires=get_requirements('requirements.txt')
)
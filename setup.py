from setuptools import setup, find_packages
with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
setup(
    name="piersfan",
    version="0.0.1",
    description="Yokohama fishing piers fan",
    author="frsw3nr@gmail.com",
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "piersfan=piersfan.cli:main",
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ]
)
from setuptools import setup

setup(
    name = "CommitHero",
    version = "0.1",
    packages = ['commithero'],
    install_requires = ['anyvc'],
    entry_points = {
        'console_scripts': [
            'commithero = commithero:main',
        ],
    },
    description = "Achievements for Programmers",
    author = "Robert Lehmann",
    author_email = "mail@robertlehmann.de",
)

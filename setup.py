from setuptools import setup

setup(
    name = "CommitHero",
    version = "0.1",
    packages = ['commithero', 'commithero.achievements'],
    install_requires = ['anyvc'],
    entry_points = {
        'console_scripts': [
            'commithero = commithero:main',
        ],
    },
    test_suite = 'commithero.tests',
    tests_require = ['dulwich'],
    zip_safe = True,
    description = "Achievements for Programmers",
    author = "Robert Lehmann",
    author_email = "mail@robertlehmann.de",
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',
    ],
)

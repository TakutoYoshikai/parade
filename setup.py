from setuptools import setup, find_packages

setup(
    name = 'parade',
    version = '1.0.0',
    url = 'https://github.com/TakutoYoshikai/lina.git',
    license = 'MIT LICENSE',
    author = 'Takuto Yoshikai',
    author_email = 'takuto.yoshikai@gmail.com',
    description = "parade is an encoder/decoder of data",
    install_requires = ['setuptools'],
    packages = find_packages(),
    entry_points={
        "console_scripts": [
            "parade = parade.parade:main",
        ]
    }
)

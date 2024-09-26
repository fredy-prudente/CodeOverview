from setuptools import setup, find_packages

setup(
    name='CodeOverview',
    version='1.0.0',
    author='Fredy',
    author_email='thenomefredy@hotmail.com',
    description='Aplicação para gerar a estrutura de projetos e integrá-los com GPT.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fredy-prudente/CodeOverview',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt5>=5.15.0'
    ],
    entry_points={
        'console_scripts': [
            'CodeOverview=CodeOverview.main:run_app',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

import setuptools

setuptools.setup(
    name="chrome_trex",
    version="0.0.1",
    author="Fernando Kurike Matsumoto",
    author_email="ferkmatsumoto@gmail.com",
    description="A library with the chrome trex game",
    url="https://github.com/GrupoTuringCodes/chrome-trex-rush",
    license="MIT",
    packages=['chrome_trex'],
    package_data={'chrome_trex': ['sprites/*.png']},
    install_requires=['pygame'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup, find_packages


setup(
    name="tanink",
    version="0.1.0",
    description="Writing software for Raspberry PI zero W and e-paper IT8951 screen",
    author="Marion Vasseur",
    keywords="writing",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "keyboard==0.13.5",
        "asyncio==3.4.3",
        "pillow==8.2.0",
        # "epd-library==0.2.3",
    ],
    extras_require={
        "quality": [
            "pytest==6.2.4",
            "pytest-mock==3.6.1",
            "flake8==3.9.2",
        ]
    },
)

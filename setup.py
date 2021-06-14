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
        "keyboard==0.13.5"
    ],
    extras_require={
        "quality": [
            "pytest==6.2.4",
            "flake8==3.9.2",
        ]
    },
)

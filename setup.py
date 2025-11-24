from setuptools import find_packages, setup

def get_requirements(file_path: str) -> list[str]:
    """
    Read requirements.txt and return a list of dependencies.
    Ignores '-e .' and empty lines.
    """
    requirements = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            req = line.strip()
            if req and req != "-e .":
                requirements.append(req)
    return requirements

setup(
    name="heartdiseasedetectionproject",   # fixed spelling
    version="0.0.1",
    author="prajwal",
    author_email="prajwaljagtap977@gmail.com",  # fixed key name
    description="Heart disease detection project using ML",
    packages=find_packages(),              # auto-detect packages
    install_requires=get_requirements("requirements.txt"),# file path dilelea ahe ya madhe 
    python_requires=">=3.8",               # adjust if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

from setuptools import find_packages,setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='shashwat mishra',
    author_email='mishrashashwat066@gmail.com',
    install_requires=["huggingface-hub","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)
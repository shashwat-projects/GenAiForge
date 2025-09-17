from setuptools import find_packages,setup

setup(
    name='QuizForgeAI',
    version='0.0.1',
    author='shashwat mishra',
    author_email='mishrashashwat066@gmail.com',
    install_requires=["huggingface-hub","langchain","langchain-huggingface", "streamlit","python-dotenv","PyPDF2", "streamlit", "pandas", "os", "warnings", "json", "traceback", "logging"],
    packages=find_packages()
)
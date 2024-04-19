import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meta_ai_api",
    author="Roméo Phillips",
    author_email="phillipsromeo@gmail.com",
    description="Meta AI API Wrapper to interact with the Meta AI API",
    keywords="llm, ai, meta_ai_api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomchen/example_pypi_package",
    project_urls={
        "Documentation": "https://github.com/Strvm/meta-ai-api",
        "Bug Reports": "https://github.com/Strvm/meta-ai-api",
        "Source Code": "https://github.com/Strvm/meta-ai-api",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        "dev": ["check-manifest"],
    },
    install_requires=["requests", "requests-html", "lxml_html_clean"],
)

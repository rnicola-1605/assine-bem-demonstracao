import setuptools

with open('requirements.txt', 'r') as fh:
    requires = [i.replace('\n', '') for i in fh.readlines()]

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description += "\n------\n"

with open("CHANGES.md", "r") as fh:
    long_description += fh.read()

desc = "Produto Zope para demonstração de integração com Assine Bem."

setuptools.setup(
    name="assine-bem-demonstracao",
    version="1.0.0",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rnicola-1605/assine-bem-demonstracao",
    packages=setuptools.find_packages(),
    install_requires=requires,
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
    namespace_packages=["Products"],
    maintainer="Rodrigo Nicola",
    maintainer_email="rnicolasilva@gmail.com",
    author="Rodrigo Nicola",
    author_email="rnicolasilva@gmail.com"
)

from setuptools import setup

setup(
	name = "sklearn2pmml-plugin",
	version = "${project.python_version}",
	packages = [
		"com",
		"com.mycompany"
	],
	install_requires = [
		"sklearn2pmml>=0.17.2"
	]
)

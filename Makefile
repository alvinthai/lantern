run:  ## clean and make target, run target
	python3 -m lantern 

build:  ## Build the repository
	python3 setup.py build 

testpy: ## Clean and Make unit tests
	python3 -m pytest -v tests --cov=lantern

test: lint ## run the tests for travis CI
	@ python3 -m pytest -v tests --cov=lantern

lint: ## run linter
	flake8 lantern 

fix:  ## run autopep8/tslint fix
	autopep8 --in-place -r -a -a lantern/

annotate: ## MyPy type annotation check
	mypy -s lantern  

annotate_l: ## MyPy type annotation check - count only
	mypy -s lantern | wc -l 

clean: ## clean the repository
	find . -name "__pycache__" | xargs  rm -rf 
	find . -name "*.pyc" | xargs rm -rf 
	find . -name ".ipynb_checkpoints" | xargs  rm -rf 
	rm -rf .coverage cover htmlcov logs build dist *.egg-info
	make -C ./docs clean

install:  ## install to site-packages
	pip3 install .

preinstall:  ## install dependencies
	python3 -m pip install -r requirements.txt

postinstall:  ## install other requisite labextensions
	jupyter labextension install @jupyter-widgets/jupyterlab-manager
	jupyter labextension install @jupyterlab/plotly-extension
	jupyter labextension install @finos/perspective-jupyterlab
	jupyter labextension install jupyterlab_bokeh
	jupyter labextension install bqplot
	jupyter labextension install qgrid

docs:  ## make documentation
	make -C ./docs html
	open ./docs/_build/html/index.html

dist:  ## dist to pypi
	rm -rf dist build
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	twine check dist/* && twine upload dist/*

# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: clean build run test tests help annotate annotate_l docs dist

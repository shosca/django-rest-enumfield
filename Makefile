PACKAGE=rest_enumfield
FILES=$(shell find $(PACKAGE) -iname '*.py')
VERSION=$(shell python setup.py --version)
NEXT=$(shell semver -i $(BUMP) $(VERSION))
COVERAGE_FLAGS?=--cov-fail-under=100

.PHONY: $(FILES)

help:
	@for f in $(MAKEFILE_LIST) ; do \
		echo "$$f:" ; \
		grep -E '^[a-zA-Z_-%]+:.*?## .*$$' $$f | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' ; \
	done ; \

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build:  ## remove build artifacts
	find -name '*.sqlite3' -delete
	rm -rf build/ dist/ .eggs/
	rm -rf '*.egg-info'
	rm -rf '*.egg'

clean-pyc:  ## remove Python file artifacts
	find -name '*.pyc' -delete
	find -name '*.pyo' -delete
	find -name '*~' -delete
	find -name '__pycache__' -delete

clean-test:  ## remove test and coverage artifacts
	rm -rf .tox/ .coverage htmlcov/

lint:  ## run pre-commit hooks on all files
	-if python -c "import sys; exit(1) if (sys.version_info.major, sys.version_info.minor) < (3, 7) else exit(0)"; then \
		pre-commit run --all-files ; \
	fi

coverage: ## check code coverage quickly with the default Python
	py.test $(PYTEST_OPTS) \
		--cov-report html \
		--cov-report term-missing \
		--cov=$(PACKAGE) tests \
		$(COVERAGE_FLAGS) \
		--doctest-modules \
		tests $(PACKAGE)

$(FILES):  ## helper target to run coverage tests on a module
	py.test $(PYTEST_OPTS) \
		--cov-report term-missing \
		--cov-fail-under 100 \
		--cov=$(subst /,.,$(firstword $(subst ., ,$@))) $(subst $(PACKAGE),tests,$(dir $@))test_$(notdir $@)

test:  ## run tests
	py.test $(PYTEST_OPTS) --doctest-modules tests $(PACKAGE)

check:  ## run all tests
	tox

history: ## generate HISTORY.rst
	gitchangelog > HISTORY.rst

version:  # print version
	@echo $(VERSION)

next:  # print next version
	@echo $(NEXT)

bump: history
	@sed -i 's/$(VERSION)/$(NEXT)/g' $(PACKAGE)/__version__.py
	@sed -i 's/Next version (unreleased yet)/$(NEXT) ($(shell date +"%Y-%m-%d"))/g' HISTORY.rst
	@git commit -am "Bump version: $(VERSION) → $(NEXT)"

tag:  ## tags branch
	git tag -a $$(python setup.py --version) -m $$(python setup.py --version)

release: dist  ## package and upload a release
	twine upload dist/*

dist: clean  ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

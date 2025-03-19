SHELL := /bin/bash

.PHONY: init_dev_env setup_dev_env dcup clean install_maas_modules init_db_mapping run_test

init_dev_env:
	@export WORK_DIR=$$(pwd) && \
	source $$WORK_DIR/development/.env && \
	python$${PYTHON_VERSION} -m venv $${WORK_DIR}/omcs-venv-$${PYTHON_VERSION}-dev && \
	source $${WORK_DIR}/omcs-venv-$${
		PYTHON_VERSION}-dev/bin/activate
	@$(MAKE) pre_install_maas_modules
	@$(MAKE) install_maas_modules
	@$(MAKE) dcup
	@$(MAKE) init_db_mapping
	@$(MAKE) run_test


setup_dev_env:
	@export WORK_DIR=$$(pwd) && \
	source $$WORK_DIR/development/.env && \
	source $${WORK_DIR}/omcs-venv-$${PYTHON_VERSION}-dev/bin/activate

dcup:
	docker compose -f $${WORK_DIR}/development/docker-compose.yaml --env-file $${WORK_DIR}/development/.env up -d

pre_install_maas_modules:
	pip install --upgrade pip && \
	pip install -U setuptools setuptools_scm wheel && \
	pip install -U tox
	pip install pytest pytest-cov wheel

install_maas_modules:
	cd $$WORK_DIR/modules/maas-model/ && pip install -e . && \
    cd $$WORK_DIR/modules/maas-engine/ && pip install -e . && \
    cd $$WORK_DIR/modules/maas-cds/ && pip install -e . && \
    cd $$WORK_DIR/modules/maas-collector/ && pip install -e . && \
    cd $$WORK_DIR

# this require the maas-engine
init_db_mapping:
	maas_migrate -v --install all -r $$WORK_DIR/modules/maas-cds/resources

run_test:
	TZ=UTC pytest -ryv

clean:
	@rm -rf omcs-venv-*


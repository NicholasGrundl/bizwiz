#### Python Environment ####
.PHONY: install
install: 
	pip install -r ./requirements.txt
	pip install -r ./requirements-dev.txt

.PHONY: uninstall
uninstall:
	@bash -c "pip uninstall -y -r <(pip freeze)"

#### Build ####
VERSION=`grep version setup.cfg | awk '{print $$3}'`
TAGNAME=v$(VERSION)

.PHONY: publish.tag
publish.tag:
	@echo "---Tagging commit hash $(TAGNAME) "
	git tag -a $(TAGNAME) -m"Release $(TAGNAME)"
	git push origin $(TAGNAME)
	@echo "---Pushed tag as version=$(VERSION)"


#### Development ####
.PHONY: jupyter
jupyter: 
	@jupyter lab --autoreload --no-browser



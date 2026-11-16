.PHONY: install run test docker clean
install: ; pip install -r requirements.txt
run:     ; PYTHONPATH=src python -m fashmatch_poc.pipeline
test:    ; PYTHONPATH=src python -m unittest discover -s tests -v
docker:  ; docker build -t fashmatch-poc . && docker run --rm -v $$PWD/reports:/app/reports fashmatch-poc
clean:   ; rm -rf output vault reports/*.json

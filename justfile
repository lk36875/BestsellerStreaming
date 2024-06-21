set shell := ["cmd.exe", "/c"]

produce:
    poetry run python -m root -t books

test:
    poetry run pytest

format:
    poetry run black .
    poetry run isort .

upgrade:
    cd terraform && terraform init -upgrade

apply:
    cd terraform && terraform apply

destroy:
    cd terraform && terraform destroy
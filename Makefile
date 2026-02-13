.PHONY: run create-user install

# Start the FastAPI dev server
run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Create a new user — usage: make create-user email=user@example.com password=secret
create-user:
	python -m cmd.create_user --email $(email) --password $(password)

# Install dependencies
install:
	pip install -r requirements.txt

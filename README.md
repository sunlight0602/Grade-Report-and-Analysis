# Grade-Report-And-Analysis
This is the backend of the Grade-Report-And-Analysis project. \
This repo includes the backend APIs and the core library.

## Setup backend APIs

1. Create and activate virtual environment (using venv as example)
```
python3 -m venv venv
source ./venv/bin/activate
```

2. Install dependencies
```
pip3 install -r requirements.txt
pip3 install -r python_code_quality.txt
```

3. Run backend apis

## Developing

1. Create and activate virtual environment (using venv as example)
```
python3 -m venv venv
source ./venv/bin/activate
```

2. Install dependencies
```
pip3 install -r requirements.txt
pip3 install -r python_code_quality.txt
```

3. An example of the library
```
python3 driver.py
```
Student reports and teacher report will appear in ```output_files/```

4. Testing the library

```
pytest .
```

5. Run code quality tools

```
black .
isort .
flake8 .
```

```
cd GradeReportAndAnalysis/
mypy
pylint
```

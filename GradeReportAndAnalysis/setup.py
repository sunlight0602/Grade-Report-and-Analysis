from setuptools import find_packages, setup

setup(
    name="GradeReportAndAnalysis",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "GradeReportAndAnalysis": ["templates/*.html"],
    },
    # ... other setup parameters ...
)

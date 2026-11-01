#!/bin/sh
rm -rf allure-results
pytest -v
status=$?
allure generate allure-results -o allure-report --clean --single-file || exit 1
exit $status

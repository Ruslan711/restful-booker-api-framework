#!/bin/sh

mkdir -p allure-results allure-report

find allure-results -mindepth 1 -delete
find allure-report -mindepth 1 -delete

pytest -v
status=$?

if [ -d allure-results ] && [ "$(find allure-results -type f | wc -l)" -gt 0 ]; then
    allure generate allure-results -o allure-report --clean --single-file
    allure_status=$?
else
    echo "Allure results are empty. Report was not generated."
    allure_status=1
fi

if [ "$status" -ne 0 ]; then
    exit "$status"
fi

exit "$allure_status"
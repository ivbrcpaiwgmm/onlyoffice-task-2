# Варианты улучшения кода тестов:
# Вынести тестовые константы из locators в отдельный файл.
# Возможно, сделать тестовые методы внутри класса статическими.

import os
import csv
from random import randint

import pytest

import locators
from contacts_parser import make_contacts_csv


@pytest.fixture(scope="class", params=locators.TEST_DATA)
def csv_file_path(request):
    path = request.param
    make_contacts_csv(path)
    yield path
    if os.path.exists(path):
        os.remove(path)


class TestContactsParser:
    def test_file_creation(self, csv_file_path):
        assert os.path.exists(csv_file_path), f"The file {csv_file_path} doesn't exist."

    def test_file_extension(self, csv_file_path):
        file_extension = os.path.splitext(csv_file_path)[1]
        assert file_extension == ".csv", f"the file has extension {file_extension}, not .csv"

    def test_csv_format(self, csv_file_path):
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=locators.CSV_DELIMITER)

            for row in reader:
                # Проверяем записанные данные на соответствие требуемому формату CSV: "Country;CompanyName;FullAddress".
                assert len(row) == 3, f"Incorrect format. Invalid number of items in row: {row}. Required 3"

    @staticmethod
    def _check_sample_in_csv(file_path, sample):
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file, delimiter=locators.CSV_DELIMITER)
            for row in csv_reader:
                for field in row:
                    if sample in field:
                        return True
        return False

    def test_sample_in_csv(self, csv_file_path):
        sample = locators.DATA_SAMPLE_LIST[randint(0, len(locators.DATA_SAMPLE_LIST) - 1)]
        assert TestContactsParser._check_sample_in_csv(csv_file_path,
                                                       sample), f"Sample '{sample}' was not found in CSV file."

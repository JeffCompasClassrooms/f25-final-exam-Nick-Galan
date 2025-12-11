

import os
import pytest
from christmas_list import ChristmasList


def describe_christmas_list_system_tests():

    @pytest.fixture
    def cl(tmp_path):
        # Each test gets a brand-new pickle file
        list_file = tmp_path / "christmas_list.pkl"
        return ChristmasList(str(list_file))

    def it_starts_with_an_empty_list(cl):
        items = cl.loadItems()
        assert items == []

    def it_adds_items_and_persists_to_disk(tmp_path):
        list_file = tmp_path / "christmas_list.pkl"

        cl1 = ChristmasList(str(list_file))
        cl1.add("bb gun")
        cl1.add("socks")

        # New instance loads persisted state
        cl2 = ChristmasList(str(list_file))
        items = cl2.loadItems()
        names = [i["name"] for i in items]

        assert "bb gun" in names
        assert "socks" in names

    def it_checks_off_items(cl):
        cl.add("bb gun")
        cl.check_off("bb gun")

        items = cl.loadItems()
        item = next(i for i in items if i["name"] == "bb gun")
        assert item["purchased"] is True

    def it_removes_items(cl):
        cl.add("bb gun")
        cl.add("socks")

        cl.remove("bb gun")

        items = cl.loadItems()
        names = [i["name"] for i in items]

        assert "bb gun" not in names
        assert "socks" in names

    def it_ignores_check_off_for_missing_item(cl):
        cl.add("socks")
        cl.check_off("tv")  # does not exist

        items = cl.loadItems()
        item = next(i for i in items if i["name"] == "socks")
        assert item["purchased"] is False

    def it_prints_checked_off_item_correctly(cl, capsys):
        cl.add("bb gun")
        cl.check_off("bb gun")

        cl.print_list()

        captured = capsys.readouterr()
        assert captured.out == "[x] bb gun\n"

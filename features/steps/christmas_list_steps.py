from behave import given, when, then
from christmas_list import ChristmasList
import io
from contextlib import redirect_stdout




@when('I check off "{name}" and capture print output')
def step_check_off_and_capture(context, name):
    context.list.check_off(name)

    import io
    from contextlib import redirect_stdout

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        context.list.print_list()

    context.print_output = buffer.getvalue()

@given("I have a fresh christmas list file")
def step_fresh_file(context):
    context.list = ChristmasList(context.christmas_list_file)
    items = context.list.loadItems()
    assert items == []


@given("the christmas list already contains:")
def step_list_already_contains(context):
    context.list = ChristmasList(context.christmas_list_file)
    items = []
    for row in context.table:
        name = row["name"]
        purchased = row["purchased"].strip().lower() == "true"
        items.append({"name": name, "purchased": purchased})
    context.list.saveItems(items)


@when('I add "{name}" to the christmas list')
def step_add_item(context, name):
    context.list.add(name)


@when('I check off "{name}" on the christmas list')
def step_check_off_item(context, name):
    context.list.check_off(name)


@when('I remove "{name}" from the christmas list')
def step_remove_item(context, name):
    context.list.remove(name)


@when("I print the christmas list")
def step_print_list(context):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        context.list.print_list()
    context.printed_output = buffer.getvalue().strip()


@then('the list should contain an item "{name}" marked as "{status}"')
def step_then_list_contains_item_with_status(context, name, status):
    items = context.list.loadItems()
    matching = [i for i in items if i["name"] == name]
    assert matching, f"No item found with name {name!r}"

    purchased_expected = {
        "purchased": True,
        "not purchased": False
    }[status.strip().lower()]

    assert matching[0]["purchased"] == purchased_expected


@then('the list should not contain an item "{name}"')
def step_then_list_not_contains_item(context, name):
    items = context.list.loadItems()
    assert all(i["name"] != name for i in items)


@then("the printed output should be:")
def step_then_printed_output_equals(context):
    expected = context.text.strip()
    actual = context.printed_output.strip()
    assert actual == expected

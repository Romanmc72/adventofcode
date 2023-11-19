#!/usr/bin/env python3
"""
Part 1
------
Find the monkey business factor!

Part 2
------
And do it for 10,000 rounds without dividing...

"""
import re
from math import prod
from typing import Callable, Dict, List, Union

MONKEYS: Dict[int, "Monkey"] = dict()


class Item:
    def __init__(self, worry_level: int, relief_divisor: int = 3) -> None:
        self.worry_level = worry_level
        self.relief_divisor = relief_divisor

    def relief(self):
        """Divides the worry level and rounds down to the nearest 3"""
        self.worry_level //= self.relief_divisor


class Monkey:
    def __init__(
        self,
        number: int,
        on_true_number: int,
        on_false_number: int,
        divisor: int,
        operation: Callable[[Item], None],
        items: List[Item] = None,
    ) -> None:
        self.number = number
        self.on_true_number = on_true_number
        self.on_false_number = on_false_number
        self.divisor = divisor
        self.operation = operation
        self.items = items or []
        self.inspected_item_count = 0
        self.monkey_mod = 1

    def inspect(self, item: Item) -> None:
        self.operation(item)
        self.inspected_item_count += 1

    def complicated_division(self, item: Item) -> bool:
        stringified = str(item.worry_level)
        odd_sum = 0
        even_sum = 0
        for digit in enumerate(stringified):
            num = int(digit)
            if num % 2 == 0:
                even_sum += num
            else:
                odd_sum += num

    def test_worry_level(self, item: Item) -> None:
        item.relief()
        true_number = item.worry_level % self.divisor == 0
        if true_number:
            monkey = self.on_true_number
        else:
            monkey = self.on_false_number
        # Dude, fuck math
        item.worry_level = item.worry_level % self.monkey_mod
        self.pass_item(item=item, monkey=monkey)

    def pass_item(
        self, item: Item, monkey: int, monkey_lookup: Dict[int, "Monkey"] = MONKEYS
    ) -> None:
        monkey_lookup[monkey].receive_item(item=item)

    def receive_item(self, item: Item) -> None:
        self.items.append(item)

    def process_item(self, item: Item) -> None:
        self.inspect(item=item)
        self.test_worry_level(item=item)

    def process_all_items(self) -> None:
        while True:
            try:
                self.process_item(item=self.items.pop())
            except IndexError:
                break


def get_data():
    with open("input.txt", "r") as f:
        data = f.read()
    return [d.strip().lower() for d in data.split("\n")]


def get_number(line: str) -> int:
    return int(re.findall(r"\d+", line)[0])


def get_all_items(line: str, worry_level_divisor: int) -> List[Item]:
    return [
        Item(worry_level=int(number), relief_divisor=worry_level_divisor)
        for number in re.findall(r"\d+", line)
    ]


def make_number_maybe(part: str) -> Union[int, Item]:
    try:
        return int(part)
    except ValueError:
        return None


def add(item: Item, amount_1: int = None, amount_2: int = None) -> None:
    if amount_2:
        item.worry_level = amount_1 + amount_2
    elif amount_1:
        item.worry_level += amount_1
    elif not amount_1 and not amount_2:
        item.worry_level += item.worry_level
    else:
        raise ValueError("Again, what the fuck?")


def multiply(item: Item, amount_1: int = None, amount_2: int = None) -> None:
    if amount_2:
        item.worry_level = amount_1 * amount_2
    elif amount_1:
        item.worry_level *= amount_1
    elif not amount_1 and not amount_2:
        item.worry_level **= 2
    else:
        raise ValueError("Again, what the fuck?")


def parse_operation(line: str) -> Callable[[Item], None]:
    equation = line.split(": ")[1]
    components = equation.split(" ")
    if components[0] != "new" or len(components) < 5:
        raise ValueError(f"What the fuck is this shit? {line}")

    left_part = make_number_maybe(components[2])
    right_part = make_number_maybe(components[4])
    operator = components[3]
    if operator == "+":
        return lambda i: add(i, right_part, left_part)
    elif operator == "*":
        return lambda i: multiply(i, right_part, left_part)
    else:
        raise ValueError(f"Seriously, what the fuck? {operator}")


def make_monkeys(
    raw_data: List[str],
    monkey_list: Dict[int, Monkey] = MONKEYS,
    worry_level_divisor: int = 3,
) -> None:
    for line in raw_data:
        if line.startswith("monkey"):
            monkey_number = get_number(line=line)
        elif line.startswith("starting items"):
            items = get_all_items(line=line, worry_level_divisor=worry_level_divisor)
        elif line.startswith("operation"):
            operation = parse_operation(line=line)
        elif line.startswith("test"):
            divisor = get_number(line=line)
        elif line.startswith("if true:"):
            on_true_number = get_number(line=line)
        elif line.startswith("if false:"):
            on_false_number = get_number(line=line)
        else:
            monkey_list[monkey_number] = Monkey(
                number=monkey_number,
                on_true_number=on_true_number,
                on_false_number=on_false_number,
                divisor=divisor,
                operation=operation,
                items=items,
            )
    monkey_list[monkey_number] = Monkey(
        number=monkey_number,
        on_true_number=on_true_number,
        on_false_number=on_false_number,
        divisor=divisor,
        operation=operation,
        items=items,
    )


def main(rounds: int, worry_level_divisor: int):
    make_monkeys(
        raw_data=get_data(),
        monkey_list=MONKEYS,
        worry_level_divisor=worry_level_divisor,
    )
    monkey_mod = prod([monkey.divisor for monkey in MONKEYS.values()])
    for monkey in MONKEYS.values():
        monkey.monkey_mod = monkey_mod
    monkey_number_list = list(MONKEYS.keys())
    monkey_number_list.sort()
    for _ in range(rounds):
        for monkey_number in monkey_number_list:
            MONKEYS[monkey_number].process_all_items()
    all_monkey_business = [monkey.inspected_item_count for monkey in MONKEYS.values()]
    all_monkey_business.sort()
    top_2 = all_monkey_business[-2:]
    print(f"Looks like the monkey business is at {top_2[0] * top_2[1]}")


if __name__ == "__main__":
    # Holy crap this takes a long time to run!
    # 42845936760
    # 29018908520
    # 28537348205
    # 25233717914
    # 14405400476
    main(rounds=20, worry_level_divisor=3)
    main(rounds=10000, worry_level_divisor=1)

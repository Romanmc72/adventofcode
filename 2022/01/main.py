#!/usr/bin/env python3
"""
Part 1
------
Elves are picking up snacks, you gotta find the top snack carrying elf's
quantity.

Part 2
------
Make that the top 3 elves and the total for all 3's quantity.
"""


def main():
    with open("input.txt", "r") as f:
        data = f.read()

    lines = data.split("\n")

    totals = list()

    current_elf_total = 0
    for line in lines:
        if line == "":
            totals.append(current_elf_total)
            current_elf_total = 0
        else:
            current_elf_total += int(line)

    totals.sort(reverse=True)
    print(f"Part 1 : {totals[0]}")
    print(f"Part 2 : {sum(totals[0:3])}")


if __name__ == "__main__":
    main()

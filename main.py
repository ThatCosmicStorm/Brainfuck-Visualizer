"""*Provides real-time visualization of a running Brainfuck program.*
"""

import sys
from typing import List, Dict
from time import sleep
from readchar import readchar
from tabulate import tabulate

COMMANDS = {
    "+", "-",
    "<", ">",
    "[", "]",
    ".", ",",
}


def clear_screen():
    print("\033[2J\033[H", end="")


class Brainfuck:

    def __init__(self, code: str):
        self.code = code

        self.stack: List[int] = []
        self.bracemap: Dict[int, int] = {}
        self.start = 0

        self.array = {0: 0}
        self.dp = 0
        self.ip: int = 0

        self.output = False
        self.words: List[str] = []

        self.cells: List[str] = []
        self.values: List[str] = []

    def get_loop_positions(self):
        for pos, cmd in enumerate(self.code):
            match cmd:
                case "[":
                    self.stack.append(pos)
                case "]":
                    self.start = self.stack.pop()
                    self.bracemap[self.start] = pos
                    self.bracemap[pos] = self.start

    def match(self):
        match self.code[self.ip]:
            case "+":
                self.array[self.dp] = (self.array[self.dp] + 1) % 256
            case "-":
                self.array[self.dp] = (self.array[self.dp] - 1) % 256
            case ">":
                self.dp += 1
                self.array.setdefault(self.dp, 0)
            case "<":
                if self.dp > 0:
                    self.dp -= 1
                else:
                    sys.exit("Error: Pointer moved left of 0")
            case "[":
                if not self.array[self.dp]:
                    self.ip = self.bracemap[self.ip]
            case "]":
                if self.array[self.dp]:
                    self.ip = self.bracemap[self.ip]
            case ".":
                self.output = True
            case ",":
                self.array[self.dp] = ord(readchar())

        self.ip += 1

    def update_table(self):
        self.cells = [str(cell) for cell in self.array]
        self.values = [
            [str(num) for num in self.array.values()],
            [ascii(chr(char)) for char in self.array.values()]
        ]

        self.cells[self.dp] = f"[ {self.cells[self.dp]} ]"

        print(tabulate(self.values, headers=self.cells, tablefmt="grid"))

    def point_to_code(self):
        self.dummy_code: str = self.code[:]
        self.code_lines: List[str] = []

        while len(self.dummy_code) > 0:
            self.code_lines.append(self.dummy_code[:78])
            self.dummy_code = self.dummy_code[79:]

        print("\n" + "Code:" + "\n")
        for i, line in enumerate(self.code_lines):
            if self.ip < (i + 1) * 79:
                pointer = " " * (self.ip - i * 79)
                pointer = pointer[:-1]
                pointer += "\u2191"
                print(line)
                if i*79 <= self.ip <= (i+1)*79:
                    print(pointer)
            else:
                print(self.code_lines[i])

    def execute(self, delay: int | float = 1):
        self.get_loop_positions()

        while self.ip < len(self.code):
            clear_screen()
            self.update_table()
            self.point_to_code()

            if self.output:
                self.words.append(chr(self.array[self.dp]))
            self.output = False

            sleep(delay)
            self.match()

        print("\n" + "Output:" + "\n")

        for word in enumerate(self.words):
            sys.stdout.write(word[1])


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: '{sys.argv[0]}' filename")

    if len(sys.argv) > 2:
        delay = float(sys.argv[2])
    else:
        delay = 1

    try:
        with open(sys.argv[1], "r", encoding="utf8") as f:
            code = "".join(char for char in f.read() if char in COMMANDS)
            Brainfuck(code).execute(delay=delay)
    except FileNotFoundError:
        sys.exit(f"Error: File '{sys.argv[1]}' not found")


if __name__ == "__main__":
    main()

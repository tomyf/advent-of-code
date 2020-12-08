from typing import List, Tuple
from y2020.libs.read_file import read_file_list_str


class Console:
    def __init__(self, program: List[str]):
        self.program = program

    def execute(self):
        instruction_pointer = 0
        accumulator = 0
        seen_instructions = set()
        return self.handle_instruction(instruction_pointer, accumulator, seen_instructions)

    def execute_fix_infinite_loop(self) -> Tuple[int, str]:
        # Create copies of current console with jmp and nop inverted
        consoles = [Console(self.program)]
        for (index, instruction) in enumerate(self.program):
            if instruction.startswith("jmp "):
                new_program = self.program.copy()
                new_program[index] = new_program[index].replace("jmp", "nop")
                consoles.append(Console(new_program))
            if instruction.startswith("nop "):
                new_program = self.program.copy()
                new_program[index] = new_program[index].replace("nop", "jmp")
                consoles.append(Console(new_program))

        # Try to execute them all
        for console in consoles:
            result, status = console.execute()
            if status == "OK":
                return (result, status)

    def handle_instruction(self, instruction_pointer: int, accumulator: int, seen_instructions: set) -> Tuple[int, str]:
        # Prevent infinite loops
        if instruction_pointer in seen_instructions:
            return (accumulator, 'Infinite')

        # Handle instruction
        seen_instructions.add(instruction_pointer)
        if instruction_pointer >= len(self.program):
            # Check normal termination
            return (accumulator, 'OK')
        operand, argument = self.program[instruction_pointer].split(" ")

        # Check operand
        if operand == "nop":
            # NOOP: Do nothing, and go to the next instruction
            return self.handle_instruction(
                instruction_pointer=instruction_pointer + 1,
                accumulator=accumulator,
                seen_instructions=seen_instructions
            )
        if operand == "acc":
            # ACC: Update accumulator
            return self.handle_instruction(
                instruction_pointer=instruction_pointer + 1,
                accumulator=accumulator + int(argument),
                seen_instructions=seen_instructions
            )
        if operand == "jmp":
            # JMP: Update instruction pointer according to the argument
            return self.handle_instruction(
                instruction_pointer=instruction_pointer + int(argument),
                accumulator=accumulator,
                seen_instructions=seen_instructions
            )


def test():
    test_data = read_file_list_str("test.txt")
    console = Console(test_data)
    assert console.execute() == (5, 'Infinite')
    assert Console(read_file_list_str("test_finishing.txt")).execute() == (8, 'OK')
    assert Console(read_file_list_str("test.txt")).execute_fix_infinite_loop() == (8, 'OK')
    print("✅ Valid tests")


def real():
    real_data = read_file_list_str("data.txt")
    console = Console(real_data)
    part1 = console.execute()
    print(f"Part 1: {part1}")
    assert part1 == (1087, 'Infinite')
    part2 = console.execute_fix_infinite_loop()
    print(f"Part 2: {part2}")
    assert part2 == (780, 'OK')


test()
real()

# Brainfuck Visualizer

## Features

- Real-time memory cell visualization
- ASCII value display
- Instruction pointer tracking
- Configurable execution speed
- Program output in realtime

## Requirements

- Since this project uses a virtual environment, no additional system-wide installations are needed.
- To install the virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

- Run the visualizer from the command line with:

```bash
python main.py <filename> [delay]
```

### Parameters

- `filename`: Path to the Brainfuck source code file
- `delay` (optional): Delay between instructions in seconds (default: 1)

### Example

```bash
python main.py helloworld.b 0.5
```

<!---
OpenSUSI TR-1um MPW Project Datasheet

This file describes your design for review and documentation.

You can include images in this folder and reference them in the markdown.
Each image must be less than 512 KB, and the total must be under 1 MB.
-->

# Project Datasheet

## Project Name

<!-- e.g. Simple CPU / PLL / ADC / Sensor Interface -->
Describe your project name.

---

## Overview

Provide a short summary of your design.

- What does the circuit do?
- What problem does it solve?
- What is the main feature?

---

## How it works

Explain the internal architecture.

Examples:
- Block diagram description
- Signal flow
- Clocking scheme
- Key modules

You may include diagrams:

![Block Diagram](block_diagram.png)

---

## Interface

Describe the I/O interface.

- Input signals
- Output signals
- Clock / reset
- Voltage domain (if relevant)

Example:

| Signal | Direction | Description |
|--------|----------|------------|
| clk    | input    | system clock |
| rst_n  | input    | active-low reset |
| out    | output   | result signal |

---

## How to test

Explain how your design can be verified.

- Simulation method
- Expected behavior
- Test vectors

Example:

1. Apply reset
2. Provide clock
3. Observe output transitions

---

## Layout notes

(Optional but recommended)

- Floorplan concept
- Analog/digital separation
- Guard ring usage
- Matching considerations

---

## External hardware

List any required external components.

Examples:

- PMOD module
- LED display
- Oscillator
- ADC/DAC interface

If none:

> No external hardware required.

---

## Known limitations

(Optional)

- Performance limits
- Frequency constraints
- Accuracy limitations

---

## Author

- Name:
- Affiliation:
- GitHub:

---

## License

Specify your design license if different from repository license.
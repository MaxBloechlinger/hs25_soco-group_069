# Software Construction – Assignments Overview

This repository contains my **Software Construction (SoCo)** coursework, showcasing progressively more complex system design, abstraction, and implementation techniques in Python and Java.

**Final Grade: (5.5/6.0)**

The assignments are explicitly designed around the principles and patterns from  
**Dr. Greg Wilson – *Software Design by Example***  
https://third-bit.com/sdxpy/

---

## Assignment 1 – Smart House Management System
- Built a **custom object system using only dictionaries** (no Python classes), including inheritance and multiple inheritance.
- Implemented devices (Light, Thermostat, Camera) with shared and abstract behavior.
- Designed a **Smart House Manager** to aggregate, filter, and compute power usage across devices.
- Developed a **custom testing framework** with automatic test discovery, setup/teardown, filtering, and runtime measurement.

**Key concepts:** object systems, inheritance, abstraction, testing frameworks, introspection.

---

## Assignment 2 – LGL Interpreter
- Implemented an interpreter for a **Little German Language (LGL)** supporting:
  - Arithmetic, comparison, and boolean operations
  - Variables, environments, and scoping
  - Arrays and sets
  - Functional programming primitives (`map`, `reduce`, `filter`)
- Added **do–until loops** and structured control flow.
- Designed and implemented a **visual execution tracer** that records call trees and execution times.

**Key concepts:** interpreters, environments, functional programming, tracing, program analysis.

---

## Assignment 3 – ZVFS (Virtual File System)
- Implemented a **binary virtual file system** stored in a single `.zvfs` file.
- Full filesystem command set: `mkfs`, `addfs`, `lsfs`, `catfs`, `getfs`, `rmfs`, `gifs`, `dfrgfs`.
- Carefully designed **fixed-size binary headers and entries** with manual packing/unpacking.
- Ported the full implementation from **Python to Java**, ensuring binary compatibility.
- Used low-level I/O (`struct` in Python, `ByteBuffer` / `FileChannel` in Java).

**Key concepts:** binary formats, file systems, low-level I/O, cross-language parity.

---

## Technologies & Skills Demonstrated
- Python & Java
- Binary data handling and file I/O
- Custom runtimes and interpreters
- Testing infrastructure design
- Clean architecture under strict constraints
- Careful alignment with formal specifications and textbook-driven design

---

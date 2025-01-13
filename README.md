# png-explorer

A simple python program to read chunks from a png file

## Research

The first step was to understand the structure of a png file and how its data is organized. For this, I used the [PNG specification](https://en.wikipedia.org/wiki/PNG#File_format).

The result of the search was the following:

-   A PNG file always starts with a signature that identifies the image as PNG, which is always equal to the value `89 50 4E 47 0D 0A 1A 0A` (size: 8 bytes)

-   Each chunk contains 4 fields : `the data length` | `the chunk type` | `the chunk data` | `CRC`

    -   **Data Length**: A 4 bytes value representing the size of the chunk data
    -   **Type**: A 4 bytes value representing the type of the chunk (IHDR, IDAT...)
    -   **Data**: A variable size field that contains the bytes of the image
    -   **CRC**: A network-byte-order CRC-32 computed over the chunk type and chunk data

-   **Reflected CRC**: refers to a variation where the bits of the CRC value are reversed (reflected) before being used or transmitted.

-   **[Entropy](<https://en.wikipedia.org/wiki/Entropy_(information_theory)>)** measures the randomness of data. You can calculate it using Shannon's formula:
    $`H = - \sum_{i} p_i \log_2 p_i​`$

    Where $`p_i`$​ is the probability of each symbol in the data.

Visual representation of a png file structure:

<img src="png-file-structure.jpg" alt="png file strucutre" width="500"/>

## Installation

### Prerequisites

-   Python 3.x
-   Standard Python libraries: `os`, `sys`, `math`, `collections.Counter`

## Steps

Clone the repository and navigate to the project folder:

```bash
    git clone https://github.com/elmahdigaga/png-explorer.git
    cd png-explorer
```

## How to Use

Run the script and provide the path to a PNG file as a command-line argument

```bash
    python png-explorer.py path/to/png/image.png
```

or input it manually when prompted.

```bash
    python png-explorer.py
    Enter the png image path : path/to/png/image.png
```

## Example

When running the script on the image included in the repository (dice.png), we get the following result:

```csv
    type, size, CRC, CRC_ref, entropy
    IHDR, 13, 36f2836e, 1992380268, 1.48
    PLTE, 21, c3c09b52, 1255736259, 3.01
    IDAT, 8192, c5b2a906, 1620397475, 4.00
    IDAT, 8192, 306e68ac, 890664460, 4.00
    IDAT, 8192, f3415c88, 289047247, 4.00
    IDAT, 8192, 16165ea0, 91908200, 4.00
    IDAT, 8192, 55b5c5e4, 665038250, 4.00
    IDAT, 236, d6129400, 2705515, 3.98
    IEND, 0, ae426082, 1090929269, 0.00
```

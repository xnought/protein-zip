# pzip `.pz`

PDB file compression with no external dependencies.

Trying to compress a pdb file format down as low as possible. Currently can make `2x` smaller. See [`A.pdb`](./data/A.pdb) versus the zipped protein [`A.pz`](./data/A.pz).

Right now, just doing Huffman coding on a character level. Note that PDB's have very repetitive words like `ATOM` and the three letter coded residues as well as tons of spaces in between. Can likely treat these as characters in the future to get down to `10x` smaller.


## Terminal Usage

Follows the structure

```bash
python3 pzip.py <mode> <input_filename> <output_filename>
```

where mode can be **zip** (from .pdb to .pz) or **unzip** (from .pz to .pdb).

### Examples

**zip**

```bash
python3 pzip.py zip ./data/A.pdb ./data/A.pz
```

**unzip**

```bash
python3 pzip.py unzip ./data/A.pz ./data/A.pdb
```

## Python Usage

```py
from pzip import pzip, unpzip

# compresses A.pdb into A.pz
pzip("./data/A.pdb", "./data/A.pz")

# decompresses the A.pz back into A.pdb (renamed)
unpzip("./data/A.pz", "./data/A_decompressed.pdb")

# now A_decompressed.pdb and the original A.pdb are the same
```

## File Format

See [`A.pz`](./data/A.pz) or click/toggle the details to see an example

<details>
    <summary>
    toggle screenshot of A.pz from vscode
    </summary>
    <img width="1433" alt="Screenshot 2024-01-01 at 7 59 08 PM" src="https://github.com/xnought/protein-zip/assets/65095341/96f4b4cc-bef9-414c-b649-533817057fce">
</details>


These are fields are separated by new lines


1. Length of bits of the encoded bitstring (not of the padded bytes) {int}
2. The starting location of the body data bytes {int}
3. The huffman tree representation in chars {str}
4. The actual encoded data in bytes {bytes}

> [!NOTE]
> The fourth field, the actual data, is in chunks of bytes, but the encoding is probably less than a multiple of 8 since I encoded a bit string. So use the first field to offset the padded 0s to get the actual start. Example in the [code](./huff.py).

## Visual Tree

For example transforming files like [`A.pdb`](./data/A.pdb) into huffman trees for compression

Max Depth=`12`

```python
Node("2,167,121")
├── Leaf(' ', "887,763")
└── Node("1,279,358")
    ├── Node("523,681")
    │   ├── Node("255,963")
    │   │   ├── Leaf('1', "127,074")
    │   │   └── Node("128,889")
    │   │       ├── Leaf('6', "64,746")
    │   │       └── Node("64,143")
    │   │           ├── Leaf('C', "34,267")
    │   │           └── Leaf('T', "29,876")
    │   └── Node("267,718")
    │       ├── Leaf('.', "133,754")
    │       └── Node("133,964")
    │           ├── Leaf('5', "69,215")
    │           └── Leaf('A', "64,749")
    └── Node("755,677")
        ├── Node("312,572")
        │   ├── Node("146,541")
        │   │   ├── Leaf('4', "71,186")
        │   │   └── Node("75,355")
        │   │       ├── Leaf('O', "37,836")
        │   │       └── Node("37,519")
        │   │           ├── Node("17,619")
        │   │           │   ├── Leaf('G', "8,583")
        │   │           │   └── Leaf('S', "9,036")
        │   │           └── Node("19,900")
        │   │               ├── Leaf('E', "10,295")
        │   │               └── Node("9,605")
        │   │                   ├── Leaf('U', "4,521")
        │   │                   └── Node("5,084")
        │   │                       ├── Leaf('I', "2,907")
        │   │                       └── Node("2,177")
        │   │                           ├── Leaf('V', "1,462")
        │   │                           └── Leaf('Z', "715")
        │   └── Node("166,031")
        │       ├── Leaf('3', "76,945")
        │       └── Node("89,086")
        │           ├── Leaf('-', "38,823")
        │           └── Node("50,263")
        │               ├── Leaf('\n', "26,754")
        │               └── Node("23,509")
        │                   ├── Leaf('N', "11,958")
        │                   └── Node("11,551")
        │                       ├── Leaf('R', "6,146")
        │                       └── Leaf('Y', "5,405")
        └── Node("443,105")
            ├── Node("207,597")
            │   ├── Leaf('0', "111,676")
            │   └── Leaf('2', "95,921")
            └── Node("235,508")
                ├── Node("113,409")
                │   ├── Leaf('9', "57,091")
                │   └── Node("56,318")
                │       ├── Leaf('M', "27,120")
                │       └── Node("29,198")
                │           ├── Leaf('L', "14,156")
                │           └── Node("15,042")
                │               ├── Node("6,594")
                │               │   ├── Leaf('B', "3,201")
                │               │   └── Leaf('D', "3,393")
                │               └── Node("8,448")
                │                   ├── Leaf('H', "4,195")
                │                   └── Leaf('P', "4,253")
                └── Node("122,099")
                    ├── Leaf('7', "62,000")
                    └── Leaf('8', "60,099")

```

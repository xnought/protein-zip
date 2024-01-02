# protein-huffman

TODO

- [ ] Encode the text in binary using the tree
- [x] Somehow store the tree information in the file
- [ ] allow for other characters, like 'ATOM' that shows up alot, it can be represented with a smaller string

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

## File Format

- Length of characters of the original string
- The huffman tree representation
- The encoded bits. Note that it is written in chunks of bytes, so will need to adjust to get the exact number of bits 
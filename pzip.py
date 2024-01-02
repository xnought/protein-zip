#!/usr/local/bin/python3
from __future__ import annotations
from heapq import heapify, heappop, heappush
import math
import sys

NEW_LINE_ASCII = 10
TEST_MODE = False


# first I want to parse the string to read the unique characters in the file
def char_frequencies(string: str) -> dict[str, int]:
    freqs = {}
    for char in string:
        if char not in freqs:
            freqs[char] = 0
        else:
            freqs[char] += 1
    return freqs


class HuffNode:
    def __init__(self, freq: int, lchild: HuffNode = None, rchild: HuffNode = None):
        self.freq = freq
        self.lchild = lchild
        self.rchild = rchild

    @property
    def is_leaf(self):
        return self.__class__ is HuffLeaf

    def str(self):
        return f"({self.lchild.str()},{self.rchild.str()})"

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.__dict__.__str__() + ")"

    def __lt__(self, other):
        """needed for heapq priority comparison"""
        return self.freq <= other.freq


class HuffLeaf(HuffNode):
    def __init__(self, freq: int, char: str):
        super().__init__(freq)
        self.char = char

    def str(self):
        return f"'{self.char}'"


class HuffQueue:
    def __init__(self, freqs: dict[str, int]):
        self.priority_queue = []
        heapify(self.priority_queue)

        # add all the leaves (characters) first
        for c, f in freqs.items():
            self.push(HuffLeaf(freq=f, char=c))

    def pop(self) -> HuffNode:
        return heappop(self.priority_queue)

    def push(self, new_node: HuffNode):
        heappush(self.priority_queue, new_node)

    def peak(self) -> HuffNode:
        return self.priority_queue[0]

    def __len__(self) -> int:
        return len(self.priority_queue)

    def __repr__(self) -> str:
        return f"HuffQueue(len={len(self)}, top={self.peak()})"


def create_huffman_code(freqs: dict[str, int]) -> HuffNode:
    """Returns the root node of the tree"""

    q = HuffQueue(freqs)
    while len(q) > 1:
        # pop two smallest nodes, they are now the bottom of the tree
        child_a, child_b = q.pop(), q.pop()
        parent = HuffNode(
            freq=child_a.freq + child_b.freq, lchild=child_a, rchild=child_b
        )
        # push the nodes (almost think of merged) back into circulation
        q.push(parent)

    return q.pop()  # return the root


def outer_comma(string: str):
    """ "Returns None on failure and an int when found"""
    other = 0
    for i, char in enumerate(string):
        if other == 1 and char == ",":
            return i

        # if we encounter another paren, need to find its own matching pair
        if char == "(":
            other += 1
        elif char == ")":
            other -= 1

    return None


def parse_str_to_tree(string: str):
    # split a string at the upperlevel comma like "((a,b), c)" would split into "(a,b)" and "c"
    # i define the scope as anything inside the upper level parentheses
    # recursively do
    comma = outer_comma(string)
    a, b = string[:comma], string[comma + 1 :]
    b = b[:-1]
    a = a[1:]
    if a[0] != "'":
        a = parse_str_to_tree(a)
    else:
        a = a[1]
    if b[0] != "'":
        b = parse_str_to_tree(b)
    else:
        b = b[1]
    return a, b


def read_huffman_tree(tree_str: str) -> HuffNode:
    tuple_tree = parse_str_to_tree(tree_str)

    def construct(node):
        if isinstance(node, str):
            return HuffLeaf(freq=-1, char=node)
        return HuffNode(freq=-1, lchild=construct(node[0]), rchild=construct(node[1]))

    return construct(tuple_tree)


def shallow_split(string: str, split_on=NEW_LINE_ASCII):
    locs = []
    outer = 0
    for i in range(len(string)):
        char = string[i]
        if char == 40:
            outer += 1
        elif char == 41:
            outer -= 1

        if outer == 0 and char == split_on:
            locs.append(i)
    return locs


def leaves_to_encoding(code: HuffNode):
    # first find all the leaves
    # I can travel down, constructing a string, then when I hit, add that string to the global dict
    mapping = {}

    def trav(node: HuffNode, bits):
        if node.is_leaf:
            mapping[node.char] = bits
            return
        trav(node.lchild, bits + "0")
        trav(node.rchild, bits + "1")

    trav(code, "")
    return mapping


def encode_huff(code: HuffNode, original: str) -> str:
    # iterate over each character in the original, and convert it to bits form by
    # considering a right turn as 1 and a left turn as 0 in the tree and when I hit a leaf stop
    # a conceptually easier way to think about this is starting from each leaf, going up and keeping track of how many it takes to go up to the top
    # and encoding based on which side it was, then creating a map that we can easily translate
    res = ""
    mapping = leaves_to_encoding(code)
    for char in original:
        res += mapping[char]
    return res


def decode_huff(root: HuffNode, encoded: str) -> str:
    # iterate over the encoded bit string where left is 0 and right is 1
    # if I hit a leaf, then that is the character and restart
    cur_node = root
    result = ""
    for bit in encoded:
        if bit == "1":
            cur_node = cur_node.rchild
        elif bit == "0":
            cur_node = cur_node.lchild
        else:
            print("ERROR")

        if cur_node.is_leaf:
            result += cur_node.char  # this is the correct char
            cur_node = root  # go back to the root node

    return result


def bit_str_to_bytes(bits: str):
    n = len(bits)
    byte = bits[:n]
    return int(byte, base=2).to_bytes(math.ceil(n / 8))


def bytes_to_bit_str(b: bytes, offset):
    """commonly offset by bits length you think it should be"""
    result = ""
    for chunk in b:
        result += f"{chunk:08b}"
    return result[len(result) - offset :]


class Huff:
    @staticmethod
    def encode(string: str) -> tuple[str, HuffNode]:
        freqs = char_frequencies(string)
        huffman_code = create_huffman_code(freqs)
        encoded = encode_huff(huffman_code, string)
        return encoded, huffman_code

    @staticmethod
    def decode(code: HuffNode, encoded: str) -> str:
        decoded = decode_huff(code, encoded)
        return decoded


def simple_test():
    test = """
    MODEL     1                                                                     
    ATOM      1  N   ASN A   1     -65.537  -3.389  11.278  1.00 44.93           N  
    ATOM      2  CA  ASN A   1     -64.535  -2.678  12.067  1.00 44.93           C  
    ATOM      3  C   ASN A   1     -63.123  -3.155  11.739  1.00 44.93           C  
    ATOM      4  CB  ASN A   1     -64.817  -2.839  13.562  1.00 44.93           C  
    ATOM      5  O   ASN A   1     -62.727  -4.253  12.133  1.00 44.93           O  
    ATOM      6  CG  ASN A   1     -65.657  -1.708  14.123  1.00 44.93           C  
    ATOM      7  ND2 ASN A   1     -66.129  -1.873  15.353  1.00 44.93           N  
    ATOM      8  OD1 ASN A   1     -65.882  -0.695  13.455  1.00 44.93           O  
    ATOM      9  N   CYS A   2     -62.653  -3.062  10.488  1.00 47.37           N  
    ATOM     10  CA  CYS A   2     -61.344  -3.432   9.960  1.00 47.37           C  
    ATOM     11  C   CYS A   2     -60.251  -2.544  10.541  1.00 47.37           C  
    ATOM     12  CB  CYS A   2     -61.335  -3.335   8.435  1.00 47.37           C  
    ATOM     13  O   CYS A   2     -60.208  -1.343  10.266  1.00 47.37           O  
    ATOM     14  SG  CYS A   2     -61.839  -4.859   7.606  1.00 47.37           S  
    ENDMDL                                                                          
    END                                                                             
    """
    encoded, tree = Huff.encode(test)
    recon = Huff.decode(tree, encoded)
    assert recon == test, "String decoded must be the same as original"


def real_test():
    pzip("./data/A.pdb", "./null/A.pz")
    unpzip("./null/A.pz", "./null/A.pdb")

    # then compare A.pdb to see if same
    og_str = None
    new_file = None
    with open("./data/A.pdb", "r") as og_file:
        og_str = og_file.read()
    with open("./null/A.pdb", "r") as new_file:
        new_str = new_file.read()

    assert new_str == og_str


def pzip(in_filename: str, out_filename: str):
    # read in the string to be compressed/encoded
    in_str = None
    with open(in_filename, "r") as in_file:
        in_str = in_file.read()

    # encode the data into bits with huffman coding
    encoded, tree = Huff.encode(in_str)

    # then I want to write the file
    with open(out_filename, "wb") as out_file:
        encoded_bytes = bit_str_to_bytes(encoded)

        HEADER_bit_str_len = f"{len(encoded)}\n".encode()
        HEADER_huffman_tree = f"{tree.str()}\n".encode()
        HEADER_data_start = (
            f"{len(HEADER_bit_str_len) + len(HEADER_huffman_tree)}\n".encode()
        )
        # HEADER
        out_file.write(HEADER_bit_str_len)
        out_file.write(HEADER_data_start)
        out_file.write(HEADER_huffman_tree)
        # BODY
        out_file.write(encoded_bytes)


def parse_header(binary: bytes) -> tuple[int, int, HuffNode]:
    # index of first and second new line characters
    first_nl = binary.index(NEW_LINE_ASCII)
    second_nl = binary[first_nl + 1 :].index(NEW_LINE_ASCII) + first_nl

    # anything up to first new line is the len
    unpadded_bit_str_len = int(binary[:first_nl].decode())
    # anything up to the second new line is the start location of the data - len(that number)
    start_data = int(binary[first_nl + 1 : second_nl + 1].decode())
    start_data += len(str(start_data))
    start_data += 1  # skip new line after tree

    # inbetween the second new line and the start of the data is the tree
    tree_str = binary[second_nl + 2 : start_data - 1].decode()
    parsed_tree = read_huffman_tree(tree_str)

    return (unpadded_bit_str_len, start_data, parsed_tree)


def unpzip(in_filename: str, out_filename: str):
    binary = None
    with open(in_filename, "rb") as in_file:
        binary = in_file.read()

    unpadded_bit_str_len, data_start, tree = parse_header(binary)
    body_bytes = binary[data_start:]
    body_bit_str = bytes_to_bit_str(body_bytes, offset=unpadded_bit_str_len)
    decoded = Huff.decode(tree, body_bit_str)

    with open(out_filename, "w") as out_file:
        out_file.write(decoded)


if __name__ == "__main__":
    if TEST_MODE:
        simple_test()
        real_test()
    else:
        # command line mode
        # example: python3 pzip.py
        args = sys.argv[1:]
        num_args = len(args)
        if num_args == 0 or num_args == 1 or num_args == 2:
            raise Exception(
                f"{num_args} is not enough arguments need 3\nExample: python3 pzip.py zip file1 file2 or python3 pzip.py unzip file1 file2"
            )
        elif num_args == 3:
            [mode, in_filename, out_filename] = args
            if mode != "zip" and mode != "unzip":
                raise Exception("Must be zip or unzip for mode")
            if mode == "zip":
                pzip(in_filename, out_filename)
            elif mode == "unzip":
                unpzip(in_filename, out_filename)
            else:
                raise Exception("impossible to get here")

        else:
            raise Exception("too many arguments")

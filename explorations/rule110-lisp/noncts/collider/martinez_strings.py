"""Glider strings in phase f1_1 from Martinez, McIntosh, Seck-Tuoh,
Chapa-Vergara, "Determining a regular language by glider-based structures
called phases fi_1 in Rule 110", J. Cellular Automata 3 (2008),
arXiv:0706.3348, Appendix A. A configuration is ether* + string + ether*
with ether = 11111000100110. Used only to attach literature names to our
own (independently verified) glider records."""

STRINGS = {
    "A": "111110",
    "B": "11111010",
    "Bbar": "1111100010110111100110",
    "Bhat": "111110001011011110011001111111000100110",
    "C1": "111110000",
    "C2": "11111000000100110",
    "C3": "11111011010",
    "D1": "11111000010",
    "D2": "1111101011000100110",
    "E": "1111100000000100110",
    "Ebar": "111110000100011111010",
    "F": "111110001011010",
    "G": "111110100111110011100110",
    "H": "11111000101100000000111110001001101001111111000100110",
    "gun": "11111010110011101001100101111100000100110",
}
EXPECTED = {"A": (3, 2), "B": (4, -2), "Bbar": (12, -6), "Bhat": (12, -6),
            "C1": (7, 0), "C2": (7, 0), "C3": (7, 0), "D1": (10, 2),
            "D2": (10, 2), "E": (15, -4), "Ebar": (30, -8), "F": (36, -4),
            "G": (42, -14), "H": (92, -18), "gun": (77, -20)}

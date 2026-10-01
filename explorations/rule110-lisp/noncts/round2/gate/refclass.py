"""Assembler rule v2: designate a packet's class relative to the REFERENCE
E^k of its slot, where k - 1 = 6^-1 * (predecessors' slip) mod 7 is the
counter value mod 7 that slip conservation forces in a garbage-free stream
(reference events: INC-only chain from E at (0,0), collider ecounter).
For Z at value-1 slots, find which class makes its trailing GB4 meet the
zero E without displacing it: test words I^a N^b Z Z (glider level)."""
import sys
from common import LIB, CHAIN
from ecounter import chain_events

ev = chain_events()
print({k: ev[k] for k in range(1, 8)})

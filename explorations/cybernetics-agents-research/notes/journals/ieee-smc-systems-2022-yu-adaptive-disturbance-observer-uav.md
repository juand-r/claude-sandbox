# Composite Adaptive Disturbance Observer-Based Decentralized Fractional-Order Fault-Tolerant Control of Networked UAVs

**Authors:** Ziquan Yu, Youmin Zhang (Concordia University), Bin Jiang, Jun Fu, Y. Jin, T.Y. Chai
**Journal:** IEEE Transactions on Systems, Man, and Cybernetics: Systems, vol. 52, no. 2, pp. 799-813, 2022
**DOI:** 10.1109/TSMC.2020.3010678

## Summary

Decentralized fault-tolerant control for networked UAVs using:

### Technical approach
- **Composite adaptive disturbance observer**: estimates both external disturbances (wind) and internal faults (actuator degradation) simultaneously
- **Fractional-order control**: uses fractional calculus (non-integer order derivatives) for more flexible controller design -- provides additional tuning parameters and can better model certain physical phenomena
- **Decentralized architecture**: each UAV runs its own controller using only local and neighbor information
- **Directed communication network**: handles asymmetric information flow (agent A can hear B, but not vice versa)

### Problem addressed
- Wind disturbances affecting UAV flight
- Actuator faults (partial loss of effectiveness)
- Limited communication topology (directed graph)
- Need for cooperative behavior (formation, coordination)

## Relevance to Our Research

This is a concrete application paper showing cybernetic principles in action:
- **Disturbance observer** = Wiener's feedback principle applied to unknown perturbations
- **Decentralized control** = Beer's VSM autonomy -- each UAV is a viable system managing itself
- **Fractional-order** = an interesting extension of classical control theory, providing "memory" in the controller (fractional derivatives depend on past states -- a form of temporal context)
- **Fault tolerance** = homeostatic regulation maintaining function despite component degradation

The UAV swarm application is one of the most tangible use cases for cybernetics-inspired multi-agent architectures.

## Access

Full text NOT freely available. Behind IEEE paywall.

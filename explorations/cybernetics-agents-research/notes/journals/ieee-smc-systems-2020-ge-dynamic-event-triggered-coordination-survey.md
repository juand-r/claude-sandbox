# Dynamic Event-Triggered Distributed Coordination Control and Its Applications: A Survey of Trends and Techniques

**Authors:** Xiaohua Ge, Qing-Long Han, Lei Ding, Yu-Long Wang, Xian-Ming Zhang (Swinburne University of Technology; Nanjing University of Posts and Telecommunications; Shanghai University)
**Journal:** IEEE Transactions on Systems, Man, and Cybernetics: Systems, vol. 50, no. 9, pp. 3112-3125, September 2020
**DOI:** 10.1109/TSMC.2020.3010825

## Summary

Survey of dynamic event-triggered distributed coordination control for networked multi-agent systems.

### Key distinction: Static vs. Dynamic event-triggering
- **Static**: fixed triggering condition based on current state/error
- **Dynamic**: triggering mechanism adapts over time using system information AND additional dynamic variables (internal states of the trigger itself)

This is significant because dynamic event-triggering can further reduce communication while maintaining performance guarantees.

### Core problem
Coordinating a large group of distributed agents under constrained communication resources. Event-triggered scheduling balances control performance vs. resource efficiency.

### Applications demonstrated
- Microgrids (distributed energy management)
- Automated vehicles (cooperative driving)

### Research directions identified
- Co-design of event-triggered control and communication
- Event-triggered coordination under cyber attacks
- Heterogeneous multi-agent scenarios

## Relevance to Our Research

This is fundamentally a cybernetic problem: how do agents coordinate with minimal information exchange? The "dynamic event-triggering" concept is interesting from a cybernetics perspective because the trigger itself becomes a feedback system -- a meta-level control loop that regulates the primary control loop's communication.

This is reminiscent of Beer's VSM recursion: a system that manages the communication channels of the system below it. The trigger acts as a kind of System 3* (monitoring function) deciding when information needs to flow.

## Access

Full text NOT freely available. Behind IEEE paywall.

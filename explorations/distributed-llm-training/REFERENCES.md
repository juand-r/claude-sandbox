# References

## Weight Prediction in Pipeline Parallelism

- Chen et al. 2018. **SpecTrain: Efficient and Robust Parallel DNN Training through Model Parallelism on Multi-GPU Platform.** [arXiv:1809.02839](https://arxiv.org/abs/1809.02839)
- Yang et al. 2019/2021. **PipeMare: Asynchronous Pipeline Parallel DNN Training.** MLSys 2021. [arXiv:1910.05124](https://arxiv.org/abs/1910.05124)
- Guan et al. 2023/2025. **PipeOptim: Ensuring Effective 1F1B Schedule with Optimizer-Dependent Weight Prediction.** IEEE TKDE 2025. [arXiv:2312.00839](https://arxiv.org/abs/2312.00839)
- McEntire 2025. **Leap+Verify: Regime-Adaptive Speculative Weight Prediction for Accelerating Neural Network Training.** [arXiv:2602.19580](https://arxiv.org/abs/2602.19580)
- Kosson et al. 2020. **Pipelined Backpropagation at Scale: Training Large Models without Batches.** [arXiv:2003.11666](https://arxiv.org/abs/2003.11666)

## Decoupled / Local Learning

- Jaderberg et al. 2017. **Decoupled Neural Interfaces using Synthetic Gradients.** ICML. [arXiv:1608.05343](https://arxiv.org/abs/1608.05343)
- Czarnecki et al. 2017. **Understanding Synthetic Gradients and Decoupled Neural Interfaces.** ICML. [arXiv:1703.00522](https://arxiv.org/abs/1703.00522)
- Huo et al. 2018a. **Decoupled Parallel Backpropagation with Convergence Guarantee.** ICML. [PMLR v80](http://proceedings.mlr.press/v80/huo18a.html)
- Huo et al. 2018b. **Training Neural Networks Using Features Replay.** NeurIPS. [arXiv:1807.04511](https://arxiv.org/abs/1807.04511)
- Belilovsky et al. 2019. **Greedy Layerwise Learning Can Scale to ImageNet.** ICML. [arXiv:1812.11446](https://arxiv.org/abs/1812.11446)
- Nokland & Eidnes 2019. **Training Neural Networks with Local Error Signals.** ICML. [arXiv:1901.06656](https://arxiv.org/abs/1901.06656)
- Belilovsky et al. 2020. **Decoupled Greedy Learning of CNNs.** ICML. [PMLR v119](https://proceedings.mlr.press/v119/belilovsky20a.html)
- Laskin et al. 2020. **Parallel Training of Deep Networks with Local Updates.** [arXiv:2012.03837](https://arxiv.org/abs/2012.03837)
- Belilovsky et al. 2021. **Decoupled Greedy Learning of CNNs for Synchronous and Asynchronous Distributed Learning.** [arXiv:2106.06401](https://arxiv.org/abs/2106.06401)
- Cheng et al. 2023. **Unlocking Deep Learning: A BP-Free Approach for Parallel Block-Wise Training of Neural Networks.** [arXiv:2312.13311](https://arxiv.org/abs/2312.13311)

## Pipeline Parallelism & Bubble Reduction

- Harlap et al. 2019. **PipeDream: Fast and Efficient Pipeline Parallel DNN Training.** SOSP. [arXiv:1806.03377](https://arxiv.org/abs/1806.03377)
- Qi et al. 2024. **Zero Bubble Pipeline Parallelism.** ICLR. [arXiv:2401.10241](https://arxiv.org/abs/2401.10241)
- PipeFisher. MLSys 2023. **Efficient Training of Large Language Models Using Pipelining and Fisher Information.** [Paper](https://proceedings.mlsys.org/paper_files/paper/2023/file/dd064459e9ef4100671ba326f0f96f2b-Paper-mlsys2023.pdf)

## Staleness & Delayed Gradients

- Xu et al. 2020. **On the Acceleration of Deep Learning Model Parallelism with Staleness.** CVPR. [arXiv:1909.02625](https://arxiv.org/abs/1909.02625)
- Unnikrishnan & Parhi 2021. **LayerPipe: Accelerating Deep Neural Network Training by Intra-Layer and Inter-Layer Gradient Pipelining.** [arXiv:2108.06629](https://arxiv.org/abs/2108.06629)
- Unnikrishnan & Parhi 2025. **LayerPipe2: Multistage Pipelining and Weight Recompute via Improved Exponential Moving Average.** [arXiv:2512.08160](https://arxiv.org/abs/2512.08160)

## Greedy Layerwise / Self-Supervised Local

- Bengio et al. 2007. **Greedy Layer-Wise Training of Deep Networks.** NeurIPS 2006. [Proceedings](https://proceedings.neurips.cc/paper/2006/hash/5da713a690c067105aeb2fae32403405-Abstract.html)
- Lowe et al. 2019. **Greedy InfoMax for Biologically Plausible Self-Supervised Representation Learning.** NeurIPS. [Semantic Scholar](https://www.semanticscholar.org/paper/Greedy-InfoMax-for-Biologically-Plausible-Learning-L%C3%B6we-O%27Connor/637471d1fd7522e5f1c1066dc3aab26780bf6c83)
- Xiong et al. 2020. **LoCo: Local Contrastive Representation Learning.** NeurIPS. [arXiv:2008.01342](https://arxiv.org/abs/2008.01342)

# eBPFAngel Reference

## Original Project

**eBPFAngel — Ransomware Detection using Machine Learning with eBPF for Linux**

Authors: Max Willers and Tomás Philippart

Repository: https://github.com/TomasPhilippart/ebpfangel

## Use in This Project

The first experimental stage of this project used the dataset associated with the eBPFAngel research project as an existing dataset for experimentation.

The project also follows a related behavioral feature representation based on system-call/event patterns and n-gram-style triplet features.

The machine-learning models used in this project were trained and evaluated as part of this project.

The second experimental stage was conducted using a separately collected dataset generated from controlled ZeroLocker and benign executions.

## Attribution

eBPFAngel is an independent research project by Max Willers and Tomás Philippart. The original eBPFAngel repository is released under the MIT License.

This repository does not redistribute the original eBPFAngel dataset. Users interested in the original dataset and implementation should obtain them from the original repository and review its current licensing and usage information.

## Related Work

The eBPFAngel project provided an important reference point for the use of eBPF-based behavioral monitoring and machine learning in Linux ransomware detection.
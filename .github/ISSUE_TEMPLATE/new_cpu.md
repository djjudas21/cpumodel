---
name: Add CPU
about: Add a new CPU or fix wrong CPU data
title: ''
labels: bug
assignees: ''

---

### Provide your CPU data

Please provide the output of the following command for your CPU

```sh
grep 'model name' /proc/cpuinfo | sort -u
```

### Describe desired output

Please describe what output you expect from this library:

* `cpuVendor`:
* `cpuString`:
* `cpuModel`:
* `cpuFamily`:
* `cpuGeneration`:
* `cpuLetter`:
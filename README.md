# cpumodel

A Python library to parse and return various attributes from the CPU string

It has only been tested on relatively modern AMD and Intel CPUs that are likely to still be in use,
i.e. AMD Ryzen, AMD EPYC, Intel i-series, Intel Xeon E3/E5 and newer. Other CPUs may or may not produce
useful output.

If you want to request support for an unsupported CPU or if you see a bug in the output, see the
Contributing section.

## Installation

```terminal
pip install cpumodel
```

## Usage

### As a library

```py
from cpumodel.cpumodel import get_cpu_model

info = get_cpu_model()
```

### As a script

```terminal
$ cpumodel
{'cpuVendor': 'AMD', 'cpuString': 'AMD Ryzen 7 5700G', 'cpuModel': 'Ryzen 7 5700G', 'cpuFamily': 'Ryzen 7', 'cpuGeneration': '5', 'cpuLetter': 'G'}
```

You can optionally supply a CPU string with `-t` or `--test` which will cause cpumodel to parse this CPU
string rather than get the local system's CPU string. This is useful for testing the logic.

```terminal
$ cpumodel -t "Intel(R) Xeon(R) Gold 6234 CPU @ 3.30GHz"
{'cpuVendor': 'Intel', 'cpuString': 'Intel Xeon Gold 6234', 'cpuModel': 'Xeon Gold 6234', 'cpuFamily': 'Xeon Gold', 'cpuGeneration': '6'}
```

## Output

This library returns up to 6 values (it is possible for values to be `None`)

* `cpuVendor`, the CPU vendor, e.g. `Intel`
* `cpuString`, the full model string of the CPU, e.g. `Intel Core i7-6700S`
* `cpuModel`, the shorter model name of the CPU, e.g. `Core i7-6700S`
* `cpuFamily`, the concise family name of the CPU, e.g. `Core i7`
* `cpuGeneration`, the numeric generation of the CPU, e.g. `6`
* `cpuLetter`, any trailing letter codes for this CPU, e.g. `S`

## Examples

The best explanation of the data returned is probably by giving various examples.

| `cpuVendor` | `cpuString`                    | `cpuModel`                 | `cpuFamily`          | `cpuGeneration` | `cpuLetter` |
|-------------|--------------------------------|----------------------------|----------------------|-----------------|-------------|
| `Intel`     | `Intel Xeon Platinum 8358`     | `Xeon Platinum 8358`       | `Xeon Platinum`      | `8`             |             |
| `Intel`     | `Intel Xeon Gold 6226R`        | `Xeon Gold 6226R`          | `Xeon Gold`          | `6`             | `R`         |
| `Intel`     | `Intel Xeon E3-1220 v6`        | `Xeon E3-1220 v6`          | `Xeon E3`            | `6`             |             |
| `Intel`     | `Intel Celeron G1610`          | `Celeron G1610`            | `Celeron`            | `1`             | `G`         |
| `Intel`     | `Intel Core i5-6500T`          | `Core i5-6500T`            | `Core i5`            | `6`             | `T`         |
| `Intel`     | `Intel Core i9-9900K`          | `Core i9-9900K`            | `Core i9`            | `9`             | `K`         |
| `Intel`     | `Intel Core i9-10900`          | `Core i9-10900`            | `Core i9`            | `10`            |             |
| `Intel`     | `12th Gen Intel Core i7-1265U` | `Core i7-1265U`            | `Core i7`            | `12`            | `U`         |
| `Intel`     | `12th Gen Intel Core i9-12900` | `Core i9-12900`            | `Core i9`            | `12`            |             |
| `AMD`       | `AMD Ryzen 7 5700G`            | `Ryzen 7 5700G`            | `Ryzen 7`            | `5`             | `G`         |
| `AMD`       | `AMD Ryzen 7 PRO 5850U`        | `Ryzen 7 PRO 5850U`        | `Ryzen 7 PRO`        | `5`             | `U`         |
| `AMD`       | `AMD Ryzen 9 7950X`            | `Ryzen 9 7950X`            | `Ryzen 9`            | `7`             | `X`         |
| `AMD`       | `AMD Ryzen Threadripper 3990X` | `Ryzen Threadripper 3990X` | `Ryzen Threadripper` | `3`             | `X`         |
| `AMD`       | `AMD Athlon 5350 APU`          | `Athlon 5350 APU`          | `Athlon`             | `5`             |             |
| `AMD`       | `AMD Opteron 6366 HE`          | `Opteron 6366 H`           | `Opteron`            | `6366`          | `H`         |
| `AMD`       | `AMD EPYC 7551P`               | `EPYC 7551P`               | `EPYC`               | `7`             | `P`         |

## Contribution

If this library doesn't work properly on your CPU, it's probably because I've never tested on a CPU of that type.

Please [open an issue](https://github.com/djjudas21/cpumodel/issues), and describe what you would expect the
output of this module to be, and include the output of this command:

```sh
grep 'model name' /proc/cpuinfo | sort -u
```

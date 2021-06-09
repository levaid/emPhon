# emPhon
Phonetic transcriber for the xtsv framework.

## Requirements
- Python >= 3.6
- make

## Installation
- Clone the repository: `git clone https://github.com/levaid/emPhon`
- `make build`
- `pip install dist/*.whl`

## Usage
- Same as any other module using the xtsv framework - either as part of the emtsv framework or as separate module

### Configurations

The module takes command line arguments. By default, the module produces IPA output in strict xtsv format.

Command line arguments:

- `--no-ipaize` turns off IPA-ization, it produces the inner representation which uses exactly one unicode character for each phoneme
- `--lax_xtsv` groups the surface form of the entire sentence into the first token, thus it can take into account the rules on word boundaries, while strict mode cannot.
- `--opt_palatal_assim` turns on optional palatal assimilation for the t/d+ny clusters, e.g. lapátnyél -> lapátynyél

## Paper

Can be downloaded from [here](https://hlt.bme.hu/media/pdf/emphon_levai.pdf). Please cite the following paper when you use this module:

```bibtex
@InProceedings{   Kulcsar:2021,
  author        = {Virág Kulcsár and Dániel Lévai},
  title         = {em{P}hon: Morphologically sensitive open-source phonetic transcriber},
  booktitle     = {{XVII}. Conference on Hungarian Computational Linguistics  ({MSZNY}2021)},
  year          = 2021,
  address       = {Szeged}
}
```

## Miscellaneous

If different IPA (or transcription) is needed, the `emphon/ipa_key.json` file contains the key, which is human-modifiable.

## License
This xtsv wrapper is licensed under the LGPL 3.0 license. The model and the included .pt files have their own licenses




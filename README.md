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
- Same as any other module using the xtsv framework - either as part of the emtsv framework or as separate module.
- The module needs `form` and `anas` fields and produces the `phon` field and by default, it prepends the phonetic form of the entire sentence

### Configurations

The module takes command line arguments. By default, the module produces IPA output in strict xtsv format.

Command line arguments:

- `--ipaize` or `--no-ipaize` toggles IPA-ization, it produces the inner representation which uses exactly one unicode character for each phoneme. Default: on.
- `--opt-palatal-assim` or `--no-opt-palatal-assim` toggles optional palatal assimilation for the t/d+ny clusters, e.g. lapátnyél -> lapátynyél. Default: off.
- `--include-sentence` or `--no-include-sentence` toggles the inclusion of the entire phonetic form as a comment before each sentence. Default: on.

### Example output

```
# phon = ɒ mɛɡoldaːʒbɒ ɒkaːr moʃt meːɡ nɛm iʃ ɛŋɡɛdeːjɛzɛtː oltaːʃok iʃ bɛjaːt͡shɒtnɒk .
A       ɒ
megoldásba      mɛɡoldaːʒbɒ
akár    ɒkaːr
most    moʃt
még     meːɡ
nem     nɛm
is      iʃ
engedélyezett   ɛŋɡɛdeːjɛzɛtː
oltások oltaːʃok
is      iʃ
bejátszhatnak   bɛjaːt͡shɒtnɒk
.       .
```
## Paper

Can be downloaded from [here](https://hlt.bme.hu/media/pdf/emphon_levai.pdf). Please cite the following paper using this module:

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

This module is licensed under the LGPL 3.0 license.




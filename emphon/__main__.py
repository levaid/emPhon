#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from xtsv import build_pipeline, parser_skeleton, jnius_config, add_bool_arg


def main():

    argparser = parser_skeleton(description='EmPhon - a phonetic transcriber module for xtsv')

    add_bool_arg(argparser, 'ipaize',
                 ('Whether the output should be IPA or the inner representation, '
                  'which marks one phoneme with exactly one letter.'),
                 default=True, has_negative_variant=True)

    add_bool_arg(
        argparser, 'opt-palatal-assim',
        ('Whether optional palatal assimilation should happen with t/d+ny, e.g. lapátnyél -> lapátynyél'),
        default=False, has_negative_variant=True)

    add_bool_arg(
        argparser, 'include-sentence',
        'If on, there is a line of comment before the sentence that contains the entire surface form of the sentence.',
        default=True, has_negative_variant=True)

    opts = argparser.parse_args()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.

    # Set input and output iterators...
    if opts.input_text is not None:
        input_data = opts.input_text
    else:
        input_data = opts.input_stream
    output_iterator = opts.output_stream

    # Set the tagger name as in the tools dictionary
    used_tools = ['emphon']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    # from emphon import EmPhon
    # Produces IPA output with the surface form of the entire sentence in the first token.
    # This can take into account the rules over the word boundaries.
    # emphon_ipa_lax = ('emphon', 'EmPhon', 'EmPhon with ipaization and lax format', (),
    #                   {'source_fields': {'form', 'anas'},
    #                    'target_fields': ['phon'],
    #                    'strict_xtsv_format': False,
    #                    'transcriber_opts': {'ipaize': True, 'optional_palatal_assimilation': False},
    #                    },
    #                   )

    # Produces IPA output with one surface form per line. Does not work over word boundaries.
    # emphon_ipa_strict = ('emphon', 'EmPhon', 'EmPhon with ipaization and strict format', (),
    #                      {'source_fields': {'form', 'anas'},
    #                       'target_fields': ['phon'],
    #                       'strict_xtsv_format': True,
    #                       'transcriber_opts': {'ipaize': True, 'optional_palatal_assimilation': False},
    #                       },
    #                      )

    # Produces inner representation (one phoneme = one character) output
    # with the surface form of the entire sentence in the first token.
    # This can take into account the rules over the word boundaries.
    # emphon_noipa_lax = ('emphon', 'EmPhon', 'EmPhon without ipaization and lax format', (),
    #                     {'source_fields': {'form', 'anas'},
    #                      'target_fields': ['phon'],
    #                      'strict_xtsv_format': False,
    #                      'transcriber_opts': {'ipaize': False, 'optional_palatal_assimilation': False},
    #                      },
    #                     )

    # Produces inner representation (one phoneme = one character) output with one surface form per line.
    # Does not work over word boundaries.
    # emphon_noipa_strict = ('emphon', 'EmPhon', 'EmPhon without ipaization and lax format', (),
    #                     {'source_fields': {'form', 'anas'},
    #                      'target_fields': ['phon'],
    #                      'strict_xtsv_format': True,
    #                      'transcriber_opts': {'ipaize': False, 'optional_palatal_assimilation': False},
    #                      },
    #                     )

    emphon = ('emphon', 'EmPhon', 'EmPhon without ipaization and lax format', (),
                        {'source_fields': {'form', 'anas'},
                         'target_fields': ['phon'],
                         'include_sentence': opts.include_sentence,
                         'transcriber_opts': {'ipaize': opts.ipaize,
                                              'optional_palatal_assimilation': opts.opt_palatal_assim},
                         },
              )

    tools = [(emphon, ('emphon', 'Phonetic transcriber ', 'emPhon'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, opts.conllu_comments))

    # TODO this method is recommended when debugging the tool
    # Alternative: Run specific tool for input (still in emtsv format):
    # from xtsv import process
    # from emphon import EmPhon
    # output_iterator.writelines(process(input_data, EmPhon(*emphon[3], **emphon[4])))

    # Alternative2: Run REST API debug server
    # from xtsv import pipeline_rest_api, singleton_store_factory
    # app = pipeline_rest_api('TEST', tools, {},  conll_comments=False, singleton_store=singleton_store_factory(),
    #                         form_title='TEST TITLE', doc_link='https://github.com/dlt-rilmta/emdummy')
    # app.run()


if __name__ == '__main__':
    main()

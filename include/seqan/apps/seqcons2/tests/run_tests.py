#!/usr/bin/env python
"""Execute the tests for the seqcons2 program.

The golden test outputs are generated by the script generate_outputs.sh.

You have to give the root paths to the source and the binaries as arguments to
the program.  These are the paths to the directory that contains the 'projects'
directory.

Usage:  run_tests.py SOURCE_ROOT_PATH BINARY_ROOT_PATH
"""
import logging
import os.path
import sys

# Automagically add util/py_lib to PYTHONPATH environment variable.
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                    '..', '..', 'util', 'py_lib'))
sys.path.insert(0, path)

import seqan.app_tests as app_tests

def main(source_base, binary_base):
    """Main entry point of the script."""

    print 'Executing test for seqcons2'
    print '==========================='
    print

    ph = app_tests.TestPathHelper(
        source_base, binary_base,
        'apps/seqcons2/tests')  # tests dir

    # ============================================================
    # Auto-detect the binary path.
    # ============================================================

    path_to_seqcons = app_tests.autolocateBinary(
      binary_base, 'bin', 'seqcons2')

    # ============================================================
    # Built TestConf list.
    # ============================================================

    # Build list with TestConf objects, analoguely to how the output
    # was generated in generate_outputs.sh.
    conf_list = []

    # We prepare a list of transforms to apply to the output files.  This is
    # used to strip the input/output paths from the programs' output to
    # make it more canonical and host independent.
    ph.outFile('-')  # To ensure that the out path is set.
    transforms = [
        app_tests.ReplaceTransform(
            os.path.join(ph.source_base_path,
                         'apps/seqcons2/tests') + os.sep,
            '', right=True),
        app_tests.ReplaceTransform(ph.temp_dir + os.sep, '', right=True),
        app_tests.RegexpReplaceTransform(r'Overall time: .*s', r'Overall time: <removed>s', right=True, left=True),
        app_tests.NormalizeScientificExponentsTransform(),
        ]

    # ============================================================
    # Test seqcons2
    # ============================================================

    # overlap_consensus and nop for FASTA input
    for method in ['overlap_consensus', 'nop']:
        conf = app_tests.TestConf(
            program=path_to_seqcons,
            args=['-m', method,
                  '-i', ph.inFile('alns1.sam'),
                  '-oc', ph.outFile('alns1.%s.fa' % method),
                  '-oa', ph.outFile('alns1.%s.sam' % method),
              ],
            redir_stdout=ph.outFile('alns1.%s.sam.stdout' % method),
            redir_stderr=ph.outFile('alns1.%s.sam.stderr' % method),
            to_diff=[(ph.inFile('alns1.%s.fa' % method),
                      ph.outFile('alns1.%s.fa' % method)),
                     (ph.inFile('alns1.%s.sam' % method),
                      ph.outFile('alns1.%s.sam' % method)),
                     (ph.inFile('alns1.%s.sam.stderr' % method),
                      ph.outFile('alns1.%s.sam.stderr' % method),
                      transforms),
                     (ph.inFile('alns1.%s.sam.stdout' % method),
                      ph.outFile('alns1.%s.sam.stdout' % method),
                      transforms),
            ])
        conf_list.append(conf)

    # all consensus variants (except for align) for SAM input
    for oa_ext in ['.sam', '.txt']:
        for method in ['overlap_consensus', 'pos_consensus',
                       'contig_consensus', 'realign', 'nop']:
            args = ['-m', method,
                    '-i', ph.inFile('alns1.sam'),
                    '-oa', ph.outFile('alns1.%s%s' % (method, oa_ext)),
                ]
            to_diff = [(ph.inFile('alns1.%s.fa' % method),
                        ph.outFile('alns1.%s.fa' % method)),
                       (ph.inFile('alns1.%s%s' % (method, oa_ext)),
                        ph.outFile('alns1.%s%s' % (method, oa_ext))),
                       (ph.inFile('alns1.%s%s.stderr' % (method, oa_ext)),
                        ph.outFile('alns1.%s%s.stderr' % (method, oa_ext)),
                        transforms),
                       (ph.inFile('alns1.%s%s.stdout' % (method, oa_ext)),
                        ph.outFile('alns1.%s%s.stdout' % (method, oa_ext)),
                        transforms)
                   ]
            if oa_ext != '.txt':
                args += ['-oc', ph.outFile('alns1.%s.fa' % method),]
                to_diff += [(ph.inFile('alns1.%s.fa' % method),
                             ph.outFile('alns1.%s.fa' % method))]
            conf = app_tests.TestConf(
                program=path_to_seqcons,
                args=args,
                redir_stdout=ph.outFile('alns1.%s%s.stdout' % (method, oa_ext)),
                redir_stderr=ph.outFile('alns1.%s%s.stderr' % (method, oa_ext)),
                to_diff=to_diff)
            conf_list.append(conf)

    # align_consensus for longer sequences that are roughly globally similar
    for oa_ext in ['.sam', '.txt']:
        for method in ['align_consensus']:
            args = ['-m', method,
                    '-i', ph.inFile('seqs2.fa'),
                    '-oa', ph.outFile('seqs2.%s%s' % (method, oa_ext)),
                ]
            to_diff = [(ph.inFile('seqs2.%s.fa' % method),
                        ph.outFile('seqs2.%s.fa' % method)),
                       (ph.inFile('seqs2.%s%s' % (method, oa_ext)),
                        ph.outFile('seqs2.%s%s' % (method, oa_ext))),
                       (ph.inFile('seqs2.%s%s.stderr' % (method, oa_ext)),
                        ph.outFile('seqs2.%s%s.stderr' % (method, oa_ext)),
                        transforms),
                       (ph.inFile('seqs2.%s%s.stdout' % (method, oa_ext)),
                        ph.outFile('seqs2.%s%s.stdout' % (method, oa_ext)),
                        transforms)
                   ]
            if oa_ext != '.txt':
                args += ['-oc', ph.outFile('seqs2.%s.fa' % method),]
                to_diff += [(ph.inFile('seqs2.%s.fa' % method),
                             ph.outFile('seqs2.%s.fa' % method))]
            conf = app_tests.TestConf(
                program=path_to_seqcons,
                args=args,
                redir_stdout=ph.outFile('seqs2.%s%s.stdout' % (method, oa_ext)),
                redir_stderr=ph.outFile('seqs2.%s%s.stderr' % (method, oa_ext)),
                to_diff=to_diff)
            conf_list.append(conf)

    # Execute the tests.
    failures = 0
    for conf in conf_list:
        res = app_tests.runTest(conf)
        # Output to the user.
        print ' '.join([os.path.basename(conf.program)] + conf.args),
        if res:
             print 'OK'
        else:
            failures += 1
            print 'FAILED'

    # Cleanup.
    ph.deleteTempDir()

    print '=============================='
    print '     total tests: %d' % len(conf_list)
    print '    failed tests: %d' % failures
    print 'successful tests: %d' % (len(conf_list) - failures)
    print '=============================='
    # Compute and return return code.
    return failures != 0


if __name__ == '__main__':
    sys.exit(app_tests.main(main))

#!/usr/bin/env python

import optparse
import morse.code
import sys


def print_file_formats():    
    print "\n".join(morse.code.available_file_formats())
    sys.exit(0)

o = optparse.OptionParser()
o.add_option("-i", "--input", dest="input_filename")
o.add_option("-e", "--encoding", default="vorbis", dest="output_encoding")
o.add_option("-f", "--format", default="ogg", dest="output_format")
o.add_option("--list-formats", action="store_true", dest="list_formats")
o.add_option("--list-encodings", dest="encoding_list")
o.add_option("-o", "--output", dest="output_filename")
o.add_option("-v", "--verbose", action="store_true", dest="verbose")
(opts, args) = o.parse_args()

if opts.encoding_list is not None:
    if opts.encoding_list not in morse.code.available_file_formats():
        print "Invalid file format"
        sys.exit(1)
    print "File encodings for %s" % opts.encoding_list
    print "\n".join(morse.code.available_encodings(opts.encoding_list))
    sys.exit(0)

if opts.list_formats:
    print_file_formats()

m = None
output = None
if opts.output_filename is not None:    
    m = morse.code.TelegraphWriter(opts.output_filename, opts.output_format, opts.output_encoding)
else:
    m = morse.code.TelegraphPlayer()

if opts.input_filename is not None:
    with open(opts.input_filename) as f:
        for line in f:
            if opts.verbose:
                print line
            m.encode(line)
elif len(args) != 0:
    m.encode(" ".join(args))
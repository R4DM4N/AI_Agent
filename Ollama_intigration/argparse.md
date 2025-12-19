(module) argparse

Command-line parsing library

This module is an optparse-inspired command-line parsing library that:

  - handles both optional and positional arguments
  - produces highly informative usage messages
  - supports parsers that dispatch to sub-parsers

The following is a simple usage example that sums integers from the
command-line and writes the result to a file:

    parser = argparse.ArgumentParser(
        description='sum the integers at the command line')
    parser.add_argument(
        'integers', metavar='int', nargs='+', type=int,
        help='an integer to be summed')
    parser.add_argument(
        '--log',
        help='the file where the sum should be written')
    args = parser.parse_args()
    with (open(args.log, 'w') if args.log is not None
          else contextlib.nullcontext(sys.stdout)) as log:
        log.write('%s' % sum(args.integers))

The module contains the following public classes:

  - ArgumentParser -- The main entry point for command-line parsing. As the
example above shows, the add\_argument() method is used to populate
the parser with actions for optional and positional arguments. Then
the parse\_args() method is invoked to convert the args at the
command-line into an object with attributes.

  - ArgumentError -- The exception raised by ArgumentParser objects when
there are errors with the parser's actions. Errors raised while
parsing the command-line are caught by ArgumentParser and emitted
as command-line messages.

  - FileType -- A factory for defining types of files to be created. As the
example above shows, instances of FileType are typically passed as
the type= argument of add\_argument() calls. Deprecated since
Python 3.14.



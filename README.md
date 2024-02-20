# transCISter
A tool for parsing information from compliance benchmark PDFs for use in security configuration assessments.

Note: This uses Apple's [Pkl](https://pkl-lang.org) config-as-code language, NOT the Python [pickle](https://docs.python.org/3/library/pickle.html) object serialization library. Pickles are insecure anyways, so it's no big loss. Just keep that in mind when working with this tool.

There are two components to this tool:

1. The extraction script, which reads a specified PDF and extracts text based on categories defined in a configuration file, exporting to the desired format (csv, json,pkl, etc)
2. The benchmark creation script, which takes a given compliance configuration file and formats it based on a specified SCA tool.

In the initial version, this converts a CIS benchmark PDF into a Wazuh-compatible YAML file.
# `des-ini-utils`
A set of tools to compare and dump the contents of producer install.ini files.

# Components
* `inicompare` - compares two Designer install.ini files, reporting how similar or different they are. This tool can detect whether the files are totally identical (in terms of raw content), whether their functional content (everything except comments/whitespace) is identical, and whether the functional content of the files is different. When functional content is different, the differences between the two files are reported.
In every case, the tool reports any line found in either file that both ISN'T a comment, and DOESN'T begin with the prefix "::InstallAPI::SetVirtualText -virtualtext".

* `inidump` - dumps the provided INI file as a JSON file at the path provided. If no path is provided, the file is dumped at the location where this script was called from.

# Usage
* `inicompare` - `$ inicompare file1 file2`
    * example: 
    ```
    $ inicompare ex1.ini ex2.ini

    ******************************************
    The parameters in the provided files are the same, but not necessarily in the same order.

    ******************************************
    The following non-parameter, non-comment lines were found:
    {'both': ['this line was not prefixed by the predefined constant and was in both files', 'and so was this one'],
    'ex1.ini': ['this line was in ex1.ini only'],
    'ex2.ini': ['and this line was only in ex2.ini']}
    ```

* `inidump` - `$ inidump input [output]`
    * example:
    ```
    $ inidump ex1.ini
    Output file created at C:\Users\nmuise\Desktop\python_projects\inicompare\inicompare\ex1.json
    
    $ inidump ex1.ini ..\custom.json
    Output file created at C:\Users\nmuise\Desktop\python_projects\inicompare\custom.json
    ```

# Installation
Prebuilt wheels of this project are available under the dist directory. Alternatively, build and install your own.

Once this package is installed to your machine, you will be able to use its commands in the shell from any location.

# `inicompare`
A tool to compare and dump the contents of producer install.ini files.

# Components
* `inicompare` - compares two Designer install.ini files, reporting how similar or different they are. This tool can detect whether the files are totally identical, whether their functional content (everything except comments) is identical (but the rest isn't), or whether the content of the files is different. When functional content is different, the differences between the two files are reported.
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
If installing this utility from a .tar.gz, a wheel, or other similar format through pip, be sure to enable the --user option. Otherwise, you may not be able to execute the primary functions of this package from the commandline directly. 
Also be aware of any warnings pip issues when installing with the --user option. In particular, if you see `WARNING: The scripts inicompare.exe and inidump.exe are installed in '/some/path/on/your/machine' which is not on PATH.`, you'll need to add that directory to your PATH in order to use this package effectively.

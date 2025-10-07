#  MD2PDF

everyone needs pdfs, i hate making them. but i *do* like markdown,

```sh
usage: md2pdf [-h] [-i INCLUDE] [-t TEMPLATE] [-v VERBOSE] input [output]

md2pdf turns markdown documents into pdfs with a custom template

positional arguments:
  input                 path to the input markdown file
  output                path to the output file (default: out.pdf)

options:
  -h, --help            show this help message and exit
  -i, --include INCLUDE
                        path of extra files to include in rendering (either directory or a single file) (default: None)
  -t, --template TEMPLATE
                        path to the template directory (default: ./template)
  -v, --verbose VERBOSE
                        more logging output
```


Templates are normal html files with a `<mardown-insert/>` tag for where the parsed markdown should go.

## Caveats: 

The include and template directories are copied to a temporary directory that is used as the root when rendering the html. This means that there cannot be files sharing the same name in either directory.



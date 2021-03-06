"""Convert wikiextractor preprocessed text to tokenized text.

## Usage

```sh
$ cd dataset/nlp/wikipedia
$ python /your/path/to/dl-cliche/tool/ja_wiki_text8_tokenize.py --path . --norm `find . -name '??' -printf '%f '`
```

## Expected Files Before Processing

```sh
$ ls dataset/nlp/wikipedia/
AA  AC  AE  AG  AI  AK  AM  AO  AQ  AS  AU  AW  AY  BA
AB  AD  AF  AH  AJ  AL  AN  AP  AR  AT  AV  AX  AZ
```

## Expected Files After Processing

If normalized, files will be created under folder 'norm'.

```sh
$ ls dataset/nlp/wikipedia/norm
full_ja_AA.wakachi  full_ja_AB.wakachi  full_ja_AC.wakachi
full_ja_AD.wakachi  full_ja_AE.wakachi  full_ja_AF.wakachi
...

If not normalized, files will be stored under folder 'asis'.
"""

from dlcliche.utils import *
from dlcliche.nlp_mecab import *
import re
import argparse
parser = argparse.ArgumentParser(description='Wikipedia tokenizer')
parser.add_argument('--path', '-p', default='dataset/nlp/wikipedia', type=str,
                    help='Full pathname for full wikiextractor outputs, and will also output tokened data there.')
parser.add_argument('--norm', '-n', default=False, action='store_true',
                    help='Normalize words if set, default is False.')
parser.add_argument('sub_folders', default='', type=str, nargs='+',
                    help='Sub folders to process (ex. AA AB ...), blank will process all sub folders.')
args = parser.parse_args()

# Confiure yours
WIKI_PATH=Path(args.path) # <<=== Set this to your wikipedia dump

# Prepare major processing instances
tokenizer = get_mecab_tokenizer(normalize=args.norm)
doc_filter_begin = re.compile('<doc[^>]+>\n')
doc_filter_end = re.compile('<\/doc>\n')

# Complete sub_folders
sub_folders = args.sub_folders if args.sub_folders is not '' else \
    [str(f.name) for f in WIKI_PATH.glob('??')]
output_folder = WIKI_PATH/'norm' if args.norm else WIKI_PATH/'asis'
ensure_folder(output_folder)
print('Output to', output_folder)

# Process
for folder_id in sub_folders:
    folder = WIKI_PATH/folder_id
    with open(f'{output_folder/"full_ja_"}{folder_id}.wakachi', 'w') as out_f:
        for file in folder.glob('wiki*'):
            print('Processing', file)
            with file.open() as f:
                lines = f.read()
            lines = doc_filter_begin.sub('', lines)
            lines = doc_filter_end.sub('', lines)
            lines = lines.split('\n')
            try:
                for line in lines:
                    if len(line) == 0: continue
                    tokens = tokenizer.tokenize(line)
                    out_f.write(' '.join(tokens)+'\n')
            except:
                print('!!! Tokenizer failed. Skipped:', file)

# eof

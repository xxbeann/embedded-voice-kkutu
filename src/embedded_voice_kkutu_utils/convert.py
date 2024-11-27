import argparse
from json import dumps

PREFIX_PATH = '/src'
KKUTU_SUBMODULE_PATH = f'.{PREFIX_PATH}/kkutu'
ASSETS_WORDS_PATH = './assets/words.json'

def load_from_kkutu_sql(path: str=f'{KKUTU_SUBMODULE_PATH}/db.sql') -> list[str]:
    f = open(f'{KKUTU_SUBMODULE_PATH}/db.sql', 'r', encoding='utf-8')
    is_word_table_entered = False
    words: list[str] = []
    while True:
        line = f.readline()
        if is_word_table_entered:
            words.append(line.split()[0])
            if line.strip() == '\\.':
                return words
        elif 'COPY kkutu_ko' in line:
            is_word_table_entered = True

def optimize_word_list_to_dict(words_list: list) -> dict[str, str]:
    words_dict: dict[str, str] = {}
    for each in words_list:
        if each[0] not in words_dict:
            words_dict[each[0]] = [each]
        else:
            words_dict[each[0]].append(each)
    return words_dict

def dump_words(words_list: list[str]=None, words_dict: dict[str, str]=None, path: str=ASSETS_WORDS_PATH):
    if words_list == None and words_dict == None:
        raise ValueError('Least one of words_list or words_dict should be provided.')
    _dumping = {
        'enabled': {
            'words_list': words_list != None,
            'words_dict': words_dict != None
        },
    }
    if words_list != None:
        _dumping['words_list'] = words_list
    if words_dict != None:
        _dumping['words_dict'] = words_dict
    with open(path, 'w', encoding='utf-8') as f:
        f.write(dumps(_dumping, ensure_ascii=False))

def main() -> int:
    parser = argparse.ArgumentParser(description='Convert kkutu words to json')
    parser.add_argument('--in-file', type=str, default=f'{KKUTU_SUBMODULE_PATH}/db.sql' ,help='Input file path. Default is `db.sql` in kkutu submodule. (./kkutu/db.sql)')
    parser.add_argument('--out-file', type=str, default=ASSETS_WORDS_PATH, help='Output file path. Default is `./assets/words.json`')
    parser.add_argument('--in-type', choices=['kkutu'], default='kkutu', help='Input db type. Default is `kkutu`')

    args = parser.parse_args()
    if args.in_type == 'kkutu':
        words_list = load_from_kkutu_sql(args.in_file)
        words_dict = optimize_word_list_to_dict(words_list)
        dump_words(words_list=words_list, words_dict=words_dict, path=args.out_file)
    else:
        print('Only kkutu is supported for now.')
        return 0

if __name__ == '__main__':
    main()

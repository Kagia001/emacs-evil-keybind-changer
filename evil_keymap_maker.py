import re

with open("/home/karl/.emacs.d/elpa/evil-20210109.807/evil-maps.el.original") as file:
    original_map = file.read().splitlines()

file = open("/home/karl/.emacs.d/elpa/evil-20210109.807/evil-maps.el", "w")

layoutlower = {
    "a": "a",
    "t": "b",
    "x": "c",
    "c": "d",
    "k": "e",
    "e": "f",
    "g": "g",
    "m": "h",
    "l": "i",
    "y": "j",
    "n": "k",
    "u": "l",
    "h": "m",
    "j": "n",
    "r": "p",
    "q": "q",
    "s": "r",
    "d": "s",
    "f": "t",
    "i": "u",
    "v": "v",
    "w": "w",
    "z": "x",
    "o": "y",
    "p": "ø",
    ":": "o",
}
layoutupper = dict((k.upper(), v.upper()) for k, v in layoutlower.items())
letter_map = layoutlower | layoutupper
letter_map["b"] = "<"
letter_map["B"] = ">"
letter_map["<"] = "z"
letter_map[">"] = "Z"

things_to_ignore = [r'RET', r"\\C-", r"DEL"]

def string_assign(string, index, letter):
    string = list(string)
    string[index] = letter
    return ''.join(string)

def parse_define_key(content):
    content = content.split(" ")
    for content_block in content:
        if re.search("vconcat", content_block):
            # line 164 or 165 for zt. They are different from the other lines so i have to do this instead
            pass

        elif re.search('"<.*>"', content_block):
            # uses keys like <insert>
            pass

        elif re.search('".*"', content_block):
            # key is kbd or just letter string

            # ignore "
            letters = re.search('(?<=")[^"]*(?=")', content_block).group()

            letters_to_swap = []
            letters_to_keep = []
            new_letters = letters

            # find out which letters to swap and which to keep

            for thing_to_ignore in things_to_ignore:
                ignore = re.search(thing_to_ignore, letters
                )  # RET is never used twice in a line, so this works
                if ignore:
                    # for index in range(ret.span()):
                    for index in range(ignore.span()[0], ignore.span()[1]):
                        letters_to_keep.append(index)

            mod = re.search(
                r"\\C-", "".join(letters)
            )  # RET is never used twice in a line, so this works
            if mod:
                # for index in range(ret.span()):
                for index in range(mod.span()[0], mod.span()[1]):
                    letters_to_keep.append(index)

            for i in range(len(letters)):
                if i not in letters_to_keep:
                    letters_to_swap.append(i)

            # replace letters, ignore if not in letter_map
            for letter_index in letters_to_swap:
                try:
                    new_letters = string_assign(new_letters, letter_index, letter_map[letters[letter_index]])
                except KeyError:
                    print(letters[letter_index], "not in letter_map, skipping")

            letters = new_letters

            letters = "".join(new_letters)
            letters = f'"{letters}"'
            content[content.index(content_block)] = letters

        elif re.match(r"[.*]", content_block):
            # uses keys in brackets like [left] or [escape]
            pass

        else:
            # irrelevant content-block
            pass
    return " ".join(content)


def parse_line(line):
    if line.find("(define-key") != -1:
        return parse_define_key(line)
    else:
        return line



parsed_map = [parse_line(i) for i in original_map]

file.write('\n'.join(parsed_map))
file.close()

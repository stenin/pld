import re

def show_match_example(pattern, line, flags=0):
    # create match object
    m = re.match(pattern, line, flags)
    if m:
        print ' '.join([line, 'matches', pattern])
        print ' '.join(['because','"' + m.group() + '"', 'provides this match\n'])
        return
    print ' '.join([line, 'does not matches', pattern])


if __name__ == "__main__":
    intro_message = """
\w matches letters, digits and _ symbol (equivalent to [0-9a-zA-Z_], see below for more explanation)
\W matches all other symbols
\d matches digits (equivalent to [0-9])
\D matches all other symbols
[abh] matches any symbol from the set - a or b or h
[^abh] matches all other symbols, excluding a, b and h
[3-7] stands for range - matches any digit from range from 3 to 7
[^3-6] matches any symbol excluding 3, 4, 5, 6
* stands for 'zero or more times'
+ stands for 'one or more times'

Here goes examples:
"""
    print intro_message
    lines = [
        "123",
        "ok",
        "OK_",
        " foo bar baz 12345"
    ]
    patterns = [
        r'\w',
        r'\W',
        r'\w*',
        r'[\d ]',
    ]

    for l in lines:
        for p in patterns:
            show_match_example(p, l)


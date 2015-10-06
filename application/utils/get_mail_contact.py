# -*- encoding: utf-8 -*-
import poplib
from email.header import decode_header
from email.utils import parseaddr


def find_sender(c):
    for line in c:
        if line.lower().startswith('from:'):
            return line


def parse_contact(line):
    desc, sender = parseaddr(line)
    name, charset = decode_header(desc)[0]
    if charset:
        name = name.decode(charset)
    else:
        try:
            name = name.decode('gbk')
        except:
            print 'decode with utf8'
            name = name.decode('utf8')
    return sender, name


def get_contact(host, username, password):
    pp = poplib.POP3_SSL(host)
    # pp = poplib.POP3(host)
    pp.user(username)
    pp.pass_(password)
    cnt, total_bytes = pp.stat()
    cnt = min(cnt, 60)
    raw_contacts = {find_sender(pp.top(i, 0)[1]) for i in range(1, cnt)}
    pp.quit()
    return {parse_contact(line) for line in raw_contacts if line}

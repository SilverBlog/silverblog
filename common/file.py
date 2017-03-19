def read_file(filename):
    f = open(filename, newline=None)
    content = f.read()
    return content


def write_file(filename, content):
    f = open(filename, "w", newline=None)
    f.write(content)
    f.close()
    return True

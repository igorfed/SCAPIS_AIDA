from pathlib import Path

# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    contents = list(dir_path.iterdir())
    #print(contents)
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir(): # extend the prefix and recurse:

            extension = branch if pointer == tee else space
            #print("branch", branch, " pointer:", pointer, "tee", tee, "ext", extension)
            #print ('ext', extension)
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)
    print('---')
    print(contents[0])
    print(contents[1])
    print(contents[3])
#tree(Path.home() / '/media/igofed/DATA/SCAPIS_Processed_Data/scapis')
for line in tree(Path.home() / '/media/igofed/DATA/SCAPIS_Processed_Data/scapis'):
    #print(line)
    continue


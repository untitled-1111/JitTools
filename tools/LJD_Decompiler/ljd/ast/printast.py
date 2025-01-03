import ljd.ast.nodes as nodes
import ljd.ast.slotworks

_printers = {}
_indent_unit = '\t'


def dump(name, obj, level=0, prefix=None, exclude=None, **kwargs):
    indent = level * _indent_unit

    if prefix is None:
        if name is not None:
            prefix = indent + str(name) + " = "
        else:
            prefix = indent

    if isinstance(obj, (int, float, str)):
        print(prefix + str(obj))
    elif isinstance(obj, list):
        if len(obj) == 0:
            print(prefix + "[]")
            return

        print(prefix + "[")

        for value in obj:
            dump(None, value, level + 1)

        print(indent + "]")
    elif isinstance(obj, dict):
        print(prefix + "{")

        for key, value in obj.items():
            dump(key, value, level + 1)

        print(indent + "}")
    elif type(obj) in _printers:
        _printers[type(obj)](obj, prefix, level, **kwargs)
    else:
        _print_default(obj, prefix, level, exclude=exclude)


def _print_default(obj, prefix, level, exclude_blocks=False, exclude=None, extra_attrs=None):
    header_keys = _header(prefix, obj, attrs=extra_attrs)

    for key in dir(obj):
        if key.startswith("__") or key in header_keys:
            continue

        if exclude and key in exclude:
            continue

        val = getattr(obj, key)

        # Exclude methods, they're of no use
        if callable(val):
            continue

        # Definitely don't show the blocks, otherwise it explodes the output
        if exclude_blocks and isinstance(val, nodes.Block):
            print(_indent_unit * (level + 1) + key + " = Block[index=%d]" % val.index)
            continue

        # Exclude class variables
        cls = obj.__class__
        if hasattr(cls, key) and getattr(cls, key) == val:
            continue

        # Since we just stripped the class variables, annotate ints with their matching
        # class variables so we can see what's happening
        val = _const_lookup(obj, val)

        dump(key, val, level + 1)


def _const_lookup(obj, val):
    # If this value is an int, do a lookup to see if there's a constant for it
    if type(val) != int:
        return val

    # Build the lookup table if it's not already there
    cls = obj.__class__
    if not hasattr(cls, "__printast_const_lookup"):
        lookup_tbl = {}
        for const_key in dir(cls):
            const_val = getattr(cls, const_key)
            if type(const_val) != int:
                continue
            lookup_tbl[const_val] = const_key
        cls.__printast_const_lookup = lookup_tbl
    lookup_tbl = cls.__printast_const_lookup

    if val not in lookup_tbl:
        return val
    return "%s (%d)" % (lookup_tbl[val], val)


def _header(prefix, obj, attrs=None, suffix="", **values):
    if attrs is None:
        attrs = ["_addr", "_line"]

    notes_name = "_dbg_notes"
    if hasattr(obj, notes_name):
        attrs.append(notes_name)

    for name in attrs:
        if not hasattr(obj, name):
            continue
        pretty_name = name.lstrip("_")
        values[pretty_name] = getattr(obj, name)

    if len(values) == 0:
        attr_block = ""
    else:
        attr_block = "[%s]" % ", ".join(["%s=%s" % (k, v) for k, v in values.items()])

    if suffix != "":
        suffix = ": " + str(suffix)

    print(prefix + type(obj).__name__ + attr_block + suffix)

    return attrs


def _printer(klass):
    def wrapper(func):
        _printers[klass] = func
        return func

    return wrapper


# TODO add some way to show the _addr elements of all these

@_printer(nodes.Identifier)
def _print_str(obj, prefix, level):
    print(prefix + str(obj))


@_printer(nodes.Constant)
def _print_const(obj: nodes.Constant, prefix, level):
    s = '"' + obj.value + '"' if obj.type == nodes.Constant.T_STRING else obj.value
    _header(prefix, obj, suffix=s)


@_printer(nodes.Assignment)
def _print_assn(obj: nodes.Assignment, prefix, level):
    _header(prefix, obj, type=["T_LOCAL_DEFINITION", "T_NORMAL"][obj.type])
    dump("dest", obj.destinations, level + 1, omit_single=True)
    dump("expr", obj.expressions, level + 1, omit_single=True)


@_printer(nodes.VariablesList)
@_printer(nodes.ExpressionsList)
@_printer(nodes.StatementsList)
def _print_list(obj: nodes.VariablesList, prefix: str, level, omit_single=False):
    name = prefix[:-2].strip()  # chop out the = and strip it to recover the name

    if len(obj.contents) == 0:
        print(prefix + type(obj).__name__ + "[empty]")
    elif len(obj.contents) == 1:
        if omit_single:
            dump(name, obj.contents[0], level)
        else:
            print(prefix + type(obj).__name__ + "[single]: ", end='')
            dump(None, obj.contents[0], level, prefix="")
    else:
        print(prefix + type(obj).__name__ + "[")
        for value in obj.contents:
            dump(None, value, level + 1)
        print(_indent_unit * level + "]")


@_printer(nodes.TableElement)
def _print_table_elem(obj: nodes.TableElement, prefix, level):
    print(prefix + "TableElement")
    dump("table", obj.table, level + 1)
    dump("key", obj.key, level + 1)


@_printer(nodes.UnconditionalWarp)
@_printer(nodes.ConditionalWarp)
@_printer(nodes.IteratorWarp)
@_printer(nodes.NumericLoopWarp)
@_printer(nodes.EndWarp)
def _print_warp(obj, prefix, level):
    _print_default(obj, prefix, level, exclude_blocks=True)


@_printer(nodes.Block)
def _print_block(obj, prefix, level):
    _print_default(obj, prefix, level, extra_attrs=["index", "first_address", "last_address"])


@_printer(ljd.ast.slotworks.SlotInfo)
def _print_slot_info(obj: ljd.ast.slotworks.SlotInfo, prefix, level):
    _print_default(obj, prefix, level, exclude=["references", "function"])
    # TODO print out addresses from the top of the path for each reference
    refs = ", ".join([str(i.path[-1]) for i in obj.references])
    print(_indent_unit * (level + 1) + "references = [%s]" % refs)


@_printer(nodes.Primitive)
def _print_primitive(obj, prefix, level):
    _header(prefix, obj, type=_const_lookup(obj, obj.type))

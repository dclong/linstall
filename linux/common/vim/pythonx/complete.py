
def complete(t, opts):
    if t:
        opts = [m[len(t):] for m in opts if m.startswith(t)]
    n = len(opts)
    if n == 0:
        return ""
    if n == 1:
        return opts[0]
    return "(" + "|".join(opts) + ")"
#edef complete

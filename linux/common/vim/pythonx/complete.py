

__auto_complete__ = True

def complete(t, opts):
    import vim
    global __auto_complete__
#    if not __auto_complete__:
#        return ""
    nt = len(t)
    if nt:
        opts = [m[len(t):] for m in opts if m.startswith(t)]
        #opts = [m for m in opts if m.startswith(t)]
    n = len(opts)
    if n == 0:
        return ""
    if n == 1:
        #__auto_complete__ = False
        opt = opts[0]
#        vim.command('normal ' + str(nt - 1) + 'h' + str(nt) + 'xi' + opt)
#        __auto_complete__ = True
        #vim.command('normal ' + str(nt) + 'X')
#        return ""
        return opt
    return "(" + "|".join(opts) + ")"
#edef complete

import re,sys

def scope_css(css, scope='main'):
    """Prefix every style rule selector with `scope ` so rules only apply
    inside <main>. Leaves @keyframes bodies and :root alone. Handles @media/
    @supports by scoping the selectors inside them. Converts bare html/body to
    the scope itself."""
    out=[]
    i=0; n=len(css)
    def scope_selector_list(sel):
        parts=[p.strip() for p in sel.split(',')]
        res=[]
        for p in parts:
            if not p: continue
            # scope :root vars to the main subtree (avoid leaking into shell)
            if p.startswith(':root'):
                res.append(scope); continue
            # bare html/body -> the scope element itself (so main gets base rules)
            if p in ('html','body','html body','*'):
                res.append(scope if p!='*' else scope+' *')
                continue
            if p.startswith('html') or p.startswith('body'):
                # strip leading html/body, then scope the rest
                p=re.sub(r'^(html\s+body|html|body)\s+','',p)
                res.append(scope+' '+p)
                continue
            res.append(scope+' '+p)
        return ', '.join(res)

    while i<n:
        # find next { or @
        at=css.find('@',i)
        br=css.find('{',i)
        if br==-1:
            out.append(css[i:]); break
        if at!=-1 and at<br:
            # at-rule
            # read at-rule name
            m=re.match(r'@([a-zA-Z-]+)',css[at:])
            name=m.group(1).lower() if m else ''
            # copy text before at
            out.append(css[i:at])
            if name in ('media','supports'):
                # @media ... { <inner rules> }
                open_br=css.find('{',at)
                prelude=css[at:open_br+1]
                # find matching close brace
                depth=1; j=open_br+1
                while j<n and depth>0:
                    if css[j]=='{':depth+=1
                    elif css[j]=='}':depth-=1
                    j+=1
                inner=css[open_br+1:j-1]
                out.append(prelude)
                out.append(scope_css(inner,scope))  # recurse to scope inner selectors
                out.append('}')
                i=j
                continue
            elif name in ('keyframes','-webkit-keyframes','font-face','page','charset','import','namespace'):
                # copy whole block/line unchanged
                open_br=css.find('{',at)
                if open_br==-1 or (name in ('charset','import','namespace')):
                    # line at-rule
                    semi=css.find(';',at)
                    out.append(css[at:semi+1]); i=semi+1; continue
                depth=1;j=open_br+1
                while j<n and depth>0:
                    if css[j]=='{':depth+=1
                    elif css[j]=='}':depth-=1
                    j+=1
                out.append(css[at:j]); i=j; continue
            else:
                # unknown at-rule with block: copy prelude, scope inside
                open_br=css.find('{',at)
                depth=1;j=open_br+1
                while j<n and depth>0:
                    if css[j]=='{':depth+=1
                    elif css[j]=='}':depth-=1
                    j+=1
                out.append(css[at:open_br+1]); out.append(scope_css(css[open_br+1:j-1],scope)); out.append('}'); i=j; continue
        else:
            # normal rule: selector { decls }
            sel=css[i:br]
            # find matching close
            depth=1;j=br+1
            while j<n and depth>0:
                if css[j]=='{':depth+=1
                elif css[j]=='}':depth-=1
                j+=1
            decls=css[br+1:j-1]
            # keep comments in selector area out
            sel_clean=sel
            out.append(scope_selector_list(sel_clean.strip())+'{'+decls+'}')
            i=j
            continue
    return ''.join(out)

if __name__=='__main__':
    css=open(sys.argv[1]).read()
    print(scope_css(css, sys.argv[2] if len(sys.argv)>2 else 'main'))

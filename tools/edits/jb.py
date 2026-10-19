import re,json
def edit_json(s,sid,fn):
    m=re.search(r'(<script[^>]*id="%s"[^>]*>)(.*?)(</script>)'%sid,s,re.S)
    raw=m.group(2); obj=json.loads(raw); assert json.dumps(obj)==raw,sid+' non roundtrip'
    fn(obj); new=json.dumps(obj)
    assert new!=raw,sid+' invariato'
    return s[:m.start(2)]+new+s[m.end(2):]
def rep(s,old,new,cnt=1):
    assert s.count(old)==cnt,(old[:90],s.count(old)); return s.replace(old,new)

import shutil
def mkbackup():
    try:
        sourcepath='C:/PCBRW/brw#185/bdata185/test.txt'
        targetpath='C:/PCBRW/brw#185/bdata185/test_copy.txt'
        res=shutil.copy2(sourcepath, targetpath)
        return str(res)
    except:
        pass

#-*-coding:utf-8-*-
import logutil
import traceback

def log_exception(s, data={}):
    if not data:
        e = str(traceback.format_exc())
    else:
        username = str(data.get("username", "默认名字"))
        idcard = str(data.get("idcard", "0"))
        e = f"{username}|{idcard}|" + str(traceback.format_exc())
    logutil.log("exception", "%s|%s|%s" % ("exception", str(s), str(e)))
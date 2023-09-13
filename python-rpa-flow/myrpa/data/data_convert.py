async def convert_data(data):

    cvData = {
        'is_cron': False,
        'projectName': data.get('projectName', ''),
        'companyId': data.get('companyId', ''),
        'gateName': data.get('sysName', ''),
        'gateNo': data.get('govAttendSysIdentifyCode', ''),
        'username': data.get('govAttendSysAccountUsername', ''),
        'password': data.get('govAttendSysAccountPassword', ''),
        'mainContractor': data.get('companyType', ''),
        'sysLoginUrl': data.get('sysLoginUrl', ''),
        'govSysProjectName': data.get('govAttendSysProjectName', ''),
        'projectNo': data.get('orderNo', '')
    }

    return cvData


# -*- coding: utf-8 -*-
from app.views.common import *
import commands

# 定义蓝图
logs = Blueprint('logs', __name__)


@logs.route('/app', methods=["GET", "POST"])
@login_required  # 登录保护
def apps():
    project_name = request.args.get('project_name')
    host = request.args.get('host')
    
    cmd= "/data/bin/out_file.sh %s"%(project_name)
    salt = saltAPI(host=app.config['SALT_API_ADDR'], user=app.config['SALT_API_USER'],password=app.config['SALT_API_USER'], prot=app.config['SALT_API_PROT'])
    info = salt.saltCmd({"fun": "cmd.run", "client": "local", "tgt": host , "arg":cmd})[0]
    g.Line = info[host]
    g.project_name=project_name
    g.host=host
    return render_template("logs/index.html")


@logs.route('/appms', methods=["GET", "POST"])
@login_required  # 登录保护
def appms():
    if request.method == 'POST':
        line = request.form['line']
        project_name = request.form['project_name']
        host = request.form['host'] 

        cmd= "/data/bin/out_file.sh %s %s"%(project_name,str(int(line)+1))
        print cmd
        status, input = commands.getstatusoutput("/usr/bin/salt '%s' cmd.run '%s'" % (host, cmd))
        return json.dumps({"code": 1, "msg": u"请求数据成功!", "data": input})
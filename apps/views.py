import json
import os
import time
from hashlib import md5

import requests
from flask import Blueprint, request, session, redirect, current_app
from utils import restful
from flask_jwt_extended import create_access_token
from models.auth import User
from models.graph import Graph, GraphCount, DataSet, File, Log
from .forms import LoginForm, DataSetAddForm, DataSetEditForm, UploadFileForm
from exts import db

bp = Blueprint('graph', __name__, url_prefix='/')

def log():
    client_ip = request.headers.get('X-Forwarded-For', None)
    if client_ip:
        client_ip = client_ip.split(',')[0]
    else:
        client_ip = request.remote_addr
    print(client_ip)
    print(request.headers)
    print(request.form)

@bp.route('/')
def index():
    # log()
    graph = Graph.query.all()
    graphcnt = GraphCount.query.first()
    g_list = []
    for x in graph:
        g_list.append(x.to_dict())
    return restful.ok(data={'graphs': g_list, 'graphcnt': graphcnt.to_dict()})

@bp.route("/log")
def graphlog():
    logs = Log.query.all()
    l_list = [l.to_dict() for l in logs]
    return restful.ok(data={'logs': l_list})

@bp.route('/delete', methods=['POST'])
def delete():
    graphid = request.form.get('graphid')
    if not graphid:
        return restful.params_error(message="没有传入id！")
    try:
        graph = Graph.query.get(graphid)
    except Exception as e:
        return restful.params_error(message="此图谱不存在！")
    entitycount = graph.entitycount
    linkcount = graph.linkcount
    eventcount = graph.eventcount
    graphcnt = GraphCount.query.first()
    graphcnt.entitycount -= entitycount
    graphcnt.linkcount -= linkcount
    graphcnt.eventcount -= eventcount
    graphcnt.gpcount -= 1
    db.session.delete(graph)
    db.session.commit()
    graph_list = Graph.query.all()
    g_list = [x.to_dict() for x in graph_list]
    return restful.ok(data={'graphcnt': graphcnt.to_dict(), 'g_list': g_list})

@bp.get('/databag')
def databag():
    dataset = DataSet.query.order_by(DataSet.createtime.desc()).all()
    d_list = [d.to_dict() for d in dataset]
    return restful.ok(data={"d_list":d_list})

@bp.route('/databag/add', methods=['POST'])
def databag_add():
    form = DataSetAddForm(request.form)
    if form.validate():
        dataname = form.dataname.data
        datadescription = form.datadescription.data
        userid = form.userid.data
        datacount = 0
        dataset = DataSet(dataname=dataname,datadescription=datadescription,userid=userid,datacount=datacount)
        db.session.add(dataset)
        db.session.commit()
        return restful.ok(data=dataset.to_dict())
    else:
        return restful.params_error(message=form.messages[0])

@bp.route('/databag/edit', methods=['POST'])
def databag_edit():
    form = DataSetEditForm(request.form)
    if form.validate():
        dataname = form.dataname.data
        datadescription = form.datadescription.data
        dataid = form.dataid.data
        try:
            dataset = DataSet.query.filter_by(dataid=dataid).first()
        except Exception as e:
            return restful.params_error(message="数据集不存在！")
        dataset.dataname = dataname
        dataset.datadescription = datadescription
        db.session.commit()
        return restful.ok(data=dataset.to_dict())
    else:
        return restful.params_error(message=form.messages[0])

@bp.route('/databag/delete', methods=['POST'])
def databag_delete():
    dataid = request.form.get("dataid")
    if not dataid:
        return restful.params_error(message="没有传入id！")
    try:
        dataset = DataSet.query.get(dataid)
    except Exception as e:
        return restful.params_error(message="此数据集不存在！")
    db.session.delete(dataset)
    db.session.commit()
    return restful.ok()

@bp.route('/databag/searcher', methods=['POST'])
def databag_searcher():
    dataname = request.form.get("dataname")
    if not dataname:
        return restful.params_error(message="请输入数据集名称！")
    try:
        dataset = DataSet.query.filter_by(dataname=dataname).all()
    except Exception as e:
        return restful.params_error(message="此数据集不存在！")
    if not dataset:
        return restful.params_error(message="此数据集不存在！")
    d_list = [d.to_dict() for d in dataset]
    return restful.ok(data={"databag_list": d_list})


@bp.route('/databag/files', methods=['POST'])
def databag_files():
    dataid = request.form.get("dataid")
    files = File.query.filter_by(dataid=dataid).all()
    f_list = [f.to_dict() for f in files]
    return restful.ok(data={"files": f_list})

@bp.route('/databag/uploadfile', methods=['POST'])
def databag_uploadfile():
    form = UploadFileForm(request.files)
    if form.validate():
        file = form.file.data
        dataid = request.form.get("dataid")
        filename = file.filename
        ff = File.query.filter_by(filename=filename)
        cnt = 1
        while(ff.first() != None):
            filename = filename+"("+str(cnt)+")"
            ff = File.query.filter_by(filename=filename)
        filepath = os.path.join(current_app.config['DATABAG_FILE_SAVE_PATH'], filename)
        file.save(filepath)
        filetxt = File(filename=filename, filepath=filepath,dataid=dataid)
        db.session.add(filetxt)
        db.session.commit()
        files = File.query.filter_by(dataid=dataid).all()
        f_list = [f.to_dict() for f in files]
        return restful.ok(data={"files": f_list})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.route('/databag/deletefile', methods=['POST'])
def databag_deletefile():
    dataid = 0
    for(key,value) in request.form.items():
        try:
            file = File.query.get(value)
        except Exception as e:
            return restful.params_error(message="当前数据集无此文件!")
        dataid = file.dataid
        db.session.delete(file)
    db.session.commit()
    files = File.query.filter_by(dataid=dataid).all()
    f_list = [f.to_dict() for f in files]
    return restful.ok(data={"files": f_list})


@bp.route('/creategraph/select', methods=['POST'])
def creategraph_select():
    dataid = request.form.get("dataid")
    if not dataid:
        return restful.params_error(message="没有传入id！")
    try:
        dataset = DataSet.query.get(dataid)
        files = dataset.files
    except Exception as e:
        return restful.params_error(message="此数据集无文件")
    file_list = [f.filename for f in files]
    return restful.ok(data={"file_list": file_list})

@bp.get('/creategraph')
def creategraph():
    d = DataSet.query.all()
    dataset = [x.to_dict() for x in d]
    return restful.ok(data = {"dataset":dataset})

@bp.route('/creategraph/file', methods=['POST'])
def creategraph_file():
    dataid = request.form.get("dataid")
    files = File.query.filter_by(dataid=dataid).all()
    f_list = [f.to_dict() for f in files]
    return restful.ok(data={"files": f_list})



@bp.route('/creategraph/extract', methods=['POST'])
def creategraph_extract():
    s_list = []
    for (key, value) in request.form.items():
        file = File.query.get(value)
        s = []
        with open(file.filepath, 'r', encoding="utf-8") as file:
            data = file.read()
        s = data.split('。')
        s_list.extend(s)
    ans = []
    for sentence in s_list:
        if(len(sentence) <= 1):
            continue
        requestData = {"data": [sentence], "modelname": "bert_crf_klg"}
        headers = {'content-type': "application/json"}
        res_result = requests.post('http://59.73.128.14:5000/relation', data=json.dumps(requestData)
                                   , headers=headers)
        res_json = res_result.json()
        res_triples = res_json['result'].get('rels')
        if(res_triples):
            ans.extend(res_triples)
    #去重
    ans = [dict(t) for t in {tuple(d.items()) for d in ans}]
    return restful.ok(data={"list":ans})

@bp.route('/creategraph/submit')
def creategraph_submit():
    form = request.form
    graphname = form['graphname']
    graphdescription = form['graphdescription']
    graph = Graph(graphname=graphname,graphdescription=graphdescription,
                  entitycount=0,linkcount=0,eventcount=0)
    db.session.add(graph)
    db.session.commit()
    return restful.ok()


@bp.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.userpwd.data
        user = User.query.filter_by(username=username).first()
        if not user:
            return restful.params_error("账号或者密码错误!")
        if password != user.userpwd:
            return restful.params_error("账号或者密码错误!")
        token = create_access_token(identity=user.userid)
        session['user_id'] = user.userid
        return restful.ok(data={"token": token, "user": user.to_dict()})
    else:
        return restful.params_error(message=form.messages[0])

@bp.route('/logout')
def logout():
    session.clear()
    return restful.ok(message="退出登录成功!")
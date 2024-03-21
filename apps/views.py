from flask import Blueprint, request, session, redirect
from utils import restful
from flask_jwt_extended import create_access_token
from models.auth import User
from models.graph import Graph, GraphCount, DataSet
from .forms import LoginForm, DataSetAddForm, DataSetEditForm
from exts import db

bp = Blueprint('graph', __name__, url_prefix='/')

@bp.route('/')
def index():
    graph = Graph.query.all()
    graphcnt = GraphCount.query.first()
    g_list = []
    for x in graph:
        g_list.append(x.to_dict())
    return restful.ok(data={'graphs': g_list, 'graphcnt': graphcnt.to_dict()})

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
    db.session.delete(graph)
    db.session.commit()
    graph_list = Graph.query.all()
    g_list = [x.to_dict() for x in graph_list]
    return restful.ok(data={'graphcnt': graphcnt.to_dict(), 'g_list': g_list})

@bp.get('/databag')
def databag():
    dataset = DataSet.query.order_by(DataSet.createtime.desc()).all()
    d_list = [d.to_dict() for d in dataset]
    return restful.ok(data=d_list)

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
    try:
        dataset = DataSet.query.filter_by(dataname=dataname).all()
    except Exception as e:
        return restful.params_error(message="此数据集不存在！")
    d_list = [d.to_dict() for d in dataset]
    return restful.ok(data={"databag_list": d_list})

@bp.get('/creategraph')
def creategraph():
    dataset = DataSet.query.all()
    d_list = [d.to_dict() for d in dataset]
    return restful.ok(data={"databag_list": d_list})



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
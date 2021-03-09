from flask import render_template, request, session
from flask_security import login_required
from werkzeug.utils import secure_filename
from sqlalchemy.orm.session import make_transient
from sqlalchemy import or_
import os
import json
import uuid
import base64
import hashlib
import sys
from datetime import datetime
import textwrap

from .  import provision
from .. import db
from .. model import *
from .. modes import *
from .. mplogger import *
from .. mputil import *
from .. aws import *

'''
	-------------------------------------------------
	Tasks
	-------------------------------------------------
'''

@provision.route('/tasks')
@login_required
def tasks():

	columns = [('tuuid','Task ID',0),('primary_suuid','Software ID',0),('name','Name',1),('active','Active',1),
			   ('scope','Scope',1),('sw_start_datetime','Valid From',1),('sw_end_datetime','Valid To',1),('mdate','Mod Date',0)]
	colsForQuery = ['tuuid','primary_suuid','name','active','scope','sw_start_datetime','sw_end_datetime','mdate']

	qSWTasks = MpProvisionTask.query.order_by(MpProvisionTask.mdate.desc()).all()
	_data = []
	for d in qSWTasks:
		row = {}
		for c in colsForQuery:

			if c in ('sw_start_datetime','sw_end_datetime','mdate'):
				dt_obj = eval("d."+c)
				if dt_obj:
					row[c] = eval("d."+c).strftime("%Y-%m-%d %H:%M:%S")
			elif c == 'active':
				_a = eval("d."+c)
				row[c] = "Yes" if _a == 1 else "No"
			elif c == 'scope':
				_a = eval("d."+c)
				row[c] = "Production" if _a == 1 else "QA"
			else:
				row[c] = eval("d."+c)

		_data.append(row)

	_columns = []
	for c, t, v in columns:
			row = {}
			row['field'] = c
			row['title'] = t
			row['sortable'] = True
			if v == 0:
				row['visible'] = False

			_columns.append(row)

	return render_template('provision/software_tasks.html', data={'rows':_data,'columns': _columns}, isAdmin=True)

@provision.route('/task/edit/<id>')
@login_required
def taskEdit(id):

	mpst = MpProvisionTask.query.filter(MpProvisionTask.tuuid == id).first()
	mps = MpSoftware.query.filter( (MpSoftware.sState == 2) | (MpSoftware.sState == 3) ).order_by(MpSoftware.sName.asc()).all()
	_data = {}
	_swPkgs = []
	for s in mps:
		_swPkgs.append((s.suuid,s.sName,s.sVersion))

	_data["Task"] = mpst.asDict
	_data["SoftwareList"] = _swPkgs

	return render_template('provision/software_task_modify.html', data=_data, type='edit', isAdmin=True)

@provision.route('/task/new')
@login_required
def taskNew():

	_data = {}
	mps = MpSoftware.query.all()

	_swPkgs = []
	for s in mps:
		_swPkgs.append((s.suuid,s.sName,s.sVersion))

	_data["Task"] = {}
	_data["SoftwareList"] = _swPkgs
	_data["NEWID"] = str(uuid.uuid4())

	return render_template('provision/software_task_modify.html', data=_data, type='new', isAdmin=True)

''' AJAX Request '''
@provision.route('/task/save/<id>', methods=['POST'])
@login_required
def taskSave(id):
	_form = request.form.to_dict()

	_isNewTask=False
	_task = MpProvisionTask.query.filter(MpProvisionTask.tuuid == _form['tuuid']).first()
	if _task is None:
		_isNewTask=True
		_task = MpProvisionTask()

	for key, value in list(_form.items()):
		setattr(_task, key, value)

	setattr(_task, 'mdate', datetime.now())

	if _isNewTask:
		db.session.add(_task)

	db.session.commit()
	return json.dumps({'error':0}), 201

''' AJAX Method '''
@provision.route('/task/generate/<id>', methods=['POST'])
def generateTask(id):

	qSW = MpSoftware.query.filter(MpSoftware.suuid == id).first()
	if qSW is not None:
		_tuuid = str(uuid.uuid4())
		_swTask = MpProvisionTask()
		setattr(_swTask, 'tuuid', _tuuid)
		setattr(_swTask, 'name', qSW.sName)
		setattr(_swTask, 'primary_suuid', id)
		setattr(_swTask, 'active', 0)
		setattr(_swTask, 'scope', 0)
		setattr(_swTask, 'sw_start_datetime', datetime.now())
		setattr(_swTask, 'sw_end_datetime', datetime.now())
		setattr(_swTask, 'cdate', datetime.now())
		setattr(_swTask, 'mdate', datetime.now())
		db.session.add(_swTask)
		db.session.commit()
		return json.dumps({'error':0}), 201

	return json.dumps({'error':1,'errormsg':'Software package not found.'}), 404

'''
	-------------------------------------------------
	Scripts
	-------------------------------------------------
'''

@provision.route('/scripts')
@login_required
def scripts():

	columns = [('sid','Script ID',0),('name','Name',1),('script','Script',1),('active','Active',1),
			   ('scope','Scope',1),('type','Type',1),('order','Order',1), ('sw_start_datetime','Valid From',0),
			   ('sw_end_datetime','Valid To',0),('mdate','Mod Date',0)]
	colsForQuery = ['sid','name','script','active','scope','type','order','sw_start_datetime','sw_end_datetime','mdate']

	qScripts = MpProvisionScript.query.order_by(MpProvisionScript.mdate.desc()).all()
	_data = []
	for d in qScripts:
		row = {}
		for c in colsForQuery:

			if c in ('sw_start_datetime','sw_end_datetime','mdate'):
				dt_obj = eval("d."+c)
				if dt_obj:
					row[c] = eval("d."+c).strftime("%Y-%m-%d %H:%M:%S")
			elif c == 'active':
				_a = eval("d."+c)
				row[c] = "Yes" if _a == 1 else "No"
			elif c == 'scope':
				_a = eval("d."+c)
				row[c] = "Production" if _a == 1 else "QA"
			elif c == 'type':
				_a = eval("d."+c)
				row[c] = "Post Software Task Install" if _a == 1 else "Pre Software Task Install"
			elif c == 'script':
				_a = eval("d." + c)
				row[c] = (_a[:10] + '...') if len(_a) > 10 else _a
			else:
				row[c] = eval("d."+c)

		_data.append(row)

	_columns = []
	for c, t, v in columns:
			row = {}
			row['field'] = c
			row['title'] = t
			row['sortable'] = True
			if v == 0:
				row['visible'] = False

			_columns.append(row)

	return render_template('provision/scripts.html', data={'rows':_data,'columns': _columns}, isAdmin=True)

@provision.route('/script/edit/<id>')
@login_required
def scriptEdit(id):
	_data = {}
	mpst = MpProvisionScript.query.filter(MpProvisionScript.sid == id).first()
	_data["Script"] = mpst.asDict

	return render_template('provision/script_modify.html', data=_data, type='edit', isAdmin=True)

@provision.route('/script/new')
@login_required
def scriptNew():

	_data = {}
	_data["Script"] = {}
	_data["NEWID"] = str(uuid.uuid4())

	return render_template('provision/script_modify.html', data=_data, type='new', isAdmin=True)

''' AJAX Request '''
@provision.route('/script/save/<id>', methods=['POST'])
@login_required
def scriptSave(id):
	_form = request.form.to_dict()
	_isNew=False

	_script = MpProvisionScript.query.filter(MpProvisionScript.sid == _form['sid']).first()
	if _script is None:
		_isNew=True
		_script = MpProvisionScript()

	for key, value in list(_form.items()):
		setattr(_script, key, value)

	setattr(_script, 'mdate', datetime.now())

	if _isNew:
		db.session.add(_script)

	db.session.commit()
	return json.dumps({'error':0}), 201

''' AJAX Request '''
@provision.route('/script/remove', methods=['DELETE'])
@login_required
def scriptRemove():
	_form = request.form.to_dict()


	if 'sids' in _form:
		for s in _form['sids'].split(","):
			_script = MpProvisionScript.query.filter(MpProvisionScript.sid == s).first()
			if _script is not None:
				log_Info("Delete provisioning script %s" % (_script.name))
				MpProvisionScript.query.filter(MpProvisionScript.sid == s).delete()
				db.session.commit()

	return json.dumps({'error':0}), 201

@provision.route('/ui/config')
@login_required
def uiConfig():

	_data = {'script':''}
	qGet = MpProvisionConfig.query.filter(MpProvisionConfig.active == 1).first()
	if qGet is not None:
		rawData = qGet.config
		script = base64.b64decode(rawData.encode('utf-8'))
		_data['script'] = script.decode("utf-8")

	return render_template('provision/ui_config.html', data=_data, isAdmin=True)

''' AJAX Request '''
@provision.route('/ui/config/upload',methods=['POST'])
def uiConfigUpload():
	# Get Patch ID
	try:
		req = request

		# Check Permissions
		if not localAdmin() and not adminRole():
			log_Error("{} does not have permission to change custom patch {}.".format(session.get('user'), puuid))
			return {'data': {}}, 403

		# Save File, returns path to file
		_file = None
		_fileData = None
		_fileDataB64 = 'None'
		# MpProvisionConfig
		if 'file' not in request.files:
			return {'errorno': 404, 'errormsg': 'Error, upload file not found.', 'result': {}}, 404
		if "file" in request.files:
			_file = request.files['file']
			_fileName = _file.filename
			if _fileName == '':
				return {'errorno': 403, 'errormsg': 'Error, upload file is blank.', 'result': {}}, 403
			if allowed_file(_fileName):
				_fileData = _file.read()
				# print(_fileData.decode("utf-8"))

				qGet = MpProvisionConfig.query.filter(MpProvisionConfig.active == 1).first()
				if qGet is not None:
					setattr(qGet, 'active', 0)
					#db.session.commit()

				mpc = MpProvisionConfig()
				setattr(mpc, 'configName', _fileName)
				setattr(mpc, 'config', base64.b64encode(_fileData))
				setattr(mpc, 'mdate', datetime.now())
				db.session.add(mpc)
				db.session.commit()



	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		log_Error('Message: %s' % (e))
		return {'errorno': 500, 'errormsg': e, 'result': {}}, 500

	return {'data': {}}, 200

def allowed_file(filename):
	extensions = ['json']
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@provision.route('/test')
@login_required
def testTask():

	_data = {}
	mps = MpSoftware.query.filter(MpSoftware.sState == 2).all()

	_swPkgs = []
	for s in mps:
		_swPkgs.append((s.suuid, s.sName, s.sVersion))

	_data["SoftwareList"] = _swPkgs

	return render_template('provision/test.html', data=_data, isAdmin=True)

@provision.route('/criteria')
@login_required
def criteria():
	cList = MpProvisionCriteria.query.order_by(MpProvisionCriteria.order.asc()).all()
	cListCols = MpProvisionCriteria.__table__.columns
	cListColsLimited = ['rid', 'type', 'type_data', 'order', 'active', 'mdate']

	return render_template('provision/criteria.html', data={}, columns=cListColsLimited, columnsAll=cListCols)

''' AJAX Request '''
@provision.route('/criteria/list', methods=['GET'])
@login_required
def criteriaList():
	_results = []
	pc = MpProvisionCriteria.query.all()

	colNames = [{'name': 'cuuid', 'label': 'CUUID'}, {'name': 'client_group', 'label': 'Client Group'},
				{'name': 'hostname', 'label': 'Host Name'}, {'name': 'computername', 'label': 'Computer Name'},
				{'name': 'addomain', 'label': 'AD-Domain'}, {'name': 'addn', 'label': 'AD-DistinguishedName'},
				{'name': 'ipaddr', 'label': 'IP Address'}, {'name': 'macaddr', 'label': 'MAC Address'},
				{'name': 'serialno', 'label': 'Serial No'}, {'name': 'fileVaultStatus', 'label': 'FileVault'},
				{'name': 'firmwareStatus', 'label': 'Firmware'}, {'name': 'osver', 'label': 'OS Ver'},
				{'name': 'consoleuser', 'label': 'Console User'}, {'name': 'needsreboot', 'label': 'Needs Reboot'},
				{'name': 'client_version', 'label': 'Client Ver'},
				{'name': 'hasPausedPatching', 'label': 'Paused Patching'},
				{'name': 'mdate', 'label': 'Mod Date'}]

	_groups = []

	for c in pc:
		_dict = c.asDict
		_dict['rid'] = c.rid
		_results.append(_dict)

	return json.dumps(_results, default=json_serial), 200

@provision.route('/criteria/add')
@login_required
def criteriaAdd():
	return render_template('provision/criteriaAdd.html', data={})

@provision.route('/criteria/edit/<id>')
@login_required
def criteriaEdit(id):
	_data = {}
	pc = MpProvisionCriteria.query.filter(MpProvisionCriteria.rid == id).first()
	if pc is not None:
		_data = pc.asDict
		_data['rid'] = pc.rid

	return render_template('provision/criteriaAdd.html', data=_data)

''' AJAX Request '''
@provision.route('/criteria/save', methods=['POST'])
@login_required
def criteriaSave():
	_form = request.form.to_dict()
	_isNew = False

	if _form['rid'] == 'NA':
		_isNew = True
		pc = MpProvisionCriteria()
	else:
		pc = MpProvisionCriteria.query.filter(MpProvisionCriteria.rid == _form['rid']).first()
		if pc is None:
			_isNew = True
			pc = MpProvisionCriteria()

	for key, value in list(_form.items()):
		if key == 'rid':
			continue
		else:
			setattr(pc, key, value)

	setattr(pc, 'mdate', datetime.now())

	if _isNew:
		db.session.add(pc)

	db.session.commit()
	return json.dumps({'error': 0}), 201


''' AJAX Request '''
@provision.route('/criteria/active', methods=['POST'])
@login_required
def criteriaActive():
	_form = request.form.to_dict()
	pc = MpProvisionCriteria.query.filter(MpProvisionCriteria.rid == _form['pk']).first()
	if pc is not None:
		setattr(pc, 'active', _form['value'])
		setattr(pc, 'mdate', datetime.now())
		db.session.commit()

	return json.dumps({'error': 0}), 201

''' AJAX Request '''
@provision.route('/criteria/order', methods=['POST'])
@login_required
def criteriaOrder():
	_form = request.form.to_dict()
	pc = MpProvisionCriteria.query.filter(MpProvisionCriteria.rid == _form['pk']).first()
	if pc is not None:
		if _form['value'].isnumeric():
			setattr(pc, 'order', _form['value'])
			setattr(pc, 'mdate', datetime.now())
			db.session.commit()
		else:
			return json.dumps("Must be a number."), 409

	return json.dumps({'error': 0}), 201

''' AJAX Request '''
@provision.route('/criteria/delete', methods=['DELETE'])
@login_required
def criteriaDelete():
	_form = request.form.to_dict()
	_rids = []
	if 'rid' in _form:
		_rids = _form['rid'].split(",")

	if len(_rids) >= 1:
		for r in _rids:
			MpProvisionCriteria.query.filter(MpProvisionCriteria.rid == r).delete()

		db.session.commit()

	return json.dumps({'error': 0}), 201

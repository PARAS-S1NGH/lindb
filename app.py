import ctypes
from flask import Flask, render_template, json, request, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'sql9172792'
app.config['MYSQL_DATABASE_PASSWORD'] = 'lsNZJs2Dc4'
app.config['MYSQL_DATABASE_DB'] = 'sql9172792'
app.config['MYSQL_DATABASE_HOST'] = 'sql9.freesqldatabase.com'
mysql.init_app(app)

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

@app.route("/")
def main():
    return render_template('index.html')

# @app.route('/test')
# def test():
#     username = request.args.get('UserName')
#     password = request.args.get('Password')
#     cursor = mysql.connect().cursor()
#     cursor.execute("SELECT * from Bundle")
#     data = cursor.fetchone()
#     if data is None:
#         return "none"
#     else:
#         return "found a tuple"

# this maybe for later use
#@app.route('/showSignUp')
#def showSignUp():
#    return render_template('signup.html')

@app.route('/showAddPatient')
def showAddPatient():
    return render_template('addPatient.html')

@app.route('/addPatient', methods=['POST'])
def addPatient():
    try:
        # read the posted values from the UI
        _fname = request.form['inputFirstName']
        _lname = request.form['inputLastName']
        _dob = request.form['inputDOB']

        # validate the received values
        if _fname and _lname and _dob:
            
            # all good, let's insert

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('addPatient',(_fname,_lname,_dob))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Patient added successfully'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'message':'Enter all required fields'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showAddOperation', methods=['GET'])
def showAddOperation():
    return render_template('addOperation.html')

@app.route('/addOperation', methods=['POST'])
def addOperation():
    try:
        # read the posted values from the UI
        _sfname = request.form['sFirstName']
        _slname = request.form['sLastName']
        _pfname = request.form['pFirstName']
        _plname = request.form['pLastName']
        _bundle = request.form['bundleName']
        _opdate = request.form['opDate']

        # validate the received values
        if _sfname and _slname and _pfname and _plname and _bundle and _opdate:
            
            # all good, let's insert

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('addOperation',(_sfname,_slname,_pfname,_plname,_bundle,_opdate))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Added new operation'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

# @app.route('/getSurgeons',methods=['POST'])
# def addOperation():
#     try:

#         # conn = mysql.connect()
#         # cursor = conn.cursor()

#         # cursor.execute("SELECT patientID FROM Patients")
#         # patients = cursor.fetchall()
#         # cursor.execute("SELECT surgeonID FROM Surgeons")
#         # surgeons = cursor.fetchall()
#         # cursor.execute("SELECT bundleName FROM Bundles")
#         # bundles = cursor.fetchall()
    
#         conn = mysql.connect()
#         cursor = conn.cursor()

#         cursor.callproc("select * from Surgeons")
#         result = cursor.fetchall()

#         surgeons = []
#         surgeons.append({'Id':result[0][0],'First Name':result[0][1],'Last Name':result[0][2]})

#         return json.dumps(surgeons)
        
#     except Exception as e:
#         return json.dumps({'error':str(e)})
#     finally:
#         cursor.close()
#         conn.close()

#     return render_template('addOperation.html', patients=patients)
@app.route('/searchProcedures')
def searchProcedures():
	return render_template('searchProcedures.html')

@app.route('/getProcedures', methods=['POST'])
def getProcedures():
	try:
		# read the posted values from the UI
		_searchField = request.form['searchField']

		conn = mysql.connect()
		cursor = conn.cursor()
		
		cursor.execute("SELECT bundleName FROM Procedures WHERE procName='" + _searchField + "'")
		
		data = cursor.fetchall()

		return jsonify(data)
        
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()

@app.route('/searchBundles')
def searchBundles():
	return render_template('searchBundles.html')

@app.route('/getBundles', methods=['POST'])
def getBundles():
	try:
		# read the posted values from the UI
		_searchField = request.form['searchField']

		conn = mysql.connect()
		cursor = conn.cursor()
		
		cursor.execute("SELECT procName FROM Procedures WHERE bundleName='" + _searchField + "'")
		
		data = cursor.fetchall()

		return jsonify(data)
        
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()

@app.route('/searchOperations')
def searchOperations():
	return render_template('searchOperations.html')

@app.route('/getOperations', methods=['POST'])
def getOperations():
    try:

        # read the posted values from the UI
        _searchCN = request.form['searchCaseNo']
        _searchSN = request.form['searchSurgeonName']
        _searchPN = request.form['searchPatientName']
        _searchD = request.form['searchDate']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        count = 0
        where_stmt = " WHERE 1=1 "
        
        if request.form.get('caseNum'):
            count = count+1
            where_stmt +=  "AND caseNumber='" + _searchCN + "' "
            
        if request.form.get('docName'):
            count = count+1
            mylist = _searchSN.split(' ')
            cursor.execute("SELECT surgeonID FROM Surgeons WHERE firstName=\"" +
                mylist[0] + "\" AND lastName=\"" + mylist[1] + "\"")
            sid = cursor.fetchall()
            where_stmt +=  "AND surgeonID='" + str(sid[0][0]) + "' "
            
        if request.form.get('patName'):
            count = count+1
            mylist = _searchPN.split(' ')
            cursor.execute("SELECT patientID FROM Patients WHERE firstName=\"" +
                mylist[0] + "\" AND lastName=\"" + mylist[1] + "\"")
            pid = cursor.fetchall()
            where_stmt +=  "AND patientID='" + str(pid[0][0]) + "' "
            
        if request.form.get('dateOp'):
            count = count+1
            where_stmt +=  "AND operationDate='" + _searchD + "' "
            
        if count > 0:
            cursor.execute("SELECT * FROM Operations" + where_stmt)
        else:
            cursor.execute("SELECT * FROM Operations")
        
        data = cursor.fetchall()
        
        return jsonify(data)
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showAddProcedure')
def showAddProcedure():
    return render_template('addProcedure.html', showProcedureInfo())
	
def showProcedureInfo():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		
		cursor.execute("SELECT procName, ValueID, procName FROM")
		
		data = cursor.fetchall()

		return jsonify(data)
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		cursor.close()
		conn.close()
		showProcedureInfo()

@app.route('/addProcedure', methods=['POST'])
def addProcedure():
    try:
        # read the posted values from the UI
        _pname = request.form['pname']
        _bname = request.form['bname']

        # validate the received values
        if _pname and _bname:
            
            # all good, let's insert

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('addProcedure',(_pname,_bname))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Procedure added successfully'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'message':'Enter all required fields'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/showAddProcedureValue')
def showAddProcedureValue():
    return render_template('addValue.html')	

@app.route('/addValue', methods=['POST'])
def addValue():
    try:
        # read the posted values from the UI
        _pname = request.form['pname']
        _val = request.form['val']
        _desp = request.form['desp']

        # validate the received values
        if _pname and _val and _desp:
            
            # all good, let's insert

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('addValue',(_val,_desp,_pname))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #show page again if user wants to continue
                #if request.form.get('cont'):
                 #   return render_template('addValue.html')
                return json.dumps({'message':'Value added successfully'})
            else:
                return json.dumps({'error':str(data[0])})

        else:
            return json.dumps({'message':'Enter all required fields'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
@app.route('/showAddBundle')
def showAddBundle():
    return render_template('addBundle.html')

@app.route('/addBundle', methods=['POST'])
def addBundle():
    try:
        # read the posted values from the UI
        _bname = request.form['bname']

        # validate the received values
        if _bname:
            
            # all good, let's insert

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute('INSERT INTO Bundles (bundleName) VALUES (\''+_bname+'\');')
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'Bundle added successfully'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'message':'Enter all required fields'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
	
@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # all good, let's insert

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('sp_createUser',(_name,_email,_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()
        
@app.route('/searchSurgeon')
def searchSurgeon():
	return render_template('searchSurgeon.html')

@app.route('/getSurgeon', methods=['POST'])
def getSurgeon():
    try:

        # read the posted values from the UI
        _searchSN = request.form['searchSurgeonName']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        
        count = 0
        where_stmt = " WHERE 1=1 "
        
            
        if request.form.get('docName'):
            count = count+1
            mylist = _searchSN.split(' ')
            cursor.execute("SELECT surgeonID FROM Surgeons WHERE firstName=\"" +
                mylist[0] + "\" AND lastName=\"" + mylist[1] + "\"")
            sid = cursor.fetchall()
            # where_stmt +=  "AND surgeonID='" + str(sid[0][0]) + "' "

            
        if count > 0:
            cursor.execute("SELECT * FROM Operations WHERE surgeonID=\""+str(sid[0][0])+"\"")
        else:
            cursor.execute("SELECT * FROM Operations")
        
        data = cursor.fetchall()
        
        return jsonify(data)
        
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run()


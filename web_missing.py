from flask import Flask, jsonify, request
import Missing

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/missing',methods=['GET'])
def missing():
    #print( request.args)
    solarFname = request.args.get('solar')
    stealthFname = request.args.get('stealth')
    solarD, stealthIPs = Missing.load(solarFname, stealthFname)
    missing = Missing.find_missing(solarD,stealthIPs)
    reportL = Missing.report(solarD,missing)
    reportS = '<pre>'+'\n'.join(reportL)+'</pre>'
    return reportS

if __name__ == '__main__':
    app.run(debug=True)

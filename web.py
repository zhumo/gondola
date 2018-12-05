import BaseHTTPServer
import threading
import urlparse

exposed_functions = []

def handle_get(path, postvars={}):
    # Construct and send basic HTTP to the client
    # Preamble
    output = 'HTTP/1.0 200 OK\r\n'
    output += 'Content-Type: text/html\r\n\r\n'
    #print postvars
    for exposed_function in exposed_functions:
        if exposed_function['function']!=None and exposed_function['arguments']!=None and "/"+exposed_function['function'].__name__==path:
            return_value = None
            #print len(exposed_function['arguments'])
            if len(exposed_function['arguments'])==0:
                return_value = exposed_function['function']()
            elif len(exposed_function['arguments'])==1:
                return_value = exposed_function['function'](postvars[exposed_function['arguments'][0]] )
            elif len(exposed_function['arguments'])==2:
                return_value = exposed_function['function'](postvars[exposed_function['arguments'][0]], postvars[exposed_function['arguments'][1]] )
            elif len(exposed_function['arguments'])==3:
                return_value = exposed_function['function'](postvars[exposed_function['arguments'][0]], postvars[exposed_function['arguments'][1]], postvars[exposed_function['arguments'][2]] )
            elif len(exposed_function['arguments'])==4:
                return_value = exposed_function['function'](postvars[exposed_function['arguments'][0]], postvars[exposed_function['arguments'][1]], postvars[exposed_function['arguments'][2]], postvars[exposed_function['arguments'][3]] )
            if return_value!=None:
                output += str(return_value)

    # Beginning of html
    if path=="/":
        output += '<html>\n'
        output += '<head>\n'
        output += '<title>Raspberry Pi Web Control</title>\n'
        output += '<script>function getElementsStartsWithId( id ) {var children = document.body.getElementsByTagName("*");var elements = [], child;for (var i = 0, length = children.length; i < length; i++) {child = children[i];if (child.id.substr(0, id.length) == id)elements.push(child);}return elements;}</script>'
        output += '<script>function ajax_call(path) {var elements=getElementsStartsWithId(path+"_arg_");data="";for(i=0;i<elements.length;i++){data+=elements[i].id+"="+elements[i].value+"&"};data=data.slice(0,-1);var xhttp=new XMLHttpRequest();xhttp.open("POST", path, true);xhttp.onload=function(e){if(xhttp.readyState==4){if(xhttp.status==200){document.getElementById("status").innerHTML=xhttp.responseText;} else {console.error(xhttp.statusText);}}};xhttp.onError=function(e){console.error(xhttp.statusText);};xhttp.send(data); }</script>\n'
        output += '<script>function draw_gcode(t,a){var s=a.getContext("2d");s.clearRect(0,0,a.width,a.height),t=t.split("\\n");for(var e=0,l=0,r=0;r<t.length;r++){_=(_=t[r]).split(" "),X=!1,Y=!1;for(var i=0;i<_.length;i++){item=_[i];var o=item.substring(0,1),g=item.substring(1);"X"==o?X=parseFloat(g):"Y"==o&&(Y=parseFloat(g))}!1!==X&&X>e&&(e=X),!1!==Y&&Y>l&&(l=Y)}var n=a.width/e,h=a.height/l;last_X=!1,last_Y=!1,last_Z=!1;for(r=0;r<t.length;r++){var _;_=(_=t[r]).split(" "),X=!1,Y=!1,Z=!1;for(i=0;i<_.length;i++){item=_[i];o=item.substring(0,1),g=item.substring(1);"X"==o?X=parseFloat(g):"Y"==o?Y=parseFloat(g):"Z"==o&&(Z=parseFloat(g))}!1!==X&&!1!==Y&&(X*=n,Y=a.height-Y*h,!1!==last_X&&!1!==last_Y&&-.125==last_Z&&(s.beginPath(),s.moveTo(last_X,last_Y),s.lineTo(X,Y),s.stroke()),last_X=X,last_Y=Y),!1!==Z&&(last_Z=Z)}}</script>' ;
        output += '<script>function gcode_to_turtle(t){var a="pen_up()\\n";t=t.split("\\n");for(var e=0,s=0,l=0;l<t.length;l++){i=(i=t[l]).split(" "),X=!1,Y=!1;for(var n=0;n<i.length;n++){item=i[n];var _=item.substring(0,1),o=item.substring(1);"X"==_?X=parseFloat(o):"Y"==_&&(Y=parseFloat(o))}!1!==X&&X>e&&(e=X),!1!==Y&&Y>s&&(s=Y)}var r=100/e,g=100/s;last_X=!1,last_Y=!1,last_Z=!1;for(l=0;l<t.length;l++){var i;i=(i=t[l]).split(" "),X=!1,Y=!1,Z=!1;for(n=0;n<i.length;n++){item=i[n];_=item.substring(0,1),o=item.substring(1);"X"==_?X=parseFloat(o):"Y"==_?Y=parseFloat(o):"Z"==_&&(Z=parseFloat(o))}!1!==X&&!1!==Y&&(X=X*r/2+25,Y=Y*g/2+25,a+="go_to( "+X+", "+Y+" )\\n",last_X=X,last_Y=Y),!1!==Z&&Z!=last_Z&&(!1!==last_Z&&(Z>last_Z?a+="pen_up()\\n":Z<last_Z&&(a+="pen_down()\\n")),last_Z=Z)}document.getElementById("parse_go_to_code_arg_0").value=a,draw_go_to_code(a,document.getElementById("canvas"))}</script>' ;
        output += '<script>function draw_go_to_code(o,t){var r=t.getContext("2d");r.clearRect(0,0,t.width,t.height),o=(o=(o=o.replace(" ","")).toLowerCase()).split("\\n");for(var a=0,_=0,m=0;m<o.length;m++){2==(s=(s=o[m]).split("(")).length&&(command=s[0],params=s[1].replace(")","").split(","),"go_to"==command&&(X=!1,Y=!1,void 0!==params[0]&&(X=parseFloat(params[0])),void 0!==params[1]&&(Y=parseFloat(params[1])),!1!==X&&X>a&&(a=X),!1!==Y&&Y>_&&(_=Y)))}a<t.width&&(a=100),_<t.height&&(_=100);var e=t.width/a,p=t.height/_,i=!1;from_X=!1,from_Y=!1;for(m=0;m<o.length;m++){var s;2==(s=(s=o[m]).split("(")).length&&(command=s[0],params=s[1].replace(")","").split(","),"go_to"==command&&(!1===from_X&&(from_X=50),!1===from_Y&&(from_Y=50),to_X=!1,to_Y=!1,void 0!==params[0]&&(to_X=parseFloat(params[0])),void 0!==params[1]&&(to_Y=parseFloat(params[1])),!1!==from_X&&!1!==from_Y&&!1!==to_X&&!1!==to_Y&&(to_X_orig=to_X,to_Y_orig=to_Y,from_X*=e,from_Y=t.height-from_Y*p,to_X*=e,to_Y=t.height-to_Y*p,!0===i&&(r.beginPath(),r.moveTo(from_X,from_Y),r.lineTo(to_X,to_Y),r.stroke()),from_X=to_X_orig,from_Y=to_Y_orig)),"pen_up"==command&&(i=!1),"pen_down"==command&&(i=!0))}}</script>' ;
        output += '</head>\n'
        # Beginning of body
        output += '<body>\n'
        for exposed_function in exposed_functions:
            output += exposed_function['html'] + '\n'
        #output += '<h1>Current LED is: %s </h1>\n' % (state)
        #output += '<a href="/%s">Turn LED %s</a>\n' % (opp_state, opp_state)
        # End of body and html
        output += '<div id="status_wrapper" style="padding:10px;"><pre>Result:<div id="status"></div></pre></div>\n'
        output += '</body>\n'
        output += '</html>\n'
    return output

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        output = handle_get(s.path)
        s.wfile.write(output)
    def do_POST(s):
        postvars = {}
        for key,value in dict(urlparse.parse_qs(s.rfile.read(int(s.headers['Content-Length'])))).items():
            postvars[key] = value[0]
        output = handle_get(s.path, postvars)
        s.wfile.write(output)

# Listen on all IP addresses, using tcp port 5005
host, port = '0.0.0.0', 5005

# Instantiate the server object and handler
server = BaseHTTPServer.HTTPServer((host, port), MyHandler)

server_thread = threading.Thread( target=server.serve_forever)
server_thread.daemon = True


def arbitrary_html( html ):
    exposed_functions.append( {'html':html, 'function':None, 'arguments':None} )


def register( html, function ):
    button_index = html.lower().find( "<button" )
    if button_index!=-1:
        html = html[:button_index] + "<button onClick=\"ajax_call('"+function.__name__+"');\" " + html[button_index+7:]

    arguments = []
    offset = 0
    input_index = html.lower().find( "<input", offset )
    while input_index!=-1:
        argument_id = function.__name__ + "_arg_" + str(offset) ;
        html = html[:input_index] + "<input id=\"" + argument_id + "\" " + html[input_index+6:]
        arguments.append( argument_id )
        offset = input_index + 6
        input_index = html.lower().find( "<input", offset )

    input_index = html.lower().find( "<textarea", offset )
    while input_index!=-1:
        argument_id = function.__name__ + "_arg_" + str(offset) ;
        html = html[:input_index] + "<textarea id=\"" + argument_id + "\" " + html[input_index+6:]
        arguments.append( argument_id )
        offset = input_index + 9
        input_index = html.lower().find( "<textarea", offset )
    exposed_functions.append( {'html':html, 'function':function, 'arguments':arguments} )


def server_start():
    server_thread.start()
    print "> web server has been started"

def server_stop():
    server.shutdown()
    server.server_close()
    print "> web server has been stopped"

# -*- coding: latin1 -*-

#SwissLegalTech Hackathon 2018, Sep 17-19th, Zurich
#Team Mighty Bytes - Oceane, Ioannis, Andreas, Nico
#Designed and programmed in the backyard

import json
import socket
import pyramid
import waitress
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

import renderer

paconfigStr = """
ZH;  0;      0;       0;
ZH;  0.6;   1.2;    0.5;
AG;     0;       0;        0;
AG;     0.6;     1.8;      0;
AR;     0;       0;        0;
AR;  0.5;        1.2;      1;
AI;     0;       2;        0;
BL;     0;       0;        0;
BL;     0.6;     1.8;      3;
BS;     0;       2;        0;
BE;     0;       0;        0;
BE;     0.5;     1.2;      1;
BE;     3.5;     9999; 0;
FR;     0;       0;        0;
FR;     0.6;     1.2;      0; Lebhag muss mindestens alle 2 Jahre zurückgeschnitten werden
GE;     0;       0;        0;
GE;     0.5;     2;        2.666;
GE;     2;       6;        0.5;
GE;     5;       12;       0;
GL;     0;       1.2;      0; Grünhäge sollen, wenn der Anstösser es verlangt, jährlich ordentlich beschnitten werden
GR;     0;       0;        0;
GR;     0.5;     1.5;      1;
GR;     2.5;     9999; 0;
JU;     0;       0;        0;
JU;     0.5;     1.2;      1;
JU;     3.5;     9999; 0;
LU;     0;       0;        0;
LU;     0.5;     1;        0.5;
LU;     4;       9999; 0;
NE;     0;       0;        0;
NE;     1;       1.5;      0; Sofern es sich beim Nachbargrundstück um einen Garten handelt
NW; 0;1.5;0;
NW; 0.75;1.6;0.5;
NW; 1.5;3;0;
OW; 0;0;0;
OW; 0.3;1.2;0.1;
SH; 0;0;0;
SH; 0.6;1.2;0.5;
SZ; 0;1.2;0; jährlicher Rückschnitt
SZ; 0.5;2;0; für höhere Einfriedungen gilt der Grenzabstand des kantonalen Baugesetzes
SO; 0;2;0;
SO; 3;9999;0;
SG; 0;0;0;
SG; 0.45;1.2;0; jährlicher Rückschnitt
TI; 0;0;0;
TI; 0.5;1.25;0; jährlicher Rückschnitt, Maulbeerbaumhecke: 1 m Abstand zur Grenze, 2 m voneinander entfernt, Höhe maximal 2 50 m | Robinienhecke: siehe Gesetz
TG; 0;0;0.5;
UR; 0;0;0;
UR; 0.3;9999;0;
VD; 0;0;0,
VD; 0.5;2;0.666;)
VS; 0;0;0;
VS; 0.5;1;0.5;
ZG; 0;0;0;
ZG; 0.5;1;0.5;
"""

vfconfigStr = """
AG; 	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Gerichte gehen aber von einer Verjährungsfrist von 30 Jahren ab Pflanzung aus.
AR;	5; Der Anspruch auf Beseitigung verjährt 5 Jahre nach der Pflanzung.
AI;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
BL;	10; Der Anspruch auf Beseitigung verjährt 10 Jahre nach der Pflanzung.
BS;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
BE;	5; Der Anspruch auf Beseitigung verjährt 5 Jahre nach Pflanzung.
FR;	20; Der Anspruch auf Beseitigung verjährt 20 Jahre nach Pflanzung. Es sei denn die Bepflanzung wurde vor dem 1. Januar 2003 angelegt.
GE;	30; Der Anspruch auf Beseitigung verjährt 30 Jahre nach Pflanzung.
GL;	5; Der Anspruch auf Beseitigung verjährt 5 Jahre nach Pflanzung.
GR;	5; Der Anspruch auf Beseitigung verjährt 5 Jahre nach Pflanzung.
JU;	5; Der Anspruch auf Beseitigung verjährt 5 Jahre nach Pflanzung.
LU;	10; Der Anspruch auf Beseitigung verjährt 10 Jahre nach Pflanzung.
NE; 	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
NW;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
OW;	2; Der Anspruch auf Beseitigung verjährt 2 Jahre nach Pflanzung.
SH;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
SZ;	10; Der Anspruch auf Beseitigung verjährt 2 Jahre ab Kenntnis, jedoch spätestens 10 Jahren nach der Pflanzung.
SO;	3; Der Anspruch auf Beseitigung verjährt 3 Jahre nach Pflanzung.
SG;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
TI;	10; Der Anspruch auf Beseitigung verjährt 10 Jahre nach Pflanzung. Nach Ablauf der 10 Jahre muss die Entfernung entschädigt werden.
TG;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.
UR;	1; Der Anspruch auf Beseitigung verjährt nach 1 Jahr und beginnt, sobald erkennbar ist, dass die Pflanzen den vorgeschriebenen Grenzabstand unterschreiten werden.
VD;	10; Der Anspruch auf Beseitigung verjährt nach 10 Jahren. Nach Ablauf der 10 Jahre muss ein überwiegendes Interesse geltend gemacht werden.
VS;	5; Der Anspruch auf Beseitigung verjährt nach 5 Jahren ab Pflanzung oder bei überschrittener Höhe ab Ende des Jahres.
ZG;	5; Der Anspruch auf Beseitigung verjährt 5 Jahre nach Pflanzung.
ZH;	9999; Der Anspruch auf Beseitigung ist unverjährbar. Die Ausübung des Rechts kann eventuell rechtsmissbräuchlich sein.

"""

class PflanzAbstandEngine(object):
    def __init__(self, configStr):
        self.plfDict_ = {}
        self.__readConfig(configStr)

    def __readConfig(self, configStr):
        for l in configStr.splitlines():
            tuples = l.split(";")
            if len(tuples) != 5:
                if l.strip():
                    print("Pflanzabstand config has illegal length (!=5): %s" % l)
                continue
            canton, d, h, s, comment = map(lambda s: s.strip(), tuples)
            canton = canton.upper()
            if not canton in self.plfDict_:
                self.plfDict_[canton] = []
            self.plfDict_[canton].append((float(d), float(h), float(s), comment))
        print("Pflanzabstand configured.")
        for c in self.plfDict_:
            print(c),
            # Sort the piecewise linear function definition tuple list,
            # we rely on that in interpolation.
            self.plfDict_[c].sort()
            for piecewiseLinearTuple in self.plfDict_[c]:
                print ("\t%s\t%s\t%s\t%s" % piecewiseLinearTuple)

    def __interpolate(self, case_d, case_h, piecewiseLinearTupleList):
        # Return tuple (isLegal, maxAllowedHeight, comment)
        isLegal = False
        maxAllowedHeight = 999.0
        comment = 'interpolation error'        
        for d, h, s, cmt in piecewiseLinearTupleList:
            if case_d >= d:
                # This is applicable. It might be changed by later segments, though.
                maxAllowedHeight = h + s * (case_d - d)
                isLegal = case_h <= maxAllowedHeight
                comment = cmt
        return (isLegal, maxAllowedHeight, comment)

    def consult(self, canton, d, h):
        # Consult about a relevant case in canton, distance from
        # clients property d, height of hecke h.
        # Return dict with attributes.
        isLegal = False
        maxAllowedHeight = 999.0
        comment = 'Not yet implemented'
        canton = canton.upper()
        if canton in self.plfDict_:
            isLegal, maxAllowedHeight, comment = self.__interpolate(d, h, self.plfDict_[canton])
        res = {}
        # Input.
        res['canton'] = canton
        res['caseDistance'] = d
        res['caseHeight'] = h
        # Output.
        if not comment:
            comment = "keine"
        res['isLegal'] = isLegal
        res['maxAllowedHeight'] = maxAllowedHeight
        res['comment'] = comment
        return res

pflanzAbstandEngine = None

def flonar_planzabstand(canton, distance, height):
    global pflanzAbstandEngine
    if pflanzAbstandEngine is None:
        pflanzAbstandEngine = PflanzAbstandEngine(paconfigStr)
    rechtslage = pflanzAbstandEngine.consult(canton, distance, height)
    return json.dumps(rechtslage)

def flonar_usage(request):
    print(request.GET)
    return Response('Flonar usage: /flonar/pa/{canton}/{distance}/{height}')

def flonarpa_engine(request):
    if "canton" in request.matchdict:
        canton = '%(canton)s' % request.matchdict
        distanceStr = '%(distance)s' % request.matchdict
        heightStr = '%(height)s' % request.matchdict
    else:
        canton = request.GET['canton']
        distanceStr = request.GET['distance']
        heightStr = request.GET['height']
    distance = float(distanceStr)
    height = float(heightStr)
    rspj = flonar_planzabstand(canton, distance, height)
    rsp = json.loads(rspj)
    if rsp['isLegal']:
        bdy = renderer.Http("res/Tree_green_body.html", rsp)
    else:
        bdy = renderer.Http("res/Tree_red_body.html", rsp)
    return pyramid.response.Response(body=bdy.http)


def flonar_pa_form(request):
    return pyramid.response.FileResponse("res/flonar_dyn.html", request=request)

if __name__ == '__main__':
    # Engine startup test.
    print("Startuptest: %s" % flonar_planzabstand('ZH', 2.3, 2.0))
    print("Startuptest: %s" % flonar_planzabstand('TI', 0.4, 1.37))
    # Webserver start.
    with Configurator() as config:
        # Render main page.
        rd = {}
        rd['localhost'] = socket.gethostbyname(socket.gethostname())
        renderer.Page("res/ab.html", "res/flonar_dyn.html", rd)
        # Flonar main. Currently only Pflanzabstand form.
        config.add_route('flonar', '/flonar')
        config.add_view(flonar_pa_form, route_name='flonar')
        # Pflanzabstand engine IF 1.
        config.add_route('flonarpa', '/flonar/pa/{canton}/{distance}/{height}')
        config.add_view(flonarpa_engine, route_name='flonarpa')
        # Pflanzabstand engine IF 2.
        config.add_route('flonarpa2', '/flonar/pa')
        config.add_view(flonarpa_engine, route_name='flonarpa2')
        # Usage help.
        config.add_route('flonar_usage1', '/flonar/')
        #config.add_route('flonar_usage2', '/flonar/{name}')
        config.add_view(flonar_usage, route_name='flonar_usage1')
        #config.add_view(flonar_usage, route_name='flonar_usage2')
        app = config.make_wsgi_app()
    #server = make_server('0.0.0.0', 80, app)
    #server.serve_forever()
    waitress.serve(app, host='0.0.0.0', port=80)

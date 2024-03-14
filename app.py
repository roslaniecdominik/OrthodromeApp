from flask import Flask, render_template, request, jsonify, redirect, url_for, session, json, flash, abort
from numpy import radians, arctan, arctan2, tan, sin, cos, sqrt, degrees, isnan
import plotly.graph_objs as go
from werkzeug.exceptions import BadRequestKeyError, BadRequest

app = Flask(__name__, template_folder="templates")

app.secret_key = "qwerty"

def calculations(sign_start_v, sign_start_h, sign_end_v, sign_end_h, Latitude1, Longitude1, Latitude2, Longitude2):
    a_GRS80 = 6378137
    b_GRS80 = 6356752.3141

    e_2 = (a_GRS80**2 - b_GRS80**2)/(a_GRS80**2)
    f = (a_GRS80 - b_GRS80) / a_GRS80

    if sign_start_v == "dot-start-north":
        signed_Latitude1 = abs(Latitude1)
    elif sign_start_v == "dot-start-south":
        signed_Latitude1 = -abs(Latitude1)

    if sign_start_h == "dot-start-west":
        signed_Longitude1 = -abs(Longitude1)
    elif sign_start_h == "dot-start-east":
        signed_Longitude1 = abs(Longitude1)

    if sign_end_v == "dot-end-south":
        signed_Latitude2 = -abs(Latitude2)
    elif sign_end_v == "dot-end-north":
        signed_Latitude2 = abs(Latitude2)

    if sign_end_h == "dot-end-west":
        signed_Longitude2 = -abs(Longitude2)
    elif sign_end_h == "dot-end-east":
        signed_Longitude2 = abs(Longitude2)


    Latitude1 = signed_Latitude1
    Longitude1 = signed_Longitude1
    Latitude2 = signed_Latitude2
    Longitude2 = signed_Longitude2

    coord1 = [Latitude1, Longitude1]
    coord2 = [Latitude2, Longitude2]

    a = 6378137.0
    f = 1/298.257223563
    b = (1-f)*a

    phi_1, L_1 = coord1
    phi_2, L_2 = coord2                  

    u_1 = arctan((1-f)*tan(radians(phi_1)))
    u_2 = arctan((1-f)*tan(radians(phi_2)))

    L = radians(L_2-L_1)

    Lambda = L         

    sin_u1 = sin(u_1)
    cos_u1 = cos(u_1)
    sin_u2 = sin(u_2)
    cos_u2 = cos(u_2)

    # --- BEGIN ITERATIONS -----
    
    for iters in range(0, 200):
        iters += 1
        
        cos_lambda = cos(Lambda)
        sin_lambda = sin(Lambda)
        sin_sigma = sqrt((cos_u2*sin(Lambda))**2 + (cos_u1*sin_u2 - sin_u1*cos_u2*cos_lambda)**2)
        cos_sigma = sin_u1*sin_u2 + cos_u1*cos_u2*cos_lambda
        sigma = arctan2(sin_sigma, cos_sigma)
        sin_alpha = (cos_u1*cos_u2*sin_lambda)/sin_sigma
        cos_sq_alpha = 1-sin_alpha**2
        cos2_sigma_m = cos_sigma - ((2*sin_u1*sin_u2)/cos_sq_alpha)
        C = (f/16)*cos_sq_alpha*(4 + f*(4 - 3*cos_sq_alpha))
        Lambda_prev = Lambda
        Lambda = L + (1-C)*f*sin_alpha*(sigma + C*sin_sigma*(cos2_sigma_m + C*cos_sigma*(-1 + 2*cos2_sigma_m**2)))

        diff = abs(Lambda_prev - Lambda)
        if diff <= 10**-12:
            break
        
    u_sq = cos_sq_alpha*((a**2 - b**2)/b**2)
    A = 1+(u_sq/16384)*(4096 + u_sq*(-768+u_sq*(320 - 175*u_sq)))
    B = (u_sq/1024)*(256 + u_sq*(-128 + u_sq*(74 - 47*u_sq)))
    delta_sig = B*sin_sigma*(cos2_sigma_m + 0.25*B*(cos_sigma*(-1 + 2*cos2_sigma_m**2) - (1/6)*B*cos2_sigma_m*(-3 + 4*sin_sigma**2)*(-3 + 4*cos2_sigma_m**2)))

    distance = b*A*(sigma-delta_sig)                                  

    azimuth = arctan2((cos(u_2) * sin(Lambda)) , 
                (cos(u_1) * sin(u_2) - sin(u_1) * cos(u_2) * cos(Lambda)))     
    azimuth_inv = arctan2((cos(u_1) * sin(Lambda)) , 
                (-1 * sin(u_1) * cos(u_2) + cos(u_1) * sin(u_2) * cos(Lambda)))
    
    azimuth = degrees(azimuth)
    azimuth_inv = degrees(azimuth_inv) + 180

    session["Latitude1"] = Latitude1
    session["Longitude1"] = Longitude1
    session["Latitude2"] = Latitude2
    session["Longitude2"] = Longitude2


    # arc coordinates
    B = radians(Latitude1)
    L = radians(Longitude1)

    M = (a_GRS80 * (1 - e_2)) / ((sqrt(1- e_2 *(sin(B)**2)))**3)
    N = a_GRS80 / (sqrt(1-e_2*(sin(B)**2)))
    
    
    if distance < 1000000:
        ds = 5000
    elif distance <2000000:
        ds = 50000
    elif distance <5000000:
        ds = 80000
    else:
        ds = 100000
    

    PB = [degrees(B)]
    PL = [degrees(L)]

    s1 = 0
    Az = radians(azimuth)

    while s1 < distance:
        Np = N
        Mp = M
        Bp = B
        dL = ds * sin(Az) / (Np * cos(Bp))
        L = L + dL
        dB = ds * cos(Az) / Mp
        B = B + dB
        M = (a_GRS80 * (1 - e_2)) / ((sqrt(1-e_2*(sin(B)**2)))**3)
        N = a_GRS80 / (sqrt(1-e_2*(sin(B)**2)))
        Az = Az + ds / Np * sin(Az) * tan(Bp)
        s1 = s1 + ds

        PB.append(degrees(B))
        PL.append(degrees(L))

    PB = [x.round(4) for x in PB]
    PL = [x.round(4) for x in PL]

    session["PB"] = PB
    session["PL"] = PL
    session["distance"] = distance
    azimuth += 360
    session["azimuth"] = azimuth
    session["azimuth_inv"] = azimuth_inv


def radio_errros(form, keys):
    sign_start_v = None
    sign_start_h = None
    sign_end_v = None
    sign_end_h = None

    for key in keys:
        try:
            if key == "start-v":
                sign_start_v = form[key]
            elif key == "start-h":
                sign_start_h = form[key]
            elif key == "end-v":
                sign_end_v = form[key]
            elif key == "end-h":
                sign_end_h = form[key]
        except KeyError:
            pass
    
    error_detail = "Mark the directions"
    return sign_start_v, sign_start_h, sign_end_v, sign_end_h, error_detail

@app.route("/")
def index(): 
    return render_template("index.html")
  
@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    
    if request.method == "POST":
        error_message = "Please enter correct details"
        keys = ["start-v", "start-h", "end-v", "end-h"]

        try:
            name1 = request.form["name1"]
            name2 = request.form["name2"]
      
            Latitude1_user = request.form["Latitude1"]
            Longitude1_user = request.form["Longitude1"]
            Latitude2_user = request.form["Latitude2"]
            Longitude2_user = request.form["Longitude2"]

            if Latitude1_user.find(",") > 0:
                Latitude1_user = Latitude1_user.replace(",", ".")
            if Longitude1_user.find(",") > 0:
                Longitude1_user = Longitude1_user.replace(",", ".")
            if Latitude2_user.find(",") > 0:
                Latitude2_user = Latitude2_user.replace(",", ".")
            if Longitude2_user.find(",") > 0:
                Longitude2_user = Longitude2_user.replace(",", ".")
            
            Latitude1 = float(Latitude1_user)
            Longitude1 = float(Longitude1_user)
            Latitude2 = float(Latitude2_user)
            Longitude2 = float(Longitude2_user)

            try:
                if abs(Latitude1) > 90 or abs(Latitude2) > 90 or  abs(Longitude1) > 180 or abs(Longitude2) > 180:
                    abort(400, "")
            except:
                sign_start_v, sign_start_h, sign_end_v, sign_end_h, error_detail = radio_errros(request.form, keys)

                error_detail = "Latitude must be lower than 90, longitude must be lower than 180"
                
                return render_template("index.html", error_message = error_message, error_detail = error_detail, name1 = name1, name2 = name2, 
                            Latitude1 = Latitude1_user, Longitude1 = Longitude1_user, start_v = sign_start_v, start_h = sign_start_h,
                            Latitude2 = Latitude2_user, Longitude2 = Longitude2_user, end_v = sign_end_v, end_h = sign_end_h)

        except:
            sign_start_v, sign_start_h, sign_end_v, sign_end_h, error_detail = radio_errros(request.form, keys)
            
            error_detail = "The entered number must be an integer or decimal separated by a dot or a comma"
            return render_template("index.html", error_message = error_message, error_detail = error_detail, name1 = name1, name2 = name2, 
                                   Latitude1 = Latitude1_user, Longitude1 = Longitude1_user, start_v = sign_start_v, start_h = sign_start_h,
                                   Latitude2 = Latitude2_user, Longitude2 = Longitude2_user, end_v = sign_end_v, end_h = sign_end_h)

        try:
            sign_start_v = request.form["start-v"]
            sign_start_h = request.form["start-h"]
            sign_end_v = request.form["end-v"]
            sign_end_h = request.form["end-h"] 
        except:
            sign_start_v, sign_start_h, sign_end_v, sign_end_h, error_detail = radio_errros(request.form, keys)

            return render_template("index.html", error_message = error_message, error_detail = error_detail, name1 = name1, name2 = name2, 
                                   Latitude1 = Latitude1_user, Longitude1 = Longitude1_user, start_v = sign_start_v, start_h = sign_start_h,
                                   Latitude2 = Latitude2_user, Longitude2 = Longitude2_user, end_v = sign_end_v, end_h = sign_end_h)
        
        session["name1"] = name1
        session["name2"] = name2

        calculations(sign_start_v, sign_start_h, sign_end_v, sign_end_h, Latitude1, Longitude1, Latitude2, Longitude2)

        return redirect(url_for("show_map"))


@app.route("/show_map")
def show_map():
    Latitude1 = session.get("Latitude1")
    Latitude2 = session.get("Latitude2")
    Longitude1 = session.get("Longitude1")
    Longitude2 = session.get("Longitude2")

    latitudes = [Latitude1, Latitude2]
    longitudes = [Longitude1, Longitude2]

    #3D
    fig = go.Figure(go.Scattergeo())

    fig.add_trace(go.Scattergeo(
        locationmode = "country names",
        lon = longitudes,
        lat = latitudes,
        mode = "lines",
        line = dict(
            width = 2,
            color = "red"
        ),
        name = "Distance",
        showlegend = False
    ))

    fig.add_trace(go.Scattergeo(
        locationmode = "country names",
        lon = longitudes,
        lat = latitudes,
        mode = "markers",
        marker = dict(
            size = 6,
            color = "red",
            opacity = 0.8,
            symbol = "circle"
        ),
        name = "Points",
        showlegend = False
    ))
    
    fig.update_geos(projection_type = "orthographic")
    fig.update_layout(
        geo = dict(
            showocean = True,
            showland = True,
        ),
        margin = {"r":5, "t":0, "l":0, "b":0}
    )

    fig_dict = fig.to_dict()


    #2D
    PB = session.get("PB")
    PL = session.get("PL")

    fig2d = go.Figure()

    fig2d.add_trace(go.Scattermapbox(
        mode = "markers",
        lat = [PB[0], PB[-1]], 
        lon = [PL[0], PL[-1]], 
        marker = dict(size = 5, color = "red"),
        showlegend = False))

    fig2d.add_trace(go.Scattermapbox(
        mode = "lines",
        lat = PB,
        lon = PL,
        line = dict(width = 2, color = "red"),
        showlegend = False))
    
    if float(session.get("distance")) > 9000000:
        zoom = 1
    elif float(session.get("distance")) > 8000000:
        zoom = 2
    elif float(session.get("distance")) > 5000000:
        zoom = 2
    elif float(session.get("distance")) > 2000000:
        zoom = 3
    elif float(session.get("distance")) > 1000000:
        zoom = 4
    else:
        zoom = 5
    
    fig2d.update_layout(
        margin = {"l": 5, "t": 5, "b": 20, "r": 5},
        mapbox = {
            "style": "open-street-map",
            "center": {"lon": ((PL[0] + PL[-1])/2), "lat": ((PB[0] + PB[-1])/2)},
            "zoom": zoom})

    fig2d_dict = fig2d.to_dict()

    if Latitude1 < 0:
        Latitude1 = str(abs(Latitude1)) + "\u00b0" + " S"
    elif Latitude1 >= 0:
        Latitude1 = str(Latitude1) + "\u00b0" + " N"

    if Longitude1 < 0:
        Longitude1 = str(abs(Longitude1)) + "\u00b0" + " W"
    elif Longitude1 >= 0:
        Longitude1 = str(Longitude1) + "\u00b0" + " E"

    if Latitude2 < 0:
        Latitude2 = str(abs(Latitude2)) + "\u00b0" + " S"
    elif Latitude2 >= 0:
        Latitude2 = str(Latitude2) + "\u00b0" + " N"

    if Longitude2 < 0:
        Longitude2 = str(abs(Longitude2)) + "\u00b0" + " W"
    elif Longitude2 >= 0:
        Longitude2 = str(Longitude2) + "\u00b0" + " E"

    name1 = session.get("name1")
    name2 = session.get("name2")
    
    distance = session.get("distance") 
    azimuth = session.get("azimuth")
    azimuth_inv = session.get("azimuth_inv")

    if azimuth > 360:
        azimuth -=360

    if not isnan(distance):
        distance = round(float(distance)/1000)
        azimuth = round(float(azimuth))
        azimuth_inv = round(float(azimuth_inv))
        
    return render_template("map.html", 
                           fig = json.dumps(fig_dict), 
                           fig2d = json.dumps(fig2d_dict), 
                           distance = distance, 
                           azimuth = azimuth, 
                           azimuth_inv = azimuth_inv,
                           Longitude1 = Longitude1,
                           Latitude1 = Latitude1,
                           Longitude2 = Longitude2,
                           Latitude2 = Latitude2,
                           name1 = name1,
                           name2 = name2)

if __name__ == "__main__":
    app.run(debug = True)
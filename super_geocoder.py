# -----------------------------------------------------------
# Creating a website which converts address into 
# latitude-longitude information using python.
#
# (C) 2020 Sandra VS Nair, Trivandrum
# email sandravsnair@gmail.com
# -----------------------------------------------------------
 
from flask import Flask, render_template, request, send_file
from geopy.geocoders import Nominatim
import pandas

# Create a Flask instance.
app=Flask(__name__)

# Home page of the website.
@app.route('/',methods=['GET', 'POST'])
def home_page():
    return render_template("index.html")

# Displays the table with lat-long information.
@app.route('/table-view',methods=["POST"])
def table():
    if request.method=="POST":
        file=request.files["file"]          #Load the uploaded csv file.
        try:
            df=pandas.read_csv(file)
            gc=Nominatim(scheme='http',timeout=5,user_agent="any-geo-0.01")  #Create an instance of Nominatim class.
            df["coordinates"]=df["address"].apply(gc.geocode)                #Find the coordinates of a given address and store it as column "coordinates".
            df["Latitude"]=df["coordinates"].apply(lambda x: x.latitude if x!=None else None)  #Find the latitude and store it as column "latitude".
            df["Longitude"]=df["coordinates"].apply(lambda x: x.longitude if x!=None else None) #Find the longitude and store it as column "longitude".
            df=df.drop("coordinates",1)                                         #Drop column "coordinates".
            df.to_csv("geocoded_info.csv",index=None)                           #Save the csv file with lat-long information.
            return render_template("index.html",text=df.to_html(),btn="download.html")
        except:                                                                 #Error condition.
            return render_template("index.html",text="Please make sure you have an address column in your csv file")
        

#Download the file with lat-long information.
@app.route('/download-file')
def download():
    return send_file("geocoded_info.csv",attachment_filename="geocoded_info.csv",as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)
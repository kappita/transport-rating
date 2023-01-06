# Laboratorio para Fundamentos de Programación USACH 2021-2
## Project
This repository contains the program made for the Programming Fundaments for Engineering class, by group 3 from E-4 section.

## Members
The members of the project are: \
Maximiliano *****\
Esteban *******\
Ignacio Lara\
Ignacio *******

## Project description:
The project corresponds to the creation of an application where you can rate the drivers of the public transport system for them to, based on the rates obtained, get bonifications on salary or benefits, so this way the performance and attitude of the drivers gets improved.


## App operation
The app is based on two main pillars, a web API and a way to access it, being this case an UI.
The web API and UI are made in Python, using the Kivy and Flask modules, respectively.

### Web API
The web API made with flask has to receive, sort and deliver information to the users, as well as being where the information is focused, allowing the simultaneous and in real time communication between different devices without losing information between interactions.


### User Interface (UI)
The UI made with Kivy serves the purpose of giving the user the tools to interact with the web API, without having to know the commands or confusing ways to give information. This is achieved by only asking the necessary information to te user, and being the app who takes that information, interprets it and sends it for later usage.


## Requirements
In order for the app to work correctly, six python modules are necessary:\
Kivy\
Flask\
Flask-Restful\
Requests\
OpenCV \
Pyzbar

Additionally you can have Droidcam installed in a smartphone connected to the same internet network the Kivy app is.



## Instructions for the use of the app
To use the app you need to have constantly running the program 'api.py' found in the 'api' folder. Then, you have to verify that the 'ip_api' variable at main.py is identical to the ip printed by the api in the console.\
Now, you can finally use the app without limitations. It can be useful to know that the app can run without the use of a camera connection, but the program will take a little bit longer to load, as it is checking if a camera is connected or not.


### In case of using DroidCam as a camera
It is important to have the app running while the main program is starting, as well as replacing the 'ip_droidcam' variable with the ip and ports given by the app, in a string format and in the shape ip:port.


## Additional information
In the 'misc' folder are two programs created for the random generation of transantiago buses (With vehicle patents and route) and the random generation of drivers for those vehicles. Also, you can find 5 sample QR codes for you to try the QR recognition feature.


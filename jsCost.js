// Javascript (web interface) version of utility_calc_cost.py
//    file ~/Encrypted/GHRental/Meters/jsCost.js
"use strict";
const galInCuFt = 0.0278;

/*  Data in CSV format:
Date,cu_ft,kwh,current price of propane/gal,paid,comment
2016-03-19,30.1,59466,N/A,N/A,Initial reading
2016-04-16,853.7,59708,$4.079,$181.35,1st reading 
2016-05-23,1691.8,60063,$3.379,$105.21,2nd reading

In JSON notation: */
var dataStr = [
{"date": "2016-03-19","gas": 30.1, "cost": 0,
                        "kwh": 59466, "paid": 0},
{"date": "2016-04-16","gas": 853.7, "cost": 4.079,
                        "kwh": 59708, "paid": 181.35},
{"date": "2016-05-23","gas": 1691.8, "cost": 3.379,
                        "kwh": 60063, "paid": 105.21},
]

//var dataJson = JSON.parse(dataStr)

var gas = {
    prevReading: 853.7,
    curReading: 1691.8,
    cost: 3.379,
    };

function getElectricity(){
    return {
    }
}

var electricityDefaults = {
    prevReading: 59708,
    curReading: 60063,
    date1: {
        yr: 2016,
        mo: 4,
        d: 16,
        },
    date2: {
        yr: 2016,
        mo: 5,
        d: 23,
        },
    };
/*
var model = {
    show: function(gasAmount, gasPrice, kWh){
        console.log("Output of model.show()");
        console.log("There are "+galInCuFt+" gal in a cuft.");
        },
    };
model.show();
*/

function calculate(){
    var gasResult = document.getElementById('gasResult');
    gasResult.textContent = "New RESULTS";
}

function getJson(){
    dataString = getElementById('readings')';
    resultPage = getElementById('results');
    resultPage.textContent = dataString
}

function check4Storage(){
    if(typeof(Storage)!=="undefined"){
        document.write("It's OK.");
    }
    else{
        document.write("Too bad.");
    }
}


var conversionFactor = document.getElementById("conversionFactor");
conversionFactor.textContent = String(galInCuFt) +
                               " Gallons per Cubic Ft";
var prevDate = document.getElementById("prevDate");
var curDate = document.getElementById("curDate");
var kwhPrev = document.getElementById("kwhPrev");
var kwhCur = document.getElementById("kwhCur");
var gasCost = document.getElementById("gasCost");
var gasPrev = document.getElementById("gasPrev");
var gasCur = document.getElementById("gasCur");
var hotButton = document.getElementById("hotButton");

gasCur.value = "70000"

check4Storage();

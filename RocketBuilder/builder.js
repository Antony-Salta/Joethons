jsonData = `{
    "heads" :[
        {
            "speed":87,
            "weight":2050,
            "cost":890,
            "image":"./Images/RocketTop1.png"
        },
        {
            "speed":95,
            "weight":2150,
            "cost":950,
            "image":"./Images/RocketTop2.png"
        },
        {
            "speed":92,
            "weight":2250,
            "cost":920,
            "image":"./Images/RocketTop3.png"
        }
    ],
    "bodies" :[
        {
            "strength":120,
            "weight":1100,
            "cost":1050,
            "image":"./Images/RocketBody1.png"
        },
        {
            "strength":115,
            "weight":1050,
            "cost":1000,
            "image":"./Images/RocketBody2.png"
        },
        {
            "strength":110,
            "weight":1000,
            "cost":950,
            "image":"./Images/RocketBody3.png"
        }
    ],
    "thrusts": [
        {
            "thrust":105,
            "weight":950,
            "cost":980,
            "image":"./Images/RocketThruster1.png"
        },
        {
            "thrust":100,
            "weight":1000,
            "cost":1000,
            "image":"./Images/RocketThruster2.png"
        },
        {
            "thrust":98,
            "weight":1050,
            "cost":1020,
            "image":"./Images/RocketThruster3.png"
        }
    ],
    "protection" : {
        "acid": {
            "cost":1000
        },
        "heat": {
            "cost":1000
        },
        "pressure": {
            "cost":1000
        }
    }
}`

const totalBudget = 10000;
const maxFuel = 1000;
const fuelCostPerLitre = 3;

var json = JSON.parse(jsonData);
var rocketHeads = json.heads;
var rocketBodies = json.bodies;
var rocketThrusts = json.thrusts;
var rocketProtection = json.protection;

var headPtr = 0;
var bodyPtr = 0;
var thrustPtr = 0;

var acidProtection = false;
var heatProtection = false;
var pressureProtection = false;

function builderLoaded() {
    updateRocketBody();
    updateRocketHead();
    updateRocketThrust();
    fuelChanged(50);
    adjustBudget();
}

function rotateRight(rocketPart) {
    switch (rocketPart) {
        case "head":
            headPtr += 1;
            if (headPtr >= rocketHeads.length) {
                headPtr = 0;
            }
            updateRocketHead();
            break;
        case "body":
            bodyPtr += 1;
            if (bodyPtr >= rocketBodies.length) {
                bodyPtr = 0;
            }
            updateRocketBody();
            break;

        case "thrust":
            thrustPtr += 1;
            if (thrustPtr >= rocketThrusts.length) {
                thrustPtr = 0;
            }
            updateRocketThrust();
            break;
    }
    adjustBudget();
}

function rotateLeft(rocketPart) {
    switch (rocketPart) {
        case "head":
            headPtr -= 1;
            if (headPtr < 0) {
                headPtr = rocketHeads.length - 1;
            }
            updateRocketHead();
            break;

        case "body":
            bodyPtr -= 1;
            if (bodyPtr < 0) {
                bodyPtr = rocketBodies.length - 1;
            }
            updateRocketBody();
            break;
        case "thrust":
            thrustPtr -= 1;
            if (thrustPtr < 0) {
                thrustPtr = rocketThrusts.length - 1;
            }
            updateRocketThrust();
            break;
    }
    adjustBudget();
}

function updateRocketHead() {
    document.getElementById("headImage").src = rocketHeads[headPtr].image;
    document.getElementById("headSpeed").innerHTML = "Speed : " + rocketHeads[headPtr].speed + "m/s";
    document.getElementById("headWeight").innerHTML = "Weight : " + rocketHeads[headPtr].weight + "kg";
    document.getElementById("headCost").innerHTML = "Cost : £" + rocketHeads[headPtr].cost;
}

function updateRocketBody() {
    document.getElementById("bodyImage").src = rocketBodies[bodyPtr].image;
    document.getElementById("bodyStrength").innerHTML = "Strength : " + rocketBodies[bodyPtr].strength;
    document.getElementById("bodyWeight").innerHTML = "Weight : " + rocketBodies[bodyPtr].weight + "kg";
    document.getElementById("bodyCost").innerHTML = "Cost : £" + rocketBodies[bodyPtr].cost;
}

function updateRocketThrust() {
    document.getElementById("thrustImage").src = rocketThrusts[thrustPtr].image;
    document.getElementById("thrustThrust").innerHTML = "Thrust : " + rocketThrusts[thrustPtr].thrust;
    document.getElementById("thrustWeight").innerHTML = "Weight : " + rocketThrusts[thrustPtr].weight + "kg";
    document.getElementById("thrustCost").innerHTML = "Cost : £" + rocketThrusts[thrustPtr].cost;
}

function fuelChanged(value) {
    const fuel = maxFuel * value * 0.01;
    document.getElementById("fuelCounter").innerHTML = "Fuel: " + fuel + "litres";
    document.getElementById("fuelWeight").innerHTML = "Weight: " + fuel + "kg";
    document.getElementById("fuelCost").innerHTML = "Fuel Cost: £" + fuel * fuelCostPerLitre;
    adjustBudget();
}

function protectionClicked(type) {
    switch (type) {
        case "acid":
            acidProtection = document.getElementById("acidCheckbox").checked;
            break;
        case "heat":
            heatProtection = document.getElementById("heatCheckbox").checked;
            break;
        case "pressure":
            pressureProtection = document.getElementById("pressureCheckbox").checked;
            break;
    }
    adjustBudget();
}

function adjustBudget() {
    const fuelCost = parseInt(document.getElementById("fuelCost").innerHTML.toString().replace("Fuel Cost: £", ""));
    var budget = totalBudget - (rocketHeads[headPtr].cost + rocketBodies[bodyPtr].cost + rocketThrusts[thrustPtr].cost + fuelCost);
    if (acidProtection) {
        budget -= 1000;
    }
    if (heatProtection) {
        budget -= 1000;
    }
    if (pressureProtection) {
        budget -= 1000;
    }
    document.getElementById("budget").innerHTML = "Budget : £" + budget;
}

function runSimulation() {

}

function runGame() {

}
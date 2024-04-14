var totalBudget;
var currentPlanet;
var targetPlanet;

var planets;

var rocketHeads;
var rocketBodies;
var rocketThrusts;
var rocketProtection;

const maxFuel = 1000;
const fuelCostPerLitre = 3;

var headPtr = 0;
var bodyPtr = 0;
var thrustPtr = 0;

var acidProtection = false;
var heatProtection = false;
var pressureProtection = false;

function builderLoaded() {
    fetch('http://localhost:3000/getStatus/')
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            totalBudget = data.budget;
            currentPlanet = data.currentPlanet;
            targetPlanet = data.targetPlanet;
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        }); 


    fetch('http://localhost:3000/getRocketParts/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        rocketHeads = data.heads;
        rocketBodies = data.bodies;
        rocketThrusts = data.thrusts;
        rocketProtection = data.protection;
        updateRocketBody();
        updateRocketHead();
        updateRocketThrust();
        fuelChanged(50);
        adjustBudget();
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });


    fetch('http://localhost:3000/getPlanets/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        planets = data;
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });    
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
    const fuelWeight = document.getElementById("fuelWeight").innerHTML.toString().replace("Weight: ", "").replace("kg","");
    const mass = rocketHeads[headPtr].weight + rocketBodies[bodyPtr].weight + rocketThrusts[thrustPtr].weight + fuelWeight;
    const fuel = document.getElementById("fuelCost").innerHTML.toString().replace("Fuel Cost: £", "").replace("litres","");
    const speed = rocketHeads[headPtr].speed;
    const thrust = rocketThrusts[thrustPtr].thrust;
    const strength = rocketBodies[bodyPtr].strength;

    const resistance = speed/100;
    const weight = mass;
    const acceleration = thrust - (weight * 0.000001);
    const exit = acceleration * resistance;

    console.log(exit)

    document.getElementById("simulationVideo").src = "";
    document.getElementById("rocketBuilder").style.visibility = "hidden";
    document.getElementById("rocketBuilder").style.display = "none";
    document.getElementById("simulationVideo").style.visibility = "visible";
    document.getElementById("simulationVideo").style.display = "block";
    document.getElementById("simulationTitle").style.visibility = "visible";
    document.getElementById("simulationTitle").style.display = "block";
    document.body.style.background = "black";

    if (exit < planets[currentPlanet].exit) {
        // run simulation where explosion occurs on exit
        document.getElementById("simulationVideo").src = "./Animations/CantExitExplosionAnimation.gif";
        loadSimulationEnd("You weren't able to escape the atmosphere, seems you don't have the power or speed to lift the weight!", 3000);
    } else {
        const distanceCanTravel = (fuel * 1000)/weight
        const distanceToTravel = Math.abs(planets[currentPlanet].distanceToSun - planets[targetPlanet].distanceToSun);
        if (distanceCanTravel < distanceToTravel) {
            // run simulation where explosion occurs in space
            document.getElementById("simulationVideo").src = "./Animations/FuelConsumptionExplosionAnimation.gif";
            loadSimulationEnd("Seem you ran out of fuel!", 5000);
        } else {
            if (planets[targetPlanet].enter.atmosphere > strength ||
            planets[targetPlanet].enter.acid && !acidProtection ||
            planets[targetPlanet].enter.heat && !heatProtection ||
            planets[targetPlanet].enter.pressure && !pressureProtection) {
                // run simulation where explosion occurs on enter
                document.getElementById("simulationVideo").src = "./Animations/enterExplosionAnimation.gif";
                loadSimulationEnd("Your rocket ship didn't have the protection required to land!", 7000);
            } else {
                // run successful simulation    
                document.getElementById("simulationVideo").src = "./Animations/successfulAnimation.gif";
                document.getElementById("simulationText").style.color = "green";
                loadSimulationEnd("Congrats! Your ship successfully passed the simulation!", 7000);
            }
        }
    }
}

function loadSimulationEnd(message, time) {
    window.setTimeout(function() {
        document.getElementById("simulationMessage").style.visibility = "visible";
        document.getElementById("simulationMessage").style.display = "block";
        document.getElementById("simulationText").innerHTML = message;
    }, time); 
}

function endSimulation() {
    document.body.style.background = "linear-gradient(to bottom right, purple, violet, dodgerblue, blue)";
    document.getElementById("rocketBuilder").style.visibility = "visible";
    document.getElementById("rocketBuilder").style.display = "block";
    document.getElementById("simulationVideo").style.visibility = "hidden";
    document.getElementById("simulationVideo").style.display = "none";
    document.getElementById("simulationMessage").style.visibility = "hidden";
    document.getElementById("simulationMessage").style.display = "none";
    document.getElementById("simulationTitle").style.visibility = "hidden";
    document.getElementById("simulationTitle").style.display = "none";
}

function runGame() {

}
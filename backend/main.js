const express = require('express');
const cors = require("cors");
const bodyParser = require('body-parser');
const fs = require('fs').promises;
const app = express();
const port = 3000;

app.use(bodyParser.json());

const corsOptions = {
    origin: 'http://localhost:8080', // Allow requests from frontend
    methods: ['GET', 'POST'], // Allow only GET and POST methods
};

app.use(cors(corsOptions));

// Function to read data from a JSON file
async function readFromJsonFile(filePath) {
    try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error(`Error reading from ${filePath}`, error);
        throw error;
    }
}

// Function to write data to a JSON file
async function writeToJsonFile(filePath, data) {
    try {
        await fs.writeFile(filePath, JSON.stringify(data, null, 2));
    } catch (error) {
        console.error(`Error writing to ${filePath}`, error);
        throw error;
    }
}

app.get("/getStatus", async (req, res) => {
    try {
        const status = await readFromJsonFile('data/status.json');

        res.send(status);
    } catch (error) {
        res.status(500).send({ message: "Error finding user", error:error.message});
    }
});

app.post('/updateStatus', async (req, res) => {
    const newRequest = req.body;

    try {
        await writeToJsonFile('data/status.json', newRequest);

        res.send({ message: 'Request submitted successfully', request: newRequest });
    } catch (error) {
        res.status(500).send({ message: 'Error submitting request', error: error.message });
    }
});



app.get("/getPlanets", async (req, res) => {
    try {
        const planets = await readFromJsonFile('data/planets.json');

        res.send(planets);
    } catch (error) {
        res.status(500).send({ message: "Error finding user", error:error.message});
    }
});

app.get("/getRocketParts", async (req, res) => {
    try {
        const parts = await readFromJsonFile('data/rocketParts.json');

        res.send(parts);
    } catch (error) {
        res.status(500).send({ message: "Error finding user", error:error.message});
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
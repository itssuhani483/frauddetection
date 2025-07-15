const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const Contact = require('./models/Contact'); // Import the Contact model
const { spawn } = require('child_process');
require('dotenv').config(); // Load environment variables

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Logging middleware
app.use((req, res, next) => {
    console.log(`Request Method: ${req.method}, Request URL: ${req.url}`);
    next();
});

// MongoDB Connection
mongoose.connect('mongodb://localhost:27017/Fraud_detect_contactForm')
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// Function to call Python script for fraud prediction
async function predict(contactData) {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', ['D:\\fraud-detection-web-app-main\\fraud-detection-web-app-main\\backend\\prediction.py', JSON.stringify(contactData)]);

        pythonProcess.stdout.on('data', (data) => {
            try {
                resolve(JSON.parse(data.toString()));
            } catch (err) {
                reject(new Error('Error parsing prediction result.'));
            }
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`Python error: ${data.toString()}`);
            reject(new Error(data.toString()));
        });

        pythonProcess.on('exit', (code) => {
            if (code !== 0) {
                reject(new Error(`Python process exited with code: ${code}`));
            }
        });
    });
}

// POST route for contact form (used for detecting fraud)
app.post('/api/contact', async (req, res) => {
    const { name, email, phone, text } = req.body;

    if (!name || !email || !phone || !text) {
        return res.status(400).json({ error: 'All fields are required.' });
    }

    // Create a new contact instance
    const contact = new Contact({ name, email, phone, text });

    try {
        await contact.save(); // Save to the database

        // Prepare contact data for prediction
        const contactData = { name, email, phone, text };

        // Make prediction
        const predictionResult = await predict(contactData);
        console.log('Prediction Result:', predictionResult);
        
        res.status(200).json({ 
            message: 'Contact data received successfully.', 
            fraudDetected: predictionResult 
        });
    } catch (error) {
        console.error('Error:', error); 
        res.status(500).json({ error: 'Error executing fraud prediction.' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

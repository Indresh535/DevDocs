const fs = require('fs');
const path = require('path');
const axios = require('axios');

class EventTracker {
    constructor(config = {}) {
        this.defaultConfig = {
            logToFile: true,
            logFilePath: path.join(__dirname, '../logs/events.log'),
            logToAPI: false,
            apiEndpoint: '',
        };
        this.config = { ...this.defaultConfig, ...config };
    }

    async logEvent(eventName, metadata = {}) {
        const event = {
            name: eventName,
            timestamp: new Date().toISOString(),
            metadata,
        };

        try {
            if (this.config.logToFile) {
                await this._logToFile(event);
            }
            if (this.config.logToAPI) {
                await this._logToAPI(event);
            }
        } catch (error) {
            console.error('Failed to log event:', error.message);
        }
    }

    async _logToFile(event) {
        const logData = JSON.stringify(event) + '\n';
        return new Promise((resolve, reject) => {
            fs.appendFile(this.config.logFilePath, logData, (err) => {
                if (err) reject(err);
                else resolve();
            });
        });
    }

    async _logToAPI(event) {
        if (!this.config.apiEndpoint) {
            throw new Error('API endpoint is not configured.');
        }
        return axios.post(this.config.apiEndpoint, event);
    }
}

module.exports = EventTracker;

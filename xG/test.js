const fs = require('fs');
const beautify = require('js-beautify').js;
const fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
require('dotenv').config();

const getData = async (url) => {
  return await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Authorization': `Bearer ${process.env.BALLCHASING_TOKEN}`
    }
  }).then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.text();
  });
};

const getPlayerData = async (replayID) => {
  try {
    const response = await getData("https://ballchasing.com/dyn/replay/" + replayID + "/threejs");
    fs.writeFileSync("replayData.js", beautify(response), "utf8");
    console.log("File 'replayData.js' created successfully.");
  } catch (error) {
    console.error("Error fetching data:", error.message);
  }
};

getPlayerData("f226e485-cd29-40d1-96a5-642f79be3787");
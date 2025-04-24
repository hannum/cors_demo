'use strict';

async function getAirportData() {                     // asynchronous function is defined by the async keyword
  console.log('asynchronous download begins');
  try {                                               // error handling: try/catch
    const response = await fetch('http://127.0.0.1:3000/lentokentta/00A');    // starting data download, fetch returns a promise which contains an object of type 'response'
    const jsonData = await response.json();          // retrieving the data retrieved from the response object using the json() function
    console.log(jsonData.ICAO, jsonData.Name);       // log the result to the console
  } catch (error) {
    console.log(error.message);
  }
}

getAirportData();

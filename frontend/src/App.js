import './App.css';
import PlayerForm from './components/PlayerForm';
import Header from './components/Header';
import About from './components/About.js';
import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';

const roundValue = (value, decimals = 3) => {
  if (typeof value === 'number') {
    return value.toFixed(decimals);
  }
  return value;
};
const CSVTable = ({ data }) => {
  const originalHeaders = data[0] && Object.keys(data[0]);
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: 'ascending',
  });
  const modifiedHeaders = originalHeaders
    ? ['Player']
        .concat(
          originalHeaders.filter(
            header => header !== 'player_id' && header !== 'first_name' && header !== 'last_name'
          )
        )
    : [];

  const modifiedData = data.map(row => {
    const { player_id, first_name, last_name, ...otherColumns } = row;
    return { ...otherColumns, Player: `${first_name} ${last_name}` };
  });

  const sortData = (data, sortConfig) => {
    const sortedData = [...data];
    if (sortConfig.key) {
      sortedData.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortedData;
  };
  
  const requestSort = key => {
    const direction = sortConfig.key === key && sortConfig.direction === 'ascending' ? 'descending' : 'ascending';
    setSortConfig({ key, direction });
  };
  
  const sortedData = sortData(modifiedData, sortConfig);

  return (
    
    <div className="table-wrapper">
      <table className="csv-table">
        <thead>
          <tr>
            {modifiedHeaders &&
              modifiedHeaders.map((header, index) => (
                <th key={index} onClick={() => requestSort(header)}>
                {header}
              </th>
              ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, index) => (
            <tr key={index}>
              {modifiedHeaders.map((header, columnIndex) => (
                <td key={columnIndex}>{roundValue(row[header])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};







function App() {
  const [csvData, setCsvData] = useState([]);
  const [pitchingCsvData, setPitchingCsvData] = useState([]);

  useEffect(() => {
    const fetchCSVData = async () => {
      const response = await fetch('/OpperStats/b_forest_pred.csv');
      const reader = response.body.getReader();
      const result = await reader.read();
      const decoder = new TextDecoder('utf-8');
      const csv = decoder.decode(result.value);
      const results = Papa.parse(csv, { header: true, dynamicTyping: true });
      const rows = results.data;
      setCsvData(rows);
    };
  
    fetchCSVData();
  }, []);

  useEffect(() => {
    const fetchPitchingCSVData = async () => {
      const response = await fetch('/OpperStats/p_forest_pred.csv');
      const reader = response.body.getReader();
      const result = await reader.read();
      const decoder = new TextDecoder('utf-8');
      const csv = decoder.decode(result.value);
      const results = Papa.parse(csv, { header: true, dynamicTyping: true });
      const rows = results.data;
      setPitchingCsvData(rows);
    };
  
    fetchPitchingCSVData();
  }, []);
  
  

  return (
    <div className="App">
      <Header />
      <PlayerForm csvData={csvData} pitchingCsvData={pitchingCsvData} />
      <h2>2023 OpperStats Preseason Batting Projections:</h2>
      <CSVTable data={csvData} />
      <h2>2023 OpperStats Preseason Pitching Projections:</h2>
      <CSVTable data={pitchingCsvData} />
      <About />
    </div>
  );
}

export default App;



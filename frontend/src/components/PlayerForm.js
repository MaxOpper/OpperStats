import React, { useState } from 'react';
import axios from 'axios';
import './Component.css';

function getPlayerImageUrl(playerID) {
  if (!playerID) return null;
  return `https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:silo:current.png/r_max/w_180,q_auto:best/v1/people/${playerID}/headshot/silo/current`;
}


function PlayerForm({ csvData, pitchingCsvData }) {
  const [inputPlayerName, setInputPlayerName] = useState('');
  const [playerName, setPlayerName] = useState('');
  const [projections, setProjections] = useState(null);
  const [playerID, setPlayerID] = useState(null);

  function findPlayerID(playerName, csvDataArray) {
    for (const row of csvDataArray) {
      const fullName = `${row.first_name} ${row.last_name}`;
      if (fullName === playerName) {
        return row.player_id;
      }
    }
    
    return null;
  }
  
  function handleInputChange(event) {
    setInputPlayerName(event.target.value);
  }
  


  function handleSubmit(event) {
    event.preventDefault();
    setPlayerName(inputPlayerName);
    const battingPlayerID = findPlayerID(inputPlayerName, csvData);
    const pitchingPlayerID = findPlayerID(inputPlayerName, pitchingCsvData);
    const currentPlayerID = battingPlayerID || pitchingPlayerID;

    setPlayerID(currentPlayerID);
    axios.post('http://18.118.162.92:5000/projections', {player_name: inputPlayerName})
      .then(response => {
        setProjections(response.data);
      })
      .catch(error => {
        console.log(error);
        setProjections(null);
      });
  }


  return (
    <div className="player-form-container">
      <form onSubmit={handleSubmit} className="player-form">
        <div className="player-search">
          <label className="player-search-label">
            <input type="text" value={inputPlayerName} onChange={handleInputChange} placeholder="Search for a player" className="player-search-input" />
          </label>
          <button type="submit" disabled={!inputPlayerName} className="player-search-button">Submit</button>
          
        </div>
      </form>
      {projections !== null ? (
        <div>
          <h2>{playerName} Live Projections:</h2>
          {playerID && <img src={getPlayerImageUrl(playerID)} alt={`${playerName}`} />}
          {projections.batting_avg ? (
  <div>
    <h3>Batting Projections</h3>
    <table>
      <tbody>
        <tr>
          <td>AVG:</td>
          <td>{projections.batting_avg.toFixed(3)}</td>
        </tr>
        <tr>
          <td>OBP:</td>
          <td>{projections.on_base_percent.toFixed(3)}</td>
        </tr>
        <tr>
          <td>SLG:</td>
          <td>{projections.slg_percent.toFixed(3)}</td>
        </tr>
        <tr>
          <td>OPS:</td>
          <td>{(projections.on_base_percent + projections.slg_percent).toFixed(3)}</td>
        </tr>
      </tbody>
    </table>
  </div>
) : null}
{projections.p_era ? (
  <div>
    <h3>Pitching Projections</h3>
    <table>
      <tbody>
        <tr>
          <td>ERA:</td>
          <td>{projections.p_era.toFixed(2)}</td>
        </tr>
        <tr>
          <td>BAA:</td>
          <td>{projections.p_opp_batting_avg.toFixed(3)}</td>
        </tr>
        <tr>
          <td>WOBA:</td>
          <td>{projections.woba.toFixed(3)}</td>
        </tr>
      </tbody>
    </table>
  </div>
) : null}

        </div>
      ) : null}
    </div>
  );
}

export default PlayerForm;

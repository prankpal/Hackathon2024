// import { useEffect, useState } from 'react';
// import axios from 'axios';
// import { Container, Row, Col, Card } from 'react-bootstrap';

// function Playlists() {
//     const [playlists, setPlaylists] = useState([]);

//     useEffect(() => {
//         const fetchPlaylists = async () => {
//             try {
//                 const response = await axios.get('http://localhost:5001/playlists');
//                 setPlaylists(response.data);
//             } catch (error) {
//                 console.error("Error fetching playlists:", error);
//             }
//         };
//         fetchPlaylists();
//     }, []);

//     return (
//         <Container className="mt-4">
//             <h1>Your Spotify Playlists</h1>
//             <Row>
//                 {playlists.map((playlist) => (
//                     <Col key={playlist.id} md={4} className="mb-4">
//                         <Card className="h-100">
//                             <Card.Body>
//                                 <Card.Title>{playlist.name}</Card.Title>
//                                 <Card.Text>Tracks: {playlist.track_count}</Card.Text>
//                             </Card.Body>
//                         </Card>
//                     </Col>
//                 ))}
//             </Row>
//         </Container>
//     );
// }

// export default Playlists;

import React, { useState } from 'react';
import axios from 'axios';

const PlaylistsPage = () => {
  const [playlists, setPlaylists] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  const fetchPlaylists = async () => {
    try {
      const response = await axios.get('http://localhost:5001/playlists');
      setPlaylists(response.data);
    } catch (error) {
      console.error('Error fetching playlists:', error);
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      alert('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('streaming_data', selectedFile);
    formData.append('start_date', startDate);
    formData.append('end_date', endDate);

    try {
      const response = await axios.post('http://localhost:5001/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      console.log('Analysis Results:', response.data);
    } catch (error) {
      console.error('Error analyzing streaming data:', error);
    }
  };

  React.useEffect(() => {
    fetchPlaylists();
  }, []);

  return (
    <div>
      <h1>Your Spotify Playlists</h1>
      {playlists.length > 0 ? (
        <ul>
          {playlists.map((playlist) => (
            <li key={playlist.id}>{playlist.name} ({playlist.track_count} tracks)</li>
          ))}
        </ul>
      ) : (
        <p>Loading playlists...</p>
      )}

      <div>
        <input
          type="datetime-local"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
        <input
          type="datetime-local"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleAnalyze}>Analyze</button>
      </div>
    </div>
  );
};

export default PlaylistsPage;
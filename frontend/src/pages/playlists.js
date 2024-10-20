import { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Card } from 'react-bootstrap';

function Playlists() {
    const [playlists, setPlaylists] = useState([]);

    useEffect(() => {
        const fetchPlaylists = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/playlists');
                setPlaylists(response.data);
            } catch (error) {
                console.error("Error fetching playlists:", error);
            }
        };
        fetchPlaylists();
    }, []);

    return (
        <Container className="mt-4">
            <h1>Your Spotify Playlists</h1>
            <Row>
                {playlists.map((playlist) => (
                    <Col key={playlist.id} md={4} className="mb-4">
                        <Card className="h-100">
                            <Card.Body>
                                <Card.Title>{playlist.name}</Card.Title>
                                <Card.Text>Tracks: {playlist.track_count}</Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                ))}
            </Row>
        </Container>
    );
}

export default Playlists;

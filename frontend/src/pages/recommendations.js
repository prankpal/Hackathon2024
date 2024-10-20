import react from 'react';
import axios from 'axios';

function Recommendations({ playlistId }) {
    const [recommendations, setRecommendations] = react.useState([]);

    react.useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5000/playlists/${playlistId}/tracks`);
                setRecommendations(response.data);
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            }
        };
        if (playlistId) {
            fetchRecommendations();
        }
    }, [playlistId]);

    return (
        <div>
            <h2>Recommended Tracks to Remove</h2>
            <ul>
                {recommendations.map((track, index) => (
                    <li key={index}>
                        {track.name} by {track.artist}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Recommendations;

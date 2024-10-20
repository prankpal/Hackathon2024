import React from 'react';

const Recommendations = ({ results }) => {
  return (
    <div className="results mt-5">
      <h3>Analysis Results</h3>
      <h4>Top 10 Most Skipped Tracks:</h4>
      <ul>
        {results.skipped_tracks.slice(0, 10).map((track, index) => (
          <li key={index}>
            {track.artist} - {track.track} (Skipped: {track.count}x)
          </li>
        ))}
      </ul>

      <h4>Playlist Analysis:</h4>
      {results.playlist_analysis.length > 0 ? (
        results.playlist_analysis.map((playlist, index) => (
          <div key={index} className="playlist-analysis my-4">
            <h5>{playlist.playlist_name}</h5>
            <ul>
              {playlist.tracks_to_remove.map((track, i) => (
                <li key={i}>
                  {track.artist} - {track.track} (Skipped: {track.count}x)
                </li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No skipped tracks found in playlists.</p>
      )}
    </div>
  );
};

export default Recommendations;

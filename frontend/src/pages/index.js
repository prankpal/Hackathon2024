// import React, { useState } from 'react';
// import axios from 'axios';
// import DatePicker from 'react-datepicker';
// import "react-datepicker/dist/react-datepicker.css";

// const IndexPage = () => {
//   const [startDate, setStartDate] = useState(new Date('2023-01-01'));
//   const [endDate, setEndDate] = useState(new Date('2023-12-31'));
//   const [results, setResults] = useState(null);
//   const [selectedFiles, setSelectedFiles] = useState(null);

//   const handleFileChange = (event) => {
//     setSelectedFiles(event.target.files);
//   };

//   const uploadStreamingData = async () => {
//     if (!selectedFiles || selectedFiles.length === 0) {
//       alert("Please select a file to upload");
//       return;
//     }
  
//     const formData = new FormData();
//     formData.append('streaming_data', selectedFiles[0]);
  
//     try {
//       const response = await axios.post("http://localhost:5001/analyze", formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data'
//         }
//       });
//       setResults(response.data);
//     } catch (error) {
//       console.error('Error uploading streaming data:', error);
//       alert("There was an error processing your request. Please try again.");
//     }
//   };
  

//   return (
//     <div className="container text-center my-5">
//       <h1 className="display-4">Spotify Playlist Cleaner - Data Analysis</h1>
//       <p className="lead">Analyze your most played and skipped tracks within a specific date range.</p>

//       <div className="my-4">
//         {/* Button to initiate Spotify login through backend */}
//         <a href="http://0.0.0.0:5001/login" className="btn btn-success btn-lg mb-4">
//           Login to Spotify
//         </a>
        
//         <div className="date-picker">
//           <label className="mx-2">Start Date:</label>
//           <DatePicker
//             selected={startDate}
//             onChange={(date) => setStartDate(date)}
//             dateFormat="yyyy-MM-dd HH:mm"
//             showTimeSelect
//             timeFormat="HH:mm"
//           />
//         </div>
//         <div className="date-picker my-3">
//           <label className="mx-2">End Date:</label>
//           <DatePicker
//             selected={endDate}
//             onChange={(date) => setEndDate(date)}
//             dateFormat="yyyy-MM-dd HH:mm"
//             showTimeSelect
//             timeFormat="HH:mm"
//           />
//         </div>
//         <div className="file-upload my-4">
//           <input type="file" accept=".json" multiple onChange={handleFileChange} />
//         </div>
//         <button
//           className="btn btn-primary btn-lg"
//           onClick={uploadStreamingData}
//         >
//           Analyze Streaming Data
//         </button>
//       </div>
//       {results && (
//         <div className="results mt-5">
//           <h3>Analysis Results</h3>
//           <h4>Top 10 Most Played Tracks:</h4>
//           <ul>
//             {results.top_played && results.top_played.slice(0, 10).map((track, index) => (
//               <li key={index}>
//                 {track.artist} - {track.track} (Played: {track.play_count}x)
//               </li>
//             ))}
//           </ul>
//           <h4>Most Skipped Tracks:</h4>
//           <ul>
//             {results.skipped_tracks && results.skipped_tracks.map((track, index) => (
//               <li key={index}>
//                 {track.artist} - {track.track} (Skipped: {track.count}x, Played: {track.play_count}x)
//               </li>
//             ))}
//           </ul>
//           <h4>Playlist Analysis:</h4>
//           {results.playlist_analysis && results.playlist_analysis.length > 0 ? (
//             results.playlist_analysis.map((playlist, index) => (
//               <div key={index} className="playlist-analysis my-4">
//                 <h5>{playlist.playlist_name}</h5>
//                 <ul>
//                   {playlist.tracks_to_remove.map((track, i) => (
//                     <li key={i}>
//                       {track.artist} - {track.track} (Skipped: {track.count}x)
//                     </li>
//                   ))}
//                 </ul>
//               </div>
//             ))
//           ) : (
//             <p>No skipped tracks found in playlists.</p>
//           )}
//         </div>
//       )}
//     </div>
//   );
// };

// export default IndexPage;
import React from 'react';

const IndexPage = () => {
  const handleLogin = () => {
    window.location.href = "http://localhost:5001/login";
  };

  return (
    <div>
      <h1>Welcome</h1>
      <a href="http://localhost:5001/login">Login with Spotify</a>
    </div>
  );
};

export default IndexPage;

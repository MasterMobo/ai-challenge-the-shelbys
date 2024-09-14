import React, { useRef } from "react";
import ReactPlayer from "react-player";
import { Button, Box, Typography } from "@mui/material";

function VideoPlayer({ videoUrl, seekTime }) {
  const playerRef = useRef(null);
  console.log(videoUrl);

  const handleSeek = () => {
    if (playerRef.current) {
      // Seek to 30 seconds
      playerRef.current.seekTo(seekTime, "seconds");
    }
  };

  return (
    <Box
      sx={{ padding: "5px", borderRadius: "8px", border: "1px solid #ddd", maxWidth: "100%", }}
    >
      <ReactPlayer
        url={videoUrl}
        onStart={handleSeek}
        ref={playerRef}
        width="100%"
        controls
      />
    </Box>
  );
}

export default VideoPlayer;

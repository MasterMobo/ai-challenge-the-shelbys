import React, { useRef } from "react";
import ReactPlayer from "react-player";
import { Button, Box, Typography } from "@mui/material";

function VideoPlayer({ videoUrl, seekTime }) {
  const playerRef = useRef(null);
  console.log(videoUrl);

  const handleSeek = () => {
    if (playerRef.current) {
      // Seek to 30 seconds
      playerRef.current.seekTo(100, "seconds");
    }
  };

  return (
    <Box
      sx={{ padding: "16px", borderRadius: "8px", border: "1px solid #ddd" }}
    >
      <Typography variant="h6">Video Player</Typography>
      <ReactPlayer
        url={videoUrl}
        onStart={handleSeek}
        ref={playerRef}
        controls
      />
    </Box>
  );
}

export default VideoPlayer;

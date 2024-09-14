import React, { useState } from "react";
import Slider from "react-slick";
import { Typography, Box, Button, Modal } from "@mui/material";
import VideoPlayer from "./VideoPlayer"; // Import the component you want to show in the modal

function FrameResult({
  rank,
  videoNo,
  frameIndex,
  timestamp,
  humanTimestamp,
  thumbnails,
  simScore,
  objects,
  videoUrl, // Pass the video URL as a prop
}) {
  const [open, setOpen] = useState(false); // State to control modal visibility

  // Function to open the modal
  const handleOpen = () => setOpen(true);

  // Function to close the modal
  const handleClose = () => setOpen(false);

  // Carousel settings
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <Box
      sx={{ border: "1px solid #ddd", padding: "16px", borderRadius: "8px" }}
    >
      <Slider {...settings}>
        {thumbnails && thumbnails.map((thumbnail, index) => (
          <div key={index}>
            <img
              src={thumbnail}
              alt={`Thumbnail ${index + 1}`}
              style={{ width: "100%", borderRadius: "8px" }}
            />
          </div>
        ))}
      </Slider>
      <VideoPlayer videoUrl={videoUrl} seekTime={timestamp} />
      <Typography variant="h6">Rank: {rank}</Typography>
      <Typography variant="body2">Video No: {videoNo}</Typography>
      <Typography variant="body2">Frame Index: {frameIndex}</Typography>
      <Typography variant="body2">Timestamp: {humanTimestamp}</Typography>
      {/* <Typography variant="body2">Similarity Score: {simScore}</Typography> */}
      <Typography variant="body2">Objects: {objects}</Typography>

      {/* Button to trigger modal */}
      <Button onClick={handleOpen} variant="contained" color="primary">
        View Video
      </Button>

      {/* Modal for displaying the VideoPlayer */}
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="video-modal-title"
        aria-describedby="video-modal-description"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "50%",
            maxWidth: "100%",
            bgcolor: "background.paper",
            boxShadow: 24,
            p: 4,
            borderRadius: "8px",
          }}
        >
          {/* Display the VideoPlayer component inside the modal */}
          <VideoPlayer videoUrl={videoUrl} seekTime={timestamp} />
          {/* Button to close the modal */}
          <Button
            onClick={handleClose}
            variant="contained"
            color="secondary"
            sx={{ mt: 2 }}
          >
            Close
          </Button>
        </Box>
      </Modal>
    </Box>
  );
}

export default FrameResult;

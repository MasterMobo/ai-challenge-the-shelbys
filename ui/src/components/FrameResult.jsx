import Slider from 'react-slick';
import { Typography, Box } from '@mui/material';

function FrameResult({ rank, videoNo, timestamp, thumbnails, simScore, objects }) {
  // Carousel settings
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <Box sx={{ border: '1px solid #ddd', padding: '16px', borderRadius: '8px' }}>
      <Slider {...settings}>
        {thumbnails.map((thumbnail, index) => (
          <div key={index}>
            <img src={thumbnail} alt={`Thumbnail ${index + 1}`} style={{ width: '100%', borderRadius: '8px' }} />
          </div>
        ))}
      </Slider>
      <Typography variant="h6">Rank: {rank}</Typography>
      <Typography variant="body2">Video No: {videoNo}</Typography>
      <Typography variant="body2">Timestamp: {timestamp}</Typography>
      <Typography variant="body2">Similarity Score: {simScore}</Typography>
      <Typography variant="body2">Objects: {objects}</Typography>
    </Box>
  );
}

export default FrameResult;

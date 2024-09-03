import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import FrameResult from '../components/FrameResult';

function Results() {
  const results = [
    { rank: '1', videoNo: 'V001', timestamp: '00:00:05', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '2', videoNo: 'V002', timestamp: '00:00:10', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '3', videoNo: 'V003', timestamp: '00:00:15', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '4', videoNo: 'V004', timestamp: '00:00:20', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '5', videoNo: 'V005', timestamp: '00:00:25', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '6', videoNo: 'V006', timestamp: '00:00:30', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '7', videoNo: 'V007', timestamp: '00:00:35', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '8', videoNo: 'V008', timestamp: '00:00:40', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '9', videoNo: 'V009', timestamp: '00:00:45', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
    { rank: '10', videoNo: 'V010', timestamp: '00:00:50', thumbnails: ["https://picsum.photos/200", "https://picsum.photos/200", "https://picsum.photos/200"], simScore: '0.9', objects: 'santa claus' },
  ];

  return (
    <Box sx={{ marginTop: '72px', padding: '20px', overflowY: 'scroll', height: 'calc(100vh - 72px)' }}>
      <Typography variant="h6">Retrieval results for: Santa Claus waving</Typography>
      <Typography variant="subtitle1">Filters applied:</Typography>

      <Grid container spacing={2}>
        {results.map((result) => (
          <Grid item xs={12} sm={6} md={4} key={result.rank}>
            <FrameResult
              rank={result.rank}
              videoNo={result.videoNo}
              timestamp={result.timestamp}
              thumbnails={result.thumbnails}
              simScore={result.simScore}
              objects={result.objects}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default Results;

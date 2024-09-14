import React from "react";
import { Grid, Typography, Box } from "@mui/material";
import FrameResult from "../components/FrameResult";

function Results({ results }) {
  return (
    <Box
      sx={{
        marginTop: "72px",
        padding: "20px",
        overflowY: "scroll",
        height: "calc(100vh - 72px)",
      }}
    >
      <Typography variant="h6">
        Retrieval results for: Santa Claus waving
      </Typography>
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
              videoUrl={"../../public/videos/" + result.videoNo + ".mp4"}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default Results;

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

      <Grid container spacing={2}>
        {results && results.map((result, key) => {
          let folder_name = result.video_name.split("_")[0]; 
          return (<Grid item xs={12} sm={6} md={4} key={result.rank}>
            <FrameResult
              rank={key + 1}
              videoNo={result.video_name}
              frameIndex={result.frame_index}
              timestamp={result.pts_time}
              humanTimestamp={result.timestamp}
              thumbnails={result.thumbnails}
              simScore={result.simScore}
              objects={result.objects}
              videoUrl={"../../public/videos/Videos_" + folder_name + "/" + result.video_name + ".mp4"}
            />
          </Grid>)}
        )}
      </Grid>
    </Box>);
    };

export default Results;

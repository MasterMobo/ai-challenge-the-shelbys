import React from "react";
import { Container, Grid, Typography } from "@mui/material";
import SearchBar from "./sections/SearchBar";
import Filters from "./sections/Filters";
import Results from "./sections/Results";
import { useState } from "react";

export default function App() {
  const [results, setResults] = useState([]); // State to hold results

  return (
    <Container maxWidth={false} maxHeight={false}>
      <SearchBar setResults={setResults} />
      <Grid container spacing={2}>
        <Grid item xs={12} sm={3}>
          <Filters />
        </Grid>

        <Grid item xs={12} sm={9}>
          <Results results={results} />
        </Grid>
      </Grid>
    </Container>
  );
}

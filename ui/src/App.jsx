import React from 'react';
import { Container, Grid, Typography } from '@mui/material';
import SearchBar from './sections/SearchBar';
import Filters from './sections/Filters';
import Results from './sections/Results';

export default function App() {
  return (
    <Container maxWidth={false} maxHeight ={false}>
      <SearchBar />
      <Grid container spacing={2}>
        <Grid item xs={12} sm={3}>
          <Filters />
        </Grid>

        <Grid item xs={12} sm={9}>
          <Results />
        </Grid>
      </Grid>
    </Container>
  );
}

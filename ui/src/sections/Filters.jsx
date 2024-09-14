import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { Slider } from '@mui/material';
import FilterAccordion from './FilterAccordion';
import Button from '@mui/material/Button';
import useMediaQuery from '@mui/material/useMediaQuery';
import FilterModal from './FilterModal';
import FilterListIcon from '@mui/icons-material/FilterList';

const style = {
  py: 0,
  width: '100%',
  height: '100vh',
  maxWidth: 360,
  top: 80,
  left: 0,
  border: '1px solid',
  borderColor: 'divider',
  backgroundColor: 'background.paper',
  display: 'flex',
  flexDirection: 'column',
  borderRadius: 4,
  zIndex: 1000,
};

const filtersData = [
  {
    title: "Location/Place",
    options: ["New York", "Los Angeles", "Chicago"]
  },
  {
    title: "Objects",
    options: ["Car", "Bike", "Plane"]
  },
  {
    title: "Colors",
    options: ["Red", "Blue", "Green"]
  },
];

const renderFilterContent = () => (
  <>
    {filtersData.map((filter, index) => (
      <FilterAccordion key={index} title={filter.title}>
        <FormGroup>
          {filter.options.map((option, idx) => (
            <FormControlLabel
              key={idx}
              control={<Checkbox />}
              label={option}
            />
          ))}
        </FormGroup>
      </FilterAccordion>
    ))}

    <FilterAccordion title="Video Length">
      <Typography gutterBottom>Length</Typography>
      <Slider
        defaultValue={30}
        aria-labelledby="discrete-slider"
        valueLabelDisplay="auto"
        step={10}
        marks
        min={0}
        max={100}
      />
    </FilterAccordion>
  </>
);

function Filters() {
  const [open, setOpen] = React.useState(false);
  const isSmallScreen = useMediaQuery((theme) => theme.breakpoints.down('sm'));  

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <Box>
      {isSmallScreen ? (
        <>
        <Box sx={{ position: 'relative', zIndex: 10, marginTop: '80px' }}>
          <Button
            variant="contained"
            startIcon={<FilterListIcon />} 
            onClick={handleOpen}
          >
            Filters
          </Button>
          <FilterModal open={open} handleClose={handleClose} renderContent={renderFilterContent} />
        </Box>
      </>
      ) : (
        <List sx={style}>
          <Typography variant="h4" sx={{ p: 2 }}>
            Filters
          </Typography>
          {renderFilterContent()}
        </List>
      )}
    </Box>
  );
}

export default Filters;

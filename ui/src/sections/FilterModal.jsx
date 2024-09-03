import * as React from 'react';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

const modalStyle = {
  position: 'fixed',
  bottom: 0,
  left: 0,
  width: '95%', 
  maxWidth: '100%',  
  margin: '0 auto',  
  bgcolor: 'background.paper',
  boxShadow: 24,
  borderTopLeftRadius: '16px',
  borderTopRightRadius: '16px',
  p: 4,
  maxHeight: '90vh',
  overflow: 'auto',
};

function FilterModal({ open, handleClose, renderContent }) {
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="filter-modal-title"
      aria-describedby="filter-modal-description"
    >
      <Box sx={modalStyle}>
        <Typography variant="h6" component="h2" id="filter-modal-title">
          Filters
        </Typography>
        {renderContent()}
        <Button variant="contained" sx={{ mt: 2 }} onClick={handleClose}>Apply Filters</Button>
      </Box>
    </Modal>
  );
}

export default FilterModal;

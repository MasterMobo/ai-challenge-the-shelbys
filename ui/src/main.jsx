import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider, createTheme } from '@mui/material/styles';
import App from './App.jsx'
import './index.css'
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";

const theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,    // default
      sm: 900,  // change this value to trigger 'sm' earlier
      md: 1200,  // default
      lg: 1536, // default
      xl: 1800, // default
    },
  },
  palette: {
    primary: {
      main: '#1976d2', // Blue
    },
    secondary: {
      main: '#dc004e', // Pink
    },
    background: {
      default: '#f4f4f4', // Light gray background
      paper: '#ffffff',   // White background for paper elements
    },
    divider: '#e0e0e0',   // Light gray divider
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </StrictMode>,
)

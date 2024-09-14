import * as React from "react";
import { styled, alpha } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import InputBase from "@mui/material/InputBase";
import SearchIcon from "@mui/icons-material/Search";
import Button from "@mui/material/Button";
import { useState } from "react";
import axios from "axios";

const Search = styled("div")(({ theme }) => ({
  position: "relative",
  borderRadius: "50px",
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  "&:hover": {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  width: "100%",
  maxWidth: "400px",
  [theme.breakpoints.up("sm")]: {
    width: "auto",
    maxWidth: "600px",
  },
  [theme.breakpoints.up("md")]: {
    maxWidth: "800px",
  },
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: "100%",
  position: "absolute",
  pointerEvents: "none",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: "inherit",
  "& .MuiInputBase-input": {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("md")]: {
      width: "40ch",
    },
  },
}));

export default function SearchBar({ setResults }) {
  const [query, setQuery] = useState(""); // State for search query
  const [fileName, setFileName] = useState("");

  // Function to handle input changes
  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleFileNameChange = (event) => {
    setFileName(event.target.value);
  };

  // Function to handle search action
  const handleSearch = async () => {
    if (query.trim() === "") {
      alert("Please enter a search query"); // Optional: Validation
      return;
    }

    try {
      // const response = await axios.get(`http://127.0.0.1:3000/search?query=${query}&out=${out}`);
      const response = await axios.get(
        `http://127.0.0.1:3000/search?query=${query}&out=${fileName}`
      );

      // Check the response data
      console.log('Search results:', response.data);
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
      if (error.response) {
        // The request was made and the server responded with a status code outside the 2xx range
        console.log("Backend error:", error.response.data);
        alert(`Error: ${error.response.data.error || "Something went wrong"}`);
      } else if (error.request) {
        // The request was made but no response was received
        console.log("No response received:", error.request);
        alert(
          "No response from server. Please check if the backend is running."
        );
      } else {
        // Something happened in setting up the request
        console.log("Error setting up request:", error.message);
      }
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="fixed">
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ display: { xs: "none", sm: "block" } }}
          >
            Video Browser
          </Typography>

          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexGrow: 1,
            }}
          >
            <Search sx={{ marginRight: 2, width: "100%" }}>
              <SearchIconWrapper>
                <SearchIcon />
              </SearchIconWrapper>
              <StyledInputBase
                placeholder="Enter text query…"
                inputProps={{ "aria-label": "search" }}
                value={query} // Bind input value to state
                onChange={handleInputChange} // Update state on input change
              />
            </Search>

            <Search sx={{ marginRight: 2, width: "100%" }}>
              <SearchIconWrapper>
                <SearchIcon />
              </SearchIconWrapper>
              <StyledInputBase
                placeholder="Enter file name…"
                inputProps={{ "aria-label": "search" }}
                value={fileName} // Bind input value to state
                onChange={handleFileNameChange} // Update state on filename change
              />
            </Search>

            <Button //search button
              sx={{ borderRadius: "50px" }}
              variant="contained"
              onClick={handleSearch} // Trigger search on button click
            >
              Search
            </Button>
          </Box>
        </Toolbar>
      </AppBar>
    </Box>
  );
}

import React, { useEffect, useState } from "react";
import styled from "styled-components";
import axios from 'axios';
import { Bar } from 'react-chartjs-2';


const Graph = (props) => {
    const [movieData, setMovieData] = useState([]);

    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch("http://127.0.0.1:8000/graph");
          if (!response.ok) {
            throw new Error("Failed to fetch data");
          }
          else{
            console.log("OK")
          }
          const data = await response.json();
          setMovieData(data);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };

      fetchData();
    }, []);
};

export default Graph;

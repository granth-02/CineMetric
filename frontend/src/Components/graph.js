import React, { useEffect, useState } from "react";
import styled from "styled-components";
import axios from 'axios';
import { Bar, Line, PolarArea } from 'react-chartjs-2';
import Chart from 'chart.js/auto';


const Graph = (props) => {
    const [movieData, setMovieData] = useState([]);
    const [chartInstance, setChartInstance] = useState(null);

    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch("http://127.0.0.1:8000/graph");
          if (!response.ok) {
            throw new Error("Failed to fetch data");
          }
          const data = await response.json();
          setMovieData(data);
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };

      fetchData();
    }, []);

    useEffect(() => {
      if (chartInstance) {
        chartInstance.destroy();
      }

      const generateChartData = () => {
        const genreRatings = {};
        const titleAvgVotes = {};
        const releaseYearCount = {};
        movieData.forEach((movie) => {
          // Genre vs Average Rating
          const genre = movie["Genres"];
          const rating = movie["Average Vote"];
          if (!genreRatings[genre]) {
            genreRatings[genre] = { total: rating, count: 1 };
          } else {
            genreRatings[genre].total += rating;
            genreRatings[genre].count += 1;
          }

          // Title vs Average Vote
          const title = movie["Title"];
          const avgVote = movie["Average Vote"];
          titleAvgVotes[title] = avgVote;

          // Distribution of movies by release year
          const releaseYear = movie["Release Year"];
          if (!releaseYearCount[releaseYear]) {
            releaseYearCount[releaseYear] = 1;
          } else {
            releaseYearCount[releaseYear] += 1;
          }
        });

        const genreLabels = Object.keys(genreRatings);
        const genreData = genreLabels.map(genre => genreRatings[genre].total / genreRatings[genre].count);

        const titleLabels = Object.keys(titleAvgVotes);
        const titleData = titleLabels.map(title => titleAvgVotes[title]);

        const releaseYearLabels = Object.keys(releaseYearCount);
        const releaseYearData = releaseYearLabels.map(year => releaseYearCount[year]);

        return {
          genreData: {
            labels: genreLabels,
            datasets: [
              {
                label: "Average Rating by Genre",
                data: genreData,
                backgroundColor: "rgba(75,192,192,0.2)",
                borderColor: "gold",
                borderWidth: 1,
              },
            ],
          },
          titleData: {
            labels: titleLabels,
            datasets: [
              {
                label: "Average Vote by Title",
                data: titleData,
                fill: false,
                borderColor: "gold",
                tension: 0.1
              },
            ],
          },
          releaseYearData: {
            labels: releaseYearLabels,
            datasets: [
              {
                label: "Number of Movies Released",
                data: releaseYearData,
                backgroundColor: [
                  'rgba(255, 99, 132, 0.6)',
                  'rgba(54, 162, 235, 0.6)',
                  'rgba(255, 206, 86, 0.6)',
                  'rgba(75, 192, 192, 0.6)',
                  'rgba(153, 102, 255, 0.6)',
                  'rgba(255, 159, 64, 0.6)',
                  'rgba(255, 99, 132, 0.6)'
                ],
                borderColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)',
                  'rgba(153, 102, 255, 1)',
                  'rgba(255, 159, 64, 1)',
                  'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1,
              },
            ],
          }
        };
      };

      if (movieData.length > 0) {
        const ctxGenre = document.getElementById("genreRatingChart");
        if (ctxGenre) {
          const newGenreChartInstance = new Chart(ctxGenre, {
            type: 'bar',
            data: generateChartData().genreData,
            options: {
              maintainAspectRatio: false,
              scales: {
                yAxes: [
                  {
                    ticks: {
                      beginAtZero: true,
                    },
                  },
                ],
              },
            },
          });
          setChartInstance(newGenreChartInstance);
        }

        const ctxTitle = document.getElementById("titleAvgVoteChart");
        if (ctxTitle) {
          const newTitleChartInstance = new Chart(ctxTitle, {
            type: 'line',
            data: generateChartData().titleData,
            options: {
              maintainAspectRatio: false,
              scales: {
                yAxes: [
                  {
                    ticks: {
                      beginAtZero: true,
                    },
                  },
                ],
              },
            },
          });
          setChartInstance(newTitleChartInstance);
        }

        const ctxReleaseYear = document.getElementById("releaseYearChart");
        if (ctxReleaseYear) {
          const newReleaseYearChartInstance = new Chart(ctxReleaseYear, {
            type: 'polarArea',
            data: generateChartData().releaseYearData,
            options: {
              maintainAspectRatio: false,
              scale: {
                ticks: {
                  beginAtZero: true,
                  stepSize: 1,
                },
              },
            },
          });
          setChartInstance(newReleaseYearChartInstance);
        }
      }
    }, [movieData]);

    return (
      <div>
        <GridContainer>
          <ChartContainer1>
            <h1>Genre vs Average Rating</h1>
            <canvas id="genreRatingChart"></canvas>
          </ChartContainer1>
          <ChartContainer2>
            <h1>Title vs Average Vote</h1>
            <canvas id="titleAvgVoteChart"></canvas>
          </ChartContainer2>
          <ChartContainer3>
            <h1>Distribution of Movies by Release Year</h1>
            <canvas id="releaseYearChart"></canvas>
          </ChartContainer3>
        </GridContainer>
      </div>
    );
};

const GridContainer = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
  padding-top: 100px;
  padding-left: 20px;
`;

const ChartContainer1 = styled.div`
  height: 400px;
  width: 600px;
  grid-column: 1 / span 1;
  grid-row: 1 / span 1;
`;

const ChartContainer2 = styled.div`
  height: 400px;
  width: 800px;
  padding-top: 100px;
  grid-column: 1 / span 2;
  grid-row: 2 / span 2;
`;

const ChartContainer3 = styled.div`
  height: 400px;
  width: 600px;
  grid-column: 2 / span 1;
  grid-row: 1 / span 1;
`;

export default Graph;

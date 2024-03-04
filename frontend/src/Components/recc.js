import React, { useEffect, useState } from "react";
import styled from "styled-components"

const Reccomed = (props) => {
    const [movieRecc, setMovieRecc] = useState([]);
    
    useEffect( () => {
        const fetchRecc = async() => {
            try{
                const response = await fetch("http://127.0.0.1:8000/recc");
                if(!response.ok){
                    throw new Error("Failed to fetch data");
                }else{console.log('Clear')}
                const recc = await response.json();
                setMovieRecc(recc.reccomendations);
            } catch(error){
                console.error("Error fetching data", error)
            }
        }
        fetchRecc() 
    }, []);


    return(
        <div>
            <h1 style={{marginTop: "150px", color: "gold"}}>Your Reccomendations</h1>
            <Card>
            
            {movieRecc.map((movie, index) => (
                <Wrap key={index}>
                    <img src={movie.PosterURL} />
                    <h2>{movie.Title}</h2>
                    <h3>Rating: {movie.Rating}</h3>
                </Wrap>    
                    ))}
            </Card>
        </div>    
    )
}


const Card = styled.div`
    display: grid;
    grid-gap: 30px;
    gap: 30px;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    margin-top: 40px;
    margin-left: 10px;
    margin-right: 10px;
    margin-bottom: 30px;
`

const Wrap = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 0;
  border-radius: 10px;
  background-color: rgb(42, 21, 105, 0.3);
  cursor: pointer;

  &:hover {
    transition: all 500ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
    border: 5px solid gold;
  }

  img {
    margin-top: 10px;
    border-radius: 5px;
    width: 95%;
  }

  h2 {
    color: gold;
    text-align: center;
  }

  h3 {
    margin-top: -10px;
    color: #a4cbe2;
    text-align: center;
  }
`;

export default Reccomed;
import { useEffect, useState } from "react";
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
                setMovieRecc(recc);
            } catch(error){
                console.error("Error fetching data", error)
            }
        }
        fetchRecc() 
    }, []);

    return(
        <>
            <h1>Recc</h1>
        </>
    )
}

export default Reccomed;
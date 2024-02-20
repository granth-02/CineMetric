import styled from "styled-components"

const Welcome = (props) => {
    return (
        <Intro>
            
            <span>WELCOME<br /><br />To<br /><br />CineMetric
            </span>
        </Intro>
      )
    }
    
    const Intro = styled.div`
        img{
            width: 100vw;
            margin-top: 80px;
            z-index: -1;
            
        }
        span{
            display: flex;
            text-align: center;
            align-items: center; 
            justify-content: center; 
            position: relative;
            margin-top: 10vw;
            color: gold;
            font-size: 5vw;
            letter-spacing: 20px;
            
    
        }
    `

export default Welcome;
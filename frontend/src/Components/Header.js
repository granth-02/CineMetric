import styled from "styled-components"
import headimg from '../Img/logo.png'

const Header = (props) => {
    return(
        <Nav>
            <Logo>
                <a href="/">
                    <Helog src = {headimg} />
                </a>
            </Logo>
            <NavMenu>
                <a href="/recc">
                    <span>Reccomendations</span>
                </a>
                <a href="/graph">
                    <span>Graph</span>
                </a>
            </NavMenu>
        </Nav>
        
    )
}

const Logo = styled.a`
    padding: 0;
    margin-top: 0px;
    max-height: 127px;
    font-size: 0;
    display: inline-block;
    img{
        display: block;
        
    }
    

`

const Nav = styled.nav`
    position: fixed;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    height: 100px;
    background-color: #090b13;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    z-index: 3;
    letter-spacing: 1.5px;
`

const Helog = styled.img`
    width: 200px;
    padding-bottom: 10vw;
`

const NavMenu = styled.div`
    align-items: center;
    display: flex;
    flex-flow: row nowrap;
    height: 100%;
    justify-content: flex-end;
    margin: 0px;
    padding: 0px;
    position: relative;
    margin-right: auto;
    margin-left: 35px;

    a{
        display: flex;
        align-items: center;
        padding: 0 12px;
        text-decoration: none;

    

    span{
        color: rgb(249, 249, 249);
        font-size: 26px;
        letter-spacing: 1.42px;
        line-height: 1.08;
        padding: 2px 0px;
        white-space: nowrap;
        position: relative;

        &:before{
            background-color: gold;
            border-radius: 0px 0px 4px 4px;
            bottom: -6px;
            content: "";
            height: 2px;
            left: 0px;
            opacity: 0;
            position: absolute;
            right: 0px;
            transform-origin: left center;
            transform: scaleX(0);
            transition: all 250ms cubic-bezier(0.25, 0.46, 0.45, 0.90) 0s;
            visibility: hidden;
            width: auto;
        }
    }

    &:hover{
        span:before{
            transform: scaleX(1);
            visibility: visible;
            opacity: 1;
            
            
        }
    }
}
    
    


    @media (max-width: 768px) {
        display: none;
    }
`



export default Header;
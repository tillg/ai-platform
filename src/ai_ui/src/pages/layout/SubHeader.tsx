
import { styled } from "styled-components";



export const SubHeader = styled.section`
    display: flex;
    background-color: #222222;
    color: #f2f2f2;
    align-items: center;
    padding-left: 52px;
    text-decoration: none;
    justify-content: flex-start; /* Aligns items to the left */
    gap: 50px; /* Sets 15px of space between the items */

    a {
        color: inherit; /* Makes the link color the same as the parent's color */
        text-decoration: none; /* Removes underline from links */
    }

`;

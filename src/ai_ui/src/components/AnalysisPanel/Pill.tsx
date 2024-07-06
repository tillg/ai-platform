
import { styled } from "styled-components";


export const Pill = styled.section`
    background-color: ${props => props.theme.pill.backgroundColor};
    color:  ${props => props.theme.pill.color};
    font-size: ${props => props.theme.pill.fontSize};
    padding: ${props => props.theme.pill.padding};
    border-radius: ${props => props.theme.pill.borderRadius};
    margin-bottom: ${props => props.theme.pill.marginBottom};
        // border: 1px solid #000; /* Default border style */
`;

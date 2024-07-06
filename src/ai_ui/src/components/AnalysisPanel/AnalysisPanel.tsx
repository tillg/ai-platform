
import { styled } from "styled-components";


export const AnalysisPanel = styled.section`
    background-color: ${props => props.theme.analysisPanel.backgroundColor};
    color:  ${props => props.theme.analysisPanel.color};
    font-size: ${props => props.theme.analysisPanel.fontSize};
    padding: ${props => props.theme.analysisPanel.padding};
    border-radius: ${props => props.theme.analysisPanel.borderRadius};
    margin-bottom: ${props => props.theme.analysisPanel.marginBottom};
    position: ${props => props.theme.analysisPanel.position};
    font-family: ${props => props.theme.analysisPanel.fontFamily};
    word-wrap: ${props => props.theme.analysisPanel.wordWrap};
    padding-top: ${props => props.theme.analysisPanel.paddingTop};
    padding-bottom: ${props => props.theme.analysisPanel.paddingBottom};
    
`;

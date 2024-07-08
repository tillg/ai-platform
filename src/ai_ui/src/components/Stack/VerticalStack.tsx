import styled from 'styled-components';

// Define a styled div that accepts a gap prop for vertical stacking
export const VerticalStack = styled.div<{ gap?: string }>`
  display: flex;
  flex-direction: column; 
  gap: ${props => props.gap || '10px'}; 
`;
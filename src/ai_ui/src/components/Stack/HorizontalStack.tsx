import styled from 'styled-components';

// Define a styled div that accepts a gap prop
export const HorizontalStack = styled.div<{ gap?: string }>`
  display: flex;
  flex-direction: row;
  gap: ${props => props.gap || '10px'};
`;
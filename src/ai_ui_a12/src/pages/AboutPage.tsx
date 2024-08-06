import { AboutPageContent } from '../components/AboutPageContent';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 20px;
`;

const StyledAboutPageContent = styled(AboutPageContent)`
  max-width: 700px;
  width: 100%;
`;

export const AboutPage = () => {
  return (
    <Container>
      <StyledAboutPageContent />
    </Container>
  );
};
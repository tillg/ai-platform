import styled from 'styled-components';
import MarkdownRenderer from '../components/MarkdownRenderer';
import aboutPageMd from '../content/aboutPage/aboutPage.md';
import { AI_BRAIN_URL, LLM_WRAPPER_URL, AI_ORCHESTRATION_URL } from '../constants';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 20px;
`;

const StyledMarkdownRenderer = styled(MarkdownRenderer)`
  max-width: 700px;
  width: 100%;
`;

const replacements = [
  { tag: '{{AI_BRAIN_URL}}', value: AI_BRAIN_URL },
  { tag: '{{LLM_WRAPPER_URL}}', value: LLM_WRAPPER_URL },
  { tag: '{{AI_ORCHESTRATION_URL}}', value: AI_ORCHESTRATION_URL },
];
export const AboutPage = () => {
  return (
    <Container>
      <StyledMarkdownRenderer markdownFile={aboutPageMd} replacements={replacements} />
    </Container>
  );
};
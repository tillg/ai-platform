import { render, screen } from '@testing-library/react';
import App from './App';


// Increase timeout for all tests in this file
jest.setTimeout(30000); // Set to 30 seconds

test('renders learn react link', async () => {
  render(<App />);
  const linkElements = await screen.findAllByText(/AI Platform/i, {}, { timeout: 10000 }); // Adjust timeout as necessary
  // Assert that there is at least one element with "AI Platform"
  expect(linkElements.length).toBeGreaterThan(0);
});
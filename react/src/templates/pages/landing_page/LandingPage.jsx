// Landing Page for the website, edit this page to change the landing page.

import { React } from 'react';
import { Link } from 'react-router-dom';
import { Card, Button } from 'react-bootstrap';
import './landing_page.css';

const LandingPage = () => {
  return (
    <div>
      <Card>
        <Card.Header>Welcome to the website!</Card.Header>
        <Card.Body>
          <Card.Title>Not logged in</Card.Title>
          <Card.Text>
            This is a simple React app that uses Flask as a backend, edit this page in src/templates/pages/LandingPage.jsx.
            Please login to get started.
          </Card.Text>
          <Link to='/login'>
            <Button variant="primary">Login</Button>
          </Link>
        </Card.Body>
      </Card>
    </div>
  );
}

export default LandingPage;
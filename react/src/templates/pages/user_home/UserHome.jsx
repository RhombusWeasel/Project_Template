// Users home page, only accessible if logged in.  Edit this page to change the users home page.

import { React } from 'react';
import { Card } from 'react-bootstrap';
import './user_home.css';

const UserHome = ({permissions, context, setContext}) => {
  return (
    <div>
      <Card>
        <Card.Header>Home</Card.Header>
        <Card.Body>
          <Card.Title>Welcome to the React App</Card.Title>
          <Card.Text>
            This is a users homepage, edit this page in src/templates/pages/UserHome.jsx.
          </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
}

export default UserHome;
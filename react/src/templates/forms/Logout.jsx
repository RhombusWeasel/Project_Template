// A basic logout page informing the user they have sucessfully logged out.

import { React, useState, useEffect } from 'react';
import { Card } from 'react-bootstrap';
import axios from 'axios';
import './form.css';

const Logout = ({ setLoggedIn, setPermissions }) => {
  let [sent, setSent] = useState(false);

  useEffect(() => {
    if (!sent) {
      axios.get('/user_logout').then(res => {
        if (res.status === 200) {
          setLoggedIn(false);
          setPermissions({
            'admin': false,
            'trusted': false,
            'user': false
          });
          setSent(true);
        }
      });
    }
  });

  return (
    <div>
      <Card>
        <Card.Header>Logout</Card.Header>
        <Card.Body>
          <Card.Title>You have successfully logged out.</Card.Title>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Logout;
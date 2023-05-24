import React, { useState } from 'react';
import axios from 'axios';
import { Card, Form, Button } from 'react-bootstrap';
import '../../App.css'

const PasswordResetForm = () => {
  const [username, setUsername] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('/reset-password', { username });
      console.log(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Card className='App-form'>
      <Card.Header>Reset Password</Card.Header>
      <Card.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter email" value={username} onChange={e => setUsername(e.target.value)} />
          </Form.Group>
          <Button variant="primary" type="submit">
            Reset Password
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default PasswordResetForm;
import React, { useState } from 'react';
import axios from 'axios';
import { Card, Form, Button } from 'react-bootstrap';
import './form.css';

const LoginForm = ({ setLoggedIn, setPermissions }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('/user_login', { username, password }, { headers: { 'Content-Type': 'application/json' } });
      if(res.status === 200) {
        setLoggedIn(true);
        const perms = await axios.get('/user_permissions');
        if (perms.status === 200) {
          setPermissions(perms.data);
        }
      }
      window.location.location = '/';
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className='form'>
      <Card>
        <Card.Header>Login</Card.Header>
        <Card.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" placeholder="Enter email" value={username} onChange={e => setUsername(e.target.value)} />
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <Button variant="primary" type="submit">
              Login
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
};

export default LoginForm;
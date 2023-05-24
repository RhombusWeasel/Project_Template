import { React } from 'react';
import { Link } from 'react-router-dom';
import './nav.css';

const NavBar = ({ isLoggedIn, permissions }) => {
  return (
    <nav>
      { isLoggedIn
        ? <div className='nav-header'>
            <Link className='nav-header-link' to="/">Home</Link>
            <Link className='nav-header-link' to="/logout">Logout</Link>
            { permissions.admin && <Link className='nav-header-link' to="/admin">Admin</Link> }
          </div>
        : <div className='nav-header'>
            <Link className='nav-header-link' to="/">Home</Link>
            <Link className='nav-header-link' to="/login">Login</Link>
            <Link className='nav-header-link' to="/register">Register</Link>
          </div>
      }
    </nav>
  );
}

export default NavBar;
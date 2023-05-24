import { React } from 'react'
import UserList from './UserList'

const AdminPage = () => {
  return (
    <div className='admin-main'>
      <h1>Admin Panel</h1>
      <div className='admin-body'>
        <UserList />
      </div>
    </div>
  )
}

export default AdminPage
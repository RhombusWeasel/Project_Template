import { React, useState, useEffect } from 'react'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCheck, faXmark, faUser, faUserPlus, faSkull, faAt } from '@fortawesome/free-solid-svg-icons'
import axios from 'axios'

library.add(faCheck, faXmark, faUser, faUserPlus, faSkull, faAt)

const CheckToggle = ({ checked, lvl, uid, onClick }) => {
  return (
    <div
      className='check-toggle'
      onClick={() => {
        onClick(lvl, uid)
      }}
    >
      {checked
        ? <FontAwesomeIcon
          icon="check"
          />
        : <FontAwesomeIcon
          icon="xmark"
        />
      }
    </div>
  )
}

const UserList = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect( () => {
    if (loading) {
      axios.get('/get_users').then(res => {
        if (res.status === 200) {
          let u = res.data
          setUsers(u)
          setLoading(false)
        }
      })
    }
  });

  const setPerms = (lvl, id, val) => {
    const updatedUsers = users.map(user => {
      if (user._id === id) {
        return {
          ...user,
          permissions: {
            ...user.permissions,
            [lvl]: val
          }
        }
      }
      return user;
    });
    setUsers(updatedUsers);
  }

  const togglePerms = async (lvl, id) => {
    const user = users.find(u => u._id === id);
    if (!user) {
      return;
    }
    if (!user.permissions[lvl]) {
      await axios.post(`/grant_perms`, { username: id, perm: lvl }).then(res => {
        if (res.status === 200) {
          setPerms(lvl, id, true)
          console.log(res.data)
        }
      })
    } else {
      await axios.post(`/revoke_perms`, { username: id, perm: lvl }).then(res => {
        if (res.status === 200) {
          setPerms(lvl, id, false)
          console.log(res.data)
        }
      })
    }
  }
    
  return (
    <div className='admin-user-list'>
      <h2 className='user-header'>Users</h2>
        {loading
          ? <div>Loading...</div>
          : (
          <table className='user-table'>
              <thead>
                <tr>
                  <th className='user-table-head'>Email</th>
                  <td className='user-table-head-icon' title='User'>
                    <FontAwesomeIcon icon="user" />
                  </td>
                  <td className='user-table-head-icon' title='Trusted'>
                    <FontAwesomeIcon icon="user-plus" />
                  </td>
                  <td className='user-table-head-icon' title='Admin'>
                    <FontAwesomeIcon icon="skull" />
                  </td>
                  <th className='user-table-head'>Last Login</th>
                </tr>
            </thead>
            <tbody>
              {users.map((u, i) => {
                if (typeof u.permissions === 'string') {
                  u.permissions = JSON.parse(u.permissions)
                }
                return (
                  <tr key={i}>
                    <td className='user-table-data'>{u._id}</td>
                    <td className='user-table-data-icon'><CheckToggle
                      checked={u.permissions.user}
                      lvl='user'
                      uid={u._id}
                      onClick={togglePerms} />
                    </td>
                    <td className='user-table-data-icon'><CheckToggle
                      checked={u.permissions.trusted}
                      lvl='trusted'
                      uid={u._id}
                      onClick={togglePerms} />
                    </td>
                    <td className='user-table-data-icon'><CheckToggle
                      checked={u.permissions.admin}
                      lvl='admin'
                      uid={u._id}
                      onClick={togglePerms} />
                    </td>
                    <td className='user-table-data'>{u.last_login}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )
      }
    </div>
  )
}

export default UserList
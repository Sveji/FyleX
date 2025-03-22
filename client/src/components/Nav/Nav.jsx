import './nav.less'
import logo from '../../img/logo.png'
import { useContext } from 'react'
import { DataContext } from '../../context/DataContext'
import { Link } from 'react-router-dom'

const Nav = () => {
    // Gets global data from the context
    const { navigate, access, setAccess, setRefresh } = useContext(DataContext)



    // Deletes the tokens from local storage and resets the variables
    const handleLogOut = () => {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        setAccess(null)
        setRefresh(null)
    }



    return (
        <div className="navbar">
            <div onClick={() => navigate('/')} className="logo-container">
                <img src={logo} className='logo' />
                <p className='logo-label'>FyleX</p>
            </div>
            {
                access ?
                <Link onClick={handleLogOut} className='log'>Log out</Link>
                :
                <Link to='/login' className='log'>Log in</Link>
            }
        </div>
    )
}

export default Nav
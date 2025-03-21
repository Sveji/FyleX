import './nav.less'
import Logo from '../../img/logo.png'

const Nav = () => {

    return (
        <>
            <div className="navbar">
                <div className='logo-container'>
                    <img src={Logo} className='logo' />

                </div>
                <div className='log'>Log in</div>
            </div>
        </>
    )
}

export default Nav
import { useContext, useState } from "react"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"
import { MdOutlineMailOutline } from "react-icons/md"
import './activateMessage.less'
import { Link } from "react-router-dom"

const ActivateMessage = () => {
    // Gets global data from the context
    const { navigate } = useContext(DataContext)



    // Holds the state for the popup
    const [shown, setShown] = useState(true)

    const handleClosePopUp = () => {
        setShown(false)
        setTimeout(() => {
            navigate('/')
        }, 300)
    }



    return (
        <PopUp classes={'account-box'} shown={shown} onClose={handleClosePopUp}>
            <MdOutlineMailOutline className="icon" />

            <h1>Activate account</h1>
            <p className="activate-message-text">Click the link we sent on your email to activate your account. Log in once you're done.</p>

            <Link to='/login'><button className="btn">Log in</button></Link>
        </PopUp>
    )
}

export default ActivateMessage
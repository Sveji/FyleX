import { useContext, useEffect, useState } from "react"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"
import { MdOutlineMailOutline } from "react-icons/md"
import { Link } from "react-router-dom"



const EmailMessage = ({ title, message }) => {
    // Gets global data from the context
    const { access, navigate } = useContext(DataContext)



    // Checks if the user is logged in
    useEffect(() => {
        if(access) navigate('/')
    }, [access])



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

            <h1>{title}</h1>
            <p className="activate-message-text">{message}</p>

            <Link to='/login'><button className="btn">Log in</button></Link>
        </PopUp>
    )
}

export default EmailMessage
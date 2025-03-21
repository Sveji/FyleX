import { useContext, useEffect, useState } from "react"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"
import { useParams } from "react-router-dom"

const ForgotPass = () => {
    // Gets parameters from the url
    const { uidb, token } = useParams()



    // Gets global data from the context
    const { access, navigate, crud } = useContext(DataContext)



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



    // Holds the state for the email
    const [password, setPassword] = useState("")
    const [error, setError] = useState(null)



    // Sends a forgot pass request to the backend
    const handleSubmit = async () => {
        const response = await crud({
            url: `/api/user/reset-password/${uidb}/${token}/`,
            method: 'post',
            body: {
                password
            }
        })

        console.log(response)

        if(response.status == 400 || response.status == 404) setError(response.response.data.error)
        if(response.status == 200) navigate('/login')
    }



    return (
        <PopUp classes={'account-box'} shown={shown} onClose={handleClosePopUp}>
            <div className="text-box">
                <h1>Forgot password</h1>
                <p>Enter your new password here.</p>
                {
                    error &&
                    <p className="error">{error}</p>
                }
            </div>

            <div className="input-container">
                <input
                    type="text"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <button onClick={handleSubmit} className="btn">Save</button>
            </div>
        </PopUp>
    )
}

export default ForgotPass
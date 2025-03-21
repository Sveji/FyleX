import { useContext, useEffect, useState } from "react"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"

const ForgotPass = () => {
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
    const [email, setEmail] = useState("")
    const [error, setError] = useState(null)



    // Sends a forgot pass request to the backend
    const handleSubmit = async () => {
        const response = await crud({
            url: '/api/user/forgot-password/',
            method: 'post',
            body: {
                email
            }
        })

        console.log(response)

        if(response.status == 400 || response.status == 404) setError(response.response.data.error)
        if(response.status == 200) navigate('/forgot-pass-message')
    }



    return (
        <PopUp classes={'account-box'} shown={shown} onClose={handleClosePopUp}>
            <div className="text-box">
                <h1>Forgot password</h1>
                <p>Enter your account email to reset your password.</p>
                {
                    error &&
                    <p className="error">{error}</p>
                }
            </div>

            <div className="input-container">
                <input
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
                <button onClick={handleSubmit} className="btn">Reset</button>
            </div>
        </PopUp>
    )
}

export default ForgotPass
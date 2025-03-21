import { useContext, useState } from "react"
import AccountForm from "../AccountBox/AccountForm"
import PopUp from "../PopUp/PopUp"
import { DataContext } from "../../context/DataContext"

const Register = () => {
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



    // Holds the state for the form
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")



    // Sends a register request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()
    }



    return (
        <PopUp classes={'account-box'} shown={shown} onClose={handleClosePopUp}>
            <AccountForm
                handleSubmit={handleSubmit}
                title="Register"
                text="Register an account to analyze your documents."
                inputs={[
                    {
                        type: "email",
                        value: email,
                        setValue: setEmail,
                        placeholder: "Email"
                    },
                    {
                        type: "text",
                        value: username,
                        setValue: setUsername,
                        placeholder: "Username"
                    },
                    {
                        type: "password",
                        value: password,
                        setValue: setPassword,
                        placeholder: "Password"
                    }
                ]}
                btn="Register"
                link={{
                    text: "Already have an account?",
                    label: "Log in",
                    route: "/login"
                }}
            />
        </PopUp>
    )
}

export default Register
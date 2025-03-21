import { useContext, useState } from "react"
import AccountForm from "../AccountBox/AccountForm"
import PopUp from "../PopUp/PopUp"
import { DataContext } from "../../context/DataContext"

const Login = () => {
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
    const [password, setPassword] = useState("")



    // Sends a login request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()
    }



    return (
        <PopUp classes={'account-box'} shown={shown} onClose={handleClosePopUp}>
            <AccountForm
                handleSubmit={handleSubmit}
                title="Log in"
                text="Log in to your account to analyze your documents."
                inputs={[
                    {
                        type: "email",
                        value: email,
                        setValue: setEmail,
                        placeholder: "Email"
                    },
                    {
                        type: "password",
                        value: password,
                        setValue: setPassword,
                        placeholder: "Password"
                    }
                ]}
                btn="Log in"
                link={{
                    text: "Don't have an account?",
                    label: "Register",
                    route: "/register"
                }}
            />
        </PopUp>
    )
}

export default Login
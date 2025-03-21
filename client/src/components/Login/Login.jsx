import { useState } from "react"
import AccountForm from "../AccountBox/AccountForm"

const Login = () => {
    // Holds the state for the form
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")



    // Sends a login request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()
    }



    return (
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
    )
}

export default Login
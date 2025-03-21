import { useState } from "react"
import AccountForm from "../AccountBox/AccountForm"

const Register = () => {
    // Holds the state for the form
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")



    // Sends a register request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()
    }



    return (
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
    )
}

export default Register
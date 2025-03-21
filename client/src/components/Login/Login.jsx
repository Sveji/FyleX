import { useState } from "react"
import PopUp from "../PopUp/PopUp"
import './login.less'
import { Link } from "react-router-dom"

const Login = () => {
    // Holds the state for the form
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")



    // Sends a login request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()
    }



    return (
        <PopUp classes={'login-box'}>
            <div className="text-box">
                <h1>Login</h1>
                <p>Log in to your account to analyze your documents.</p>
            </div>

            <form className="account-form" onSubmit={(e) => handleSubmit(e)}>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />

                <button className="btn">Log in</button>
            </form>

            <div className="redirect-text">
                <p>Don't have an account?</p>
                <Link className="link">Register</Link>
            </div>
        </PopUp>
    )
}

export default Login
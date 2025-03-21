import { useContext, useState } from "react"
import AccountForm from "../../components/AccountBox/AccountForm"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"

const Register = () => {
    // Gets global data from the context
    const { crud, navigate } = useContext(DataContext)



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
    const [error, setError] = useState(null)



    // Sends a register request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()

        const response = await crud({
            url: '/api/user/register/',
            method: 'post',
            body: {
                username,
                email,
                password
            }
        })

        console.log(response)

        if(response.status == 400) {
            setError(response.response.data.error)
        }
        if(response.status == 201) {
            navigate('/activate-message')
        }
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
                error={error}
            />
        </PopUp>
    )
}

export default Register
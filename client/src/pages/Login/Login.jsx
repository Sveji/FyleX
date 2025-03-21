import { useContext, useState } from "react"
import AccountForm from "../../components/AccountBox/AccountForm"
import PopUp from "../../components/PopUp/PopUp"
import { DataContext } from "../../context/DataContext"

const Login = () => {
    // Gets global data from the context
    const { crud, navigate, setAccess, setRefresh } = useContext(DataContext)



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
    const [error, setError] = useState(null)



    // Sends a login request to the backend server
    const handleSubmit = async (e) => {
        e.preventDefault()

        const response = await crud({
            url: '/api/user/login/',
            method: 'post',
            body: {
                email,
                password
            }
        })

        console.log(response)

        if(response.status == 400 || response.status == 401) setError(response.response.data.error)
        if(response.status == 200) {
            localStorage.setItem('access', response.data.token.access)
            setAccess(response.data.token.access)
            localStorage.setItem('refresh', response.data.token.refresh)
            setRefresh(response.data.token.refresh)
            navigate('/')
        }
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
                error={error}
                forgotPass
            />
        </PopUp>
    )
}

export default Login